import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title = 'HIV market analysis 2025',
    layout = 'wide',
    initial_sidebar_state = 'collapsed'
)

if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

def next_page():
    st.session_state.page_num += 1

if st.session_state.page_num == 1:
    st.markdown(body = "## Для одних, ВИЧ - это приговор.", text_alignment='center')
    st.markdown(body = "## Для других, ВИЧ - это рынок.", text_alignment='center')
    st.write(' ')
    st.write(' ')
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
        <style>
        /* Center the button */
        .stButton > button {
            animation: pulse 2s infinite;
            background-color: #FF4B4B;
            color: white;
            border: none;
            font-size: 20px;
            font-weight: bold;
            padding: 15px 30px;
            border-radius: 10px;
            margin: 0 auto !important;
            display: block !important;
        }

        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
            70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button('смотреть рынок', use_container_width = True):
            next_page()
            st.rerun()

elif st.session_state.page_num == 2:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(body = "## В 2025 году, рынок первичных тестов на ВИЧ был поделён пятью производителями:",text_alignment = 'center')
        st.write('guangzhou_farm')
        st.write('standard_test')
        st.write('med_express')
        st.write('biolab')
        st.write('eshuer')
        st.write("Иногда, больницы объявляют открытую закупку, такие закупки помечены как free")

    b1, b2, b3 = st.columns([5, 1, 5])
    with b2:    
        if st.button("Дальше"):
            next_page()
            st.rerun()


elif st.session_state.page_num == 3:
    @st.cache_data(ttl=3600)
    def load_sales():
        df = pd.read_csv('hiv.csv')
        return df

    df = load_sales()

    #Picture 1: total sales
    st.markdown(body = "## Объём продаж в млн. руб.", text_alignment = 'center')
    total = df.groupby('vendor')['total'].sum().reset_index().sort_values(by = 'total', ascending=False)
    fig = px.bar(total, x = 'vendor', y = 'total', text_auto = '.3s', labels = {
        'vendor': 'Производитель',
        'total': 'Объём продаж, млн. руб.'
    })
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    #Picture 2: price
    st.markdown(body = "## Цена за тест в рублях", text_alignment = 'center')
    p1, p2 = st.columns(2)
    with p1:
        df = df.sort_values(by='price', ascending=False)
        fig = px.scatter(df,
                        x = 'vendor',
                        y = 'price',
                        color = 'price',
                        color_continuous_scale = 'RdYlGn_r',
                        title = 'Распределение цены',
                        labels = {
                            'vendor': 'Производитель',
                            'price': 'Цена'
                        })
        st.plotly_chart(fig, use_container_width = True)
    with p2:
        mean_price = df.groupby('vendor')['price'].mean().reset_index().sort_values(by='price', ascending=False)
        fig = px.bar(mean_price, x = 'vendor', y = 'price', text_auto = '.3s', title = 'Средняя цена', labels = {
            'vendor': 'Производитель',
            'price': 'Средняя цена'
        })
        fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
        st.plotly_chart(fig, use_container_width = True)

    #Picture 3: quantity
    st.markdown(body = "## Количество проданных тестов, в штуках", text_alignment = 'center')
    quantity = df.groupby('vendor')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False)
    fig = px.bar(quantity, x = 'vendor', y = 'quantity', text_auto = '.3s', title = 'Количество штук', labels = {
        'vendor': 'Производитель',
        'quantity': 'Количество, в штуках'
    })
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    #col1, col2, col3 = st.columns([3, 1, 3])
    #with col2:
    st.markdown(body = '## Лидер: med_express.', text_alignment = 'center')
    st.markdown(body = '## Почему?', text_alignment = 'center')
    st.markdown(body = '## Откаты?', text_alignment = 'center')
    st.markdown(body = '## Или характеристики?', text_alignment = 'center')
    
    b1, b2, b3 = st.columns([3, 1, 3])
    with b2:
        if st.button("смотреть характеристики"):
            next_page()
            st.rerun()

