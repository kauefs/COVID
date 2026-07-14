# Libraries
import streamlit           as   st
import numpy               as   np
import pandas              as   pd
import matplotlib.gridspec as   gs
import matplotlib.pyplot   as   plt
import matplotlib.ticker   as   ticker
import matplotlib.dates    as   mdates
import seaborn             as   sns
from   datetime          import date, datetime, timedelta
st.set_page_config(page_title='COVID19', page_icon='😷', layout='wide', initial_sidebar_state='expanded')
# DATA     https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv
DATA     ='https://github.com/owid/covid-19-data/raw/refs/heads/master/public/data/owid-covid-data.csv'
@st.cache_data
def LoadData( ):
    data =pd.read_csv(DATA) #, index_col=1)
# Selecting Columns
    columns=['date',
             'location',
             'total_cases',
             'total_deaths',
             'new_cases_smoothed',
             'new_deaths_smoothed',
             'new_vaccinations_smoothed']
    existingCols=[c for c in columns if c in data.columns]
    X=data[existingCols].copy( )
    X['date']=pd.to_datetime(X['date'], format='%Y-%m-%d')
    X. set_index('date', inplace=True)
    X.sort_index(        inplace=True)
    return X
try:df=LoadData( )
except Exception as e:
    st.error(f'Failed to load data. Falling back to local data structure. Error: {e}')
    # FallBack Structure
    df=pd.DataFrame(columns=['location','total_cases','total_deaths','new_cases_smoothed','new_deaths_smoothed','new_vaccinations_smoothed'])
