import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='NPA dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and weight
    gdp_df = raw_gdp_df.melt(
        ['Country Code'], # kommun_namn
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year', # year
        'GDP',  # weight
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()
print(gdp_df)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: NPA dashboard
'''

# Add some spacing
''
''
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

st.line_chart(
    filtered_result_df_year,
    x='year',
    y='weight',
    color='materialslag_namn', # Kommun namn
)

my_first_year = df_results[df_results['year'] == my_from_year]
my_last_year = df_results[df_results['year'] == my_to_year]

st.header(f'Weight in {my_to_year}', divider='gray')


cols = st.columns(4)

for i, kommun in enumerate(selected_kommun):
    col = cols[i % len(cols)]

    with col:
        first_weight = my_first_year[my_first_year['kommun_namn'] == kommun]['weight'].iat[0] / 1000000000
        last_weight = my_last_year[my_last_year['kommun_namn'] == kommun]['weight'].iat[0] / 1000000000

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







min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Vilket åt vill du undersöka?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Välj minst ett material")

selected_countries = st.multiselect(
    'Vilket material vill du undersöka?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('FTI översikt', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

''
''


first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
