# Libraries:
import numpy               as np
import pandas              as pd
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gs
import matplotlib.ticker   as ticker
import matplotlib.dates    as mdates
import seaborn             as sns
import streamlit           as st
from   datetime        import date, datetime, timedelta
st.set_page_config(page_title='COVID19', page_icon='😷')
DATA     = 'https://covid.ourworldindata.org/data/owid-covid-data-old.csv'
@st.cache_data
def LoadData():
    data = pd.read_csv(DATA, index_col=0)
# Selecting Coluns:
    X    = data[['date',
                 'location',
                 'new_cases_smoothed',
                 'new_deaths_smoothed',
                 'new_vaccinations_smoothed']].copy()
    X.reset_index(inplace=True)
    X['date'] = pd.to_datetime(X['date'], format='%Y-%m-%d')
    X.set_index('date',   inplace=True)
    X.sort_index(inplace=True)
    return X
df      = LoadData()
# SIDE:
st.sidebar.header(   'COVID-19     ')
st.sidebar.subheader('Data Analysis')
st.sidebar.write(    'Comparisson Charts')
st.sidebar.divider()

Location1    = df['location'].unique()
# SelectBox for Location:
FilteredLoc1 = st.sidebar.selectbox('Location 1:', Location1, index=7)
# PlaceHolder for Filtered Entries:
SideBarInfo1 = st.sidebar.empty()
# PlaceHolder for Table:
table1       = st.sidebar.empty()
# Filtered Data:
FilteredDF1  = df[df['location'].str.contains(FilteredLoc1)]
# Updating PlaceHoder:
SideBarInfo1.info('{} Entries for {}'.format(FilteredDF1.shape[0], FilteredLoc1))

# MAIN:
st.title(    'COVID-19')
st.markdown('''
[![GitHub](https://img.shields.io/badge/GitHub-000000?logo=github&logoColor=white)](https://github.com/kauefs/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kauefs/)
[![Python](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-black.svg)](https://www.apache.org/licenses/LICENSE-2.0)
            ''')
st.write('23 October 2023')
st.subheader('Comparisson Charts')
st.markdown(f'''➡️ {'**{}**'.format(FilteredDF1.shape[0])} Entries for **{FilteredLoc1}**:'''
            'from {} to {}'.format(df.loc[df.location == FilteredLoc1].index.min(), df.loc[df.location == FilteredLoc1].index.max()))
fig,ax= plt.subplots(figsize=(12,8)  , tight_layout=True)
df.loc[df.location == FilteredLoc1,'new_vaccinations_smoothed'].plot(
                kind       ='line'   ,
                label      ='Vaccinations',
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#4CAF50',
                linewidth  ='2.25'   ,
                ms=.01, mec='#4CAF50',   mfc='#4CAF50')
df.loc[df.location == FilteredLoc1,'new_cases_smoothed'].plot(
                kind       ='line'   ,
                label      ='Cases'  ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',   mfc='#FF8C00')
df.loc[df.location == FilteredLoc1,'new_deaths_smoothed'].plot(
                kind       ='line'   ,
                label      ='Deaths' ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F',   mfc='#FF103F')
ax.set_title('COVID in {}: Vaccinations & Cases & Deaths (Log Scale)'.format(FilteredLoc1), fontsize=20, fontweight='bold')
ax.grid(linestyle=':' ,   linewidth=1, color='#DCDCDC')
ax.tick_params(axis   ='both',
                which ='both',
                left  = False,
                bottom= False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax.xaxis.set_tick_params(rotation=0)
ax.set(xlabel=None)
ax.spines[['top',  'right', 'left', 'bottom']].set_visible(False)
ax.legend(loc='upper left', fontsize=15)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale(   'log')
plt.show()
st.pyplot(fig)
if table1.checkbox('Show Table Data 1', value=False):st.write(FilteredDF1)
st.divider()

Location2    = df['location'].unique()
# SelectBox for Location:
FilteredLoc2 = st.sidebar.selectbox('Location 2:', Location2, index=8)
# PlaceHolder for Filtered Entries:
SideBarInfo2 = st.sidebar.empty()
# PlaceHolder for Table:
table2       = st.sidebar.empty()
# Filtered Data:
FilteredDF2  = df[df['location'].str.contains(FilteredLoc2)]
# Updating PlaceHoder:
SideBarInfo2.success('{} Entries for {}'.format(FilteredDF2.shape[0], FilteredLoc2))

st.sidebar.divider()
st.sidebar.markdown('''Source:    [Our World in Data](https://covid.ourworldindata.org/)''')
st.sidebar.write(    'Johns Hopkins University daily reports from {} to {}'.format(df.index.min(), df.index.max()))
st.sidebar.markdown('''Reference: [Data Cleaning Techniques in Python: the Ultimate Guide](https://www.justintodata.com/data-cleaning-techniques-python-guide/)''')
st.sidebar.divider()

with st.sidebar.container():
     cols = st.columns(3)
     with cols[0]:st.empty()
     with cols[1]:st.markdown('''©2023™''')
     with cols[2]:st.empty()

st.markdown(f'''➡️ {'**{}**'.format(FilteredDF2.shape[0])} Entries for **{FilteredLoc2}**:'''
            'from {} to {}'.format(df.loc[df.location == FilteredLoc2].index.min(), df.loc[df.location == FilteredLoc2].index.max()))
fig,ax= plt.subplots(figsize=(12,8)  , tight_layout=True)
df.loc[df.location == FilteredLoc2,'new_vaccinations_smoothed'].plot(
                kind       ='line'   ,
                label      ='Vaccinations',
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#4CAF50',
                linewidth  ='2.25'   ,
                ms=.01, mec='#4CAF50',   mfc='#4CAF50')
df.loc[df.location == FilteredLoc2,'new_cases_smoothed'].plot(
                kind       ='line'   ,
                label      ='Cases'  ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',   mfc='#FF8C00')
df.loc[df.location == FilteredLoc2,'new_deaths_smoothed'].plot(
                kind       ='line'   ,
                label      ='Deaths' ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F',   mfc='#FF103F')
ax.set_title('COVID in {}: Vaccinations & Cases & Deaths (Log Scale)'.format(FilteredLoc2), fontsize=20, fontweight='bold')
ax.grid(linestyle=':' ,   linewidth=1, color='#DCDCDC')
ax.tick_params(axis   ='both',
                which ='both',
                left  = False,
                bottom= False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax.xaxis.set_tick_params(rotation=0)
ax.set(xlabel=None)
ax.spines[['top',  'right', 'left', 'bottom']].set_visible(False)
ax.legend(loc='upper left', fontsize=15)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale(   'log')
plt.show()
st.pyplot(fig)
if table2.checkbox('Show Table Data 2', value=False):st.write(FilteredDF2)
st.toast('Vaccinate!', icon='💉')
