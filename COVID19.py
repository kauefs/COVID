# Libraries:
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
# DATA:
DATA     = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
@st.cache_data
def LoadData():
    data = pd.read_csv(DATA, index_col=0)
# Selecting Columns:
    X    = data[['date',
                 'location',
                 'total_cases',
                 'total_deaths',
                 'new_cases_smoothed',
                 'new_deaths_smoothed',
                 'new_vaccinations_smoothed']].copy()
    X.reset_index(inplace=True)
    X['date'] = pd.to_datetime(X['date'], format='%Y-%m-%d')
    X.set_index('date',   inplace=True)
    X.sort_index(inplace=True)
    return X
df            =  LoadData(   )
# SIDE:
st.sidebar.title    ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.divider  (                     )
st.sidebar.title    ('COVID-19'           )
st.sidebar.header   ('Data Analysis'      )
st.sidebar.subheader('Comparisson Charts' )
st.sidebar.divider  (                     )
Location1    = df['location'].sort_values(ascending=True).unique()
FilteredLoc1 = st.sidebar.selectbox('Location 1:', Location1, index=241)
SideBarInfo1 = st.sidebar.empty()
table1       = st.sidebar.empty()
FilteredDF1  = df[df['location'].str.contains(FilteredLoc1)]
SideBarInfo1.info('{} Entries for {}'.format(FilteredDF1.shape[0], FilteredLoc1))
Location2    = df['location'].sort_values(ascending=True).unique()
FilteredLoc2 = st.sidebar.selectbox('Location 2:', Location2, index=128)
SideBarInfo2 = st.sidebar.empty()
table2       = st.sidebar.empty()
FilteredDF2  = df[df['location'].str.contains(FilteredLoc2)]
SideBarInfo2.success('{} Entries for {}'.format(FilteredDF2.shape[0], FilteredLoc2))
st.sidebar.divider (   )
st.sidebar.markdown('''Source:    [Our World in Data](https://covid.ourworldindata.org/)''')
st.sidebar.write   (  'OWID daily reports from {} to {}'.format(df.index.min(), df.index.max()))
st.sidebar.markdown('''Reference: [Data Cleaning Techniques in Python: the Ultimate Guide](https://www.justintodata.com/data-cleaning-techniques-python-guide/)''')
st.sidebar.divider (   )
st.sidebar.markdown('''
![2023.10.23   ](https://img.shields.io/badge/2023.10.23-000000)

[![GitHub      ](https://img.shields.io/badge/GitHub-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/Medium-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/Python3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2024&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.divider  (                    )
st.title    ('COVID-19'          )
st.divider  (                    )
st.subheader('Comparisson Charts')
# Chart1:
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
ax.set_title('COVID in {}: Vaccinations & Cases & Deaths'.format(FilteredLoc1), fontsize=20, fontweight='bold')
ax.grid(linestyle=':' ,   linewidth=1, color='#DCDCDC')
ax.tick_params(axis   ='both',
                which ='both',
                left  = False,
                bottom= False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax.xaxis.set_tick_params(rotation=0)
ax.set(xlabel=None)
ax.spines[['top',  'right', 'left', 'bottom']].set_visible(False)
ax.legend(loc='upper left',  fontsize=15)
plt.gca().set_ylim(bottom=10**0)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale  ( 'log')
st.pyplot(fig)
if table1.checkbox('DataFrame 1', value=False):st.write(FilteredDF1)
st.markdown('''
            ''')
st.markdown(f'''Latest entries for **{FilteredLoc1}**:''')
AA=df.loc[  df.location          == FilteredLoc1].copy()
C1=         aa['total_cases'              ].sort_values(ascending=False)[0]
D1=         aa['total_deaths'             ].sort_values(ascending=False)[0]
d1=aa.index[aa['new_deaths_smoothed'      ]!=0.0][-1].strftime('%d %b %Y')
c1=aa.index[aa['new_cases_smoothed'       ]!=0.0][-1].strftime('%d %b %Y')
v1=aa.index[aa['new_vaccinations_smoothed']!=0.0][-1].strftime('%d %b %Y')
st.write('• Total   cases:       {:,.0f}'.format(C1))
st.write('  – Lastest  case:          {}'.format(c1))
st.write('• Total  deaths:       {:,.0f}'.format(D1))
st.write('  – Lastest death:          {}'.format(d1))
st.write('• Lastest vaccination:      {}'.format(v1))
# Chart2:
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
ax.set_title('COVID in {}: Vaccinations & Cases & Deaths'.format(FilteredLoc2), fontsize=20, fontweight='bold')
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
plt.gca().set_ylim(bottom=10**0)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale(   'log')
st.pyplot(fig)
if table2.checkbox('DataFrame 2', value=False):st.write(FilteredDF2)
st.markdown(f'''Latest entries for **{FilteredLoc2}**:''')
aa = df.loc[  df.location          == FilteredLoc2].copy()
C2=         aa['total_cases'              ].sort_values(ascending=False)[0]
D2=         aa['total_deaths'             ].sort_values(ascending=False)[0]
d2=aa.index[aa['new_deaths_smoothed'      ]!=0.0][-1].strftime('%d %b %Y')
c2=aa.index[aa['new_cases_smoothed'       ]!=0.0][-1].strftime('%d %b %Y')
v2=aa.index[aa['new_vaccinations_smoothed']!=0.0][-1].strftime('%d %b %Y')
st.write('• Total   cases:       {:,.0f}'.format(C2))
st.write('  – Lastest  case:          {}'.format(c2))
st.write('• Total  deaths:       {:,.0f}'.format(D2))
st.write('  – Lastest death:          {}'.format(d2))
st.write('• Lastest vaccination:      {}'.format(v2))
st.toast('Vaccinate!', icon='💉')