# SIDE
st.sidebar.title    ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.divider  (                     )
st.sidebar.title    ('COVID-19'           )
st.sidebar.header   ('Data Analysis'      )
st.sidebar.subheader('Comparisson Charts' )
st.sidebar.divider  (                     )
if not df.empty:locations=df['location'].dropna( ).sort_values( ).unique( )
else           :locations['No Data Loaded']
FilteredLoc1=st.sidebar.selectbox('Location 1', locations, index= 97)
SideBarInfo1=st.sidebar.empty( )
table1      =st.sidebar.empty( )
FilteredDF1 =df[df['location']==FilteredLoc1]
SideBarInfo1.info(f'{FilteredDF1.shape[0]} entries for {FilteredLoc1}')
FilteredLoc2=st.sidebar.selectbox('Location 2', locations, index=128)
SideBarInfo2=st.sidebar.empty( )
table2      =st.sidebar.empty( )
FilteredDF2 =df[df['location']==FilteredLoc2]
SideBarInfo2.success(f'{FilteredDF2.shape[0]} entries for {FilteredLoc2}')
st.sidebar.divider (   )
st.sidebar.markdown('''Source:    [Our World in Data](https://github.com/owid/covid-19-data/)''')
st.sidebar.write   ( f'OWID daily reports from {df.index.min( ).strftime('%Y-%m-%d')} to {df.index.max( ).strftime('%Y-%m-%d')}')
st.sidebar.markdown('''Reference: [Data Cleaning Techniques in Python: the Ultimate Guide](https://www.justintodata.com/data-cleaning-techniques-python-guide/)''')
st.sidebar.divider (   )
st.sidebar.markdown('''
![2023.10.23   ](https://img.shields.io/badge/2023.10.23-000000)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2026&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN
st.divider  (                    )
st.title    (      'COVID-19'    )
st.divider  (                    )
st.subheader('Comparisson Charts')
# Chart1
if not FilteredDF1.empty:
    st.markdown(f'''➡️ **{FilteredDF1.shape[0]}** entries for **{FilteredLoc1}**
                from {df.loc[df['location']==FilteredLoc1].index.min( ).strftime('%Y-%m-%d')} to {df.loc[df['location']==FilteredLoc1].index.max( ).strftime('%Y-%m-%d')}''')
    fig,ax=plt.subplots(figsize=(12, 6), frameon=True , tight_layout=True)
    FilteredLoc1['new_vaccinations_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Vaccinations',
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#4CAF50',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#4CAF50',   mfc='#4CAF50')
    FilteredLoc1['new_cases_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Cases'  ,
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#FF8C00',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#FF8C00',   mfc='#FF8C00')
    FilteredLoc1['new_deaths_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Deaths' ,
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#FF103F',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#FF103F',   mfc='#FF103F')
    ax.set_title(f'COVID in {FilteredLoc1} – Vaccinations & Cases & Deaths', fontsize=15, fontweight='bold')
    ax.grid(linestyle=':',   linewidth=.75,   color='#DCDCDC')
    ax.tick_params(axis='both', which ='both', left=False, bottom=False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
    ax.xaxis.set_tick_params(rotation=0)
    ax.set(xlabel=None)
    for spine in ax.spines.values( ):spine.set_visible(False)
    ax.legend(loc='upper right', fontsize=13,  frameon=False)
    plt.gca( ).set_ylim(bottom=10**0)
    plt.yscale  ('log')
    st.pyplot    (fig)
    if table1.checkbox('DataFrame 1', value=False):st.dataframe(FilteredDF1, width='stretch')
    st.markdown('''
                ''')
    st.markdown(f'''**{FilteredLoc1}**''')
    C1=                FilteredLoc1['total_cases' ].max( )
    D1=                FilteredLoc1['total_deaths'].max( )
    valC1=f'{C1:,.0f}' if pd.notna(C1)else'No Data'
    valD1=f'{D1:,.0f}' if pd.notna(D1)else'No Data'
    st.write(f'• Total   cases:   {valC1}')
    st.write(f'• Total  deaths:   {valD1}')
else:st.warning(f'No available logs to map for {FilterdLoc1}')
st.divider( )
# Chart2
if not FilteredDF2.empty:
    st.markdown(f'''➡️ **{FilteredDF2.shape[0]}** entries for **{FilteredLoc2}**
                from {df.loc[df['location']==FilteredLoc2].index.min( ).strftime('%Y-%m-%d')} to {df.loc[df['location']==FilteredLoc2].index.max( ).strftime('%Y-%m-%d')}''')
    fig,ax=plt.subplots(figsize=(12, 6), frameon=True , tight_layout=True)
    FilteredLoc2['new_vaccinations_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Vaccinations',
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#4CAF50',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#4CAF50',   mfc='#4CAF50')
    FilteredLoc2['new_cases_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Cases'  ,
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#FF8C00',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#FF8C00',   mfc='#FF8C00')
    FilteredLoc2['new_deaths_smoothed'].plot(
                    kind       ='line'   ,
                    label      ='Deaths' ,
                    ax         = ax      ,
                    marker     ='o'      ,
                    linestyle  ='solid'  ,
                    color      ='#FF103F',
                    linewidth  = 2.25    ,
                    ms=.01, mec='#FF103F',   mfc='#FF103F')
    ax.set_title(f'COVID in {FilteredLoc2} – Vaccinations & Cases & Deaths', fontsize=15, fontweight='bold')
    ax.grid(linestyle=':',   linewidth=.75,   color='#DCDCDC')
    ax.tick_params(axis='both', which ='both', left=False, bottom=False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
    ax.xaxis.set_tick_params(rotation=0)
    ax.set(xlabel=None)
    for spine in ax.spines.values( ):spine.set_visible(False)
    ax.legend(loc='upper right', fontsize=13,  frameon=False)
    plt.gca( ).set_ylim(bottom=10**0)
    plt.yscale  ('log')
    st.pyplot    (fig)
    if table2.checkbox('DataFrame 2', value=False):st.dataframe(FilteredDF2, width='stretch')
    st.markdown(f'''**{FilteredLoc2}**''')
    C2=                FilteredLoc2['total_cases' ].max( )
    D2=                FilteredLoc2['total_deaths'].max( )
    valC2=f'{C2:,.0f}' if pd.notna(C2)else'No Data'
    valD2=f'{D2:,.0f}' if pd.notna(D2)else'No Data'
    st.write(f'• Total   cases:   {valC2}')
    st.write(f'• Total  deaths:   {valD2}')
else:st.warning(f'No available logs to map for {FilterdLoc2}')
st.toast('Vaccinate!', icon='💉')