elif st.session_state.page_num == 4:

    #load feature data
    st.cache_data(ttl=3600)
    def load_vendors():
        vendor_data = {}
        vendor_files = {
            'med_express': 'med_express.xlsx',
            'eshuer': 'eshuer.xlsx',
            'guangzhou_farm': 'guangzhou_farm.xlsx',
            'biolab': 'biolab.xlsx',
            'standard_test': 'standard_test.xlsx'
        }

        for vendor_name, file_name in vendor_files.items():
            dfv = pd.read_excel(file_name)
            vendor_data[vendor_name] = dfv
        
        return vendor_data

    vendor_data = load_vendors()

    #Picture 4: Analytycal sensitivity
    ansen = []
    for vendor_name, dfv in vendor_data.items():
        an_sens = dfv['analytycal_sensitivity'].iloc[0]
        ansen.append({
            'vendor': vendor_name,
            'analytical_sensitivity': an_sens
        })
    st.markdown(body = "## Аналитическая чувствительность", text_alignment = 'center')
    st.markdown(body = "#### Основная характеристика. Чем меньше, тем лучше тест.", text_alignment = 'left')
    sens_df = pd.DataFrame(ansen)
    sens_df = sens_df.sort_values('analytical_sensitivity', ascending = True)
    fig = px.bar(sens_df, x = 'vendor', y = 'analytical_sensitivity', text = 'analytical_sensitivity', labels = {
        'vendor': 'Производитель',
        'analytical_sensitivity': 'Аналитическая чувствительность, в ме/мл'
    })
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    #Picture 5: Specificity
    specificity = []
    for vendor_name, dfv in vendor_data.items():
        spec = dfv['specificity'].iloc[0]
        specificity.append({
            'vendor': vendor_name,
            'specificity': spec
        })

    st.markdown(body = "## Специфичность", text_alignment = 'center')
    st.markdown(body = "#### Абсолютно бесполезная характеристика.", text_alignment = 'left')
    st.markdown(body = "#### Технически - больше специфичность, меньше ложных результатов.", text_alignment = 'left')
    st.markdown(body = "#### На практике, эта характеристика считается в процентах.", text_alignment = 'left')
    st.markdown(body = "#### Поэтому любой производитель может посчитать её как надо для маркетинга.", text_alignment = 'left')
    specificity_df = pd.DataFrame(specificity)
    specificity_df = specificity_df.sort_values('specificity', ascending = False)
    fig = px.bar(specificity_df,
                x = 'vendor',
                y = 'specificity',
                text = specificity_df['specificity'].apply(lambda x: f"{x:.0f}%"),
                labels = {
                    'vendor': 'Производитель',
                    'specificity': 'Специфичность, %'
                })
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    #Picture 6: blood_sample_amount
    blood = []
    for vendor_name, dfv in vendor_data.items():
        bl = dfv['sample_amount'].iloc[0]
        blood.append({
            'vendor': vendor_name,
            'blood_sample_amount': bl
        })
    st.markdown(body = "## Объём крови взятый у пациента, в микролитрах", text_alignment = 'center')
    st.markdown(body = "#### Важная характеристика - чем меньше, тем лучше.", text_alignment = 'left')
    st.markdown(body = "#### Врачи любят, когда не нужно выдавливать много крови из пациента.", text_alignment = 'left')
    st.markdown(body = "#### Особенно из детей.", text_alignment = 'left')
    blood_df = pd.DataFrame(blood)
    blood_df = blood_df.sort_values('blood_sample_amount', ascending = True)
    fig = px.bar(blood_df,
                x = 'vendor',
                y = 'blood_sample_amount',
                text = blood_df['blood_sample_amount'].apply(lambda x: f"{x:.0f} мкл"),
                labels = {
                    'vendor': 'Производитель',
                    'blood_sample_amount': 'Объём крови, мкл'
                }
    )
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    #Picture 7: time
    time = []
    for vendor_name, dfv in vendor_data.items():
        ti = dfv['time'].iloc[0]
        time.append({
            'vendor': vendor_name,
            'minutes': ti
        })

    st.markdown(body = "## Время теста", text_alignment = 'center')
    st.markdown(body = "#### Ключевая характеристика - чем меньше, тем лучше.", text_alignment = 'left')
    st.markdown(body = "#### По приказу Минздрава 290Н, на одного пациента отводится 15 минут.", text_alignment = 'left')
    st.markdown(body = "#### По факту, у врачей нет этого времени.", text_alignment = 'left')
    st.markdown(body = "#### Пациент находится в кабинете в среднем 7-10 минут.", text_alignment = 'left')
    st.markdown(body = "#### Пациент выходит за дверь - тест летит в мусорку.", text_alignment = 'left')
    time_df = pd.DataFrame(time)
    time_df = time_df.sort_values('minutes', ascending = True)
    fig = px.bar(time_df,
                x = 'vendor',
                y = 'minutes',
                text = time_df['minutes'].apply(lambda x: f"{x:.0f} мин."),
                labels = {
                    'vendor': 'Производитель',
                    'minutes': 'минуты'
                }
    )
    fig.update_traces(textfont_size = 12, textangle = 0, textposition = 'outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width = True)

    b1, b2, b3 = st.columns([5, 1, 5])
    with b2:
        if st.button('Выводы'):
            next_page()
            st.rerun()

elif st.session_state.page_num == 5:
    st.markdown('### med_express забирает рынок из-за своих характеристик.', text_alignment = 'center')
    st.markdown('#### Есть два способа подвинуть его:')
    st.markdown('#### 1) Предложить характеристики лучше:')
    st.markdown('##### - 0,05 против 0,1;')
    st.markdown('##### - 2 минуты против 3;')
    st.markdown('##### - 5 мкл. против 10.')
    st.markdown('##### - но не всё может оказаться реальным, потому что каждая технология имеет свой потолок.')
    st.markdown('#### 2) Предложить такие же характеристики, но за меньшую цену.')
    
    b1, b2, b3 = st.columns([5, 1, 5])
    with b2:
        if st.button('Заключение'):
            next_page()
            st.rerun()

elif st.session_state.page_num == 6:
    st.markdown('#### Данный проект является тренировочным проектом для портфолио.', text_alignment = 'center')
    st.markdown('#### Все наименования производителей и финансовые показатели являются вымышленными.', text_alignment = 'center')
    st.markdown('#### Остальная информация, к сожалению, нет.', text_alignment = 'center')
    st.markdown('#### Благодарю за внимание.', text_alignment = 'center')