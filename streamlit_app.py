import streamlit as st
import pandas as pd

df_results = pd.read_csv('data/result_kommun.csv')
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