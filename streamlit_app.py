import streamlit as st
import pandas as pd
import math

df_results = pd.read_csv('data/result_sum_weight_kommun.csv')
print(df_results)

my_min = df_results['year'].min()
my_max = df_results['year'].max()
print(my_min)
print(my_max)

my_from_year, my_to_year = st.slider(
    'Vilket år vill du undersöka?',
    min_value=my_min,
    max_value=my_max,
    value=[my_min, my_max])

kommun = df_results['kommun_namn'].unique()

if not len(kommun):
    st.warning("Välj minst en kommun")

selected_kommun = st.multiselect(
    'Vilken kommun vill du undersöka?',
    kommun,
    ['Ale'])

# Filter the data year
filtered_result_df_year = df_results[
    (df_results['kommun_namn'].isin(selected_kommun))
    & (df_results['year'] <= my_to_year)
    & (my_from_year <= df_results['year'])
]

st.header('FTI översikt', divider='gray')

st.subheader('Plast')
df_plast = filtered_result_df_year[filtered_result_df_year['materialslag_namn'] == 'Plast'] 
st.line_chart(
    df_plast,
    x='year',
    y='weight',
    color='kommun_namn', # Kommun namn
)

st.subheader('Metall')
df_metall = filtered_result_df_year[filtered_result_df_year['materialslag_namn'] == 'Metall'] 
st.line_chart(
    df_metall,
    x='year',
    y='weight',
    color='kommun_namn', # Kommun namn
)

st.subheader('Kartong')
df_kartong = filtered_result_df_year[filtered_result_df_year['materialslag_namn'] == 'Kartong'] 
st.line_chart(
    df_kartong,
    x='year',
    y='weight',
    color='kommun_namn', # Kommun namn
)

st.subheader('Tidningar')
df_tidningar = filtered_result_df_year[filtered_result_df_year['materialslag_namn'] == 'Tidningar'] 
st.line_chart(
    df_tidningar,
    x='year',
    y='weight',
    color='kommun_namn', # Kommun namn
)

st.subheader('Glas')
df_glas = filtered_result_df_year[filtered_result_df_year['materialslag_namn'] == 'Glas'] 
st.line_chart(
    df_glas,
    x='year',
    y='weight',
    color='kommun_namn', # Kommun namn
)

my_first_year = df_results[df_results['year'] == my_from_year]
my_last_year = df_results[df_results['year'] == my_to_year]

st.header(f'Weight in {my_to_year}', divider='gray')


cols = st.columns(4)

for i, kommun in enumerate(selected_kommun):
    col = cols[i % len(cols)]

    with col:
        first_weight = my_first_year[my_first_year['kommun_namn'] == kommun]['weight']
        last_weight = my_last_year[my_last_year['kommun_namn'] == kommun]['weight']

        if math.isnan(first_weight):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_weight / first_weight:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{kommun} weight',
            value=f'{last_weight:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )