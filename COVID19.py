# Libraries:
import numpy               as np
import pandas              as pd
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gs
import matplotlib.ticker   as ticker
import matplotlib.dates    as mdates
import seaborn             as sns
import streamlit           as st
#import bar_chart_race      as bcr
#from   wordcloud         import WordCloud, STOPWORDS, ImageColorGenerator
#from   PIL import Image
from   datetime        import date, datetime, timedelta
st.set_page_config(page_title='COVID-19', page_icon='😷')
# DATA:https://covid.ourworldindata.org/data/owid-covid-data-old.csv
DATA         = 'datasets/COVID19W.csv'
@st.cache_data
def LoadData():
    data     = pd.read_csv(DATA, index_col=0, parse_dates=True)
    return data
df           = LoadData()
# MAIN:
st.title(    'COVID-19')
# Table:
st.subheader('DATA')
st.markdown( '''Source: [Our World in Data](https://covid.ourworldindata.org/)''')
st.markdown( 'Period covered by The Johns Hopkins CoronaVirus Resource Center: from {} to {}'.format(df.index.min(), df.index.max()))
# SIDE:
st.sidebar.header(   'COVID-19     ')
st.sidebar.subheader('Data Analysis')
st.sidebar.write(    'Comparissons')

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

st.markdown(f'''➡️ {'**{}**'.format(FilteredDF1.shape[0])} Entries for **{FilteredLoc1}**:'''
            'from {} to {}'.format(df.loc[df.location == FilteredLoc1].index.min(), df.loc[df.location == FilteredLoc1].index.max()))
fig,ax= plt.subplots(figsize=(12,8)  , tight_layout=True)
df.loc[df.location == FilteredLoc1,'new_vaccinations_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Vaccinations',
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#4CAF50',
                linewidth  ='2.25'   ,
                ms=.01, mec='#4CAF50',   mfc='#4CAF50')
df.loc[df.location == FilteredLoc1,'new_cases_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Cases'  ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',   mfc='#FF8C00')
df.loc[df.location == FilteredLoc1,'new_deaths_smoothed'].sort_values(ascending=False).plot(
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
ax.legend(loc='best', fontsize=15)
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

st.markdown(f'''➡️ {'**{}**'.format(FilteredDF2.shape[0])} Entries for **{FilteredLoc2}**:'''
            'from {} to {}'.format(df.loc[df.location == FilteredLoc2].index.min(), df.loc[df.location == FilteredLoc2].index.max()))
fig,ax= plt.subplots(figsize=(12,8)  , tight_layout=True)
df.loc[df.location == FilteredLoc2,'new_vaccinations_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Vaccinations',
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#4CAF50',
                linewidth  ='2.25'   ,
                ms=.01, mec='#4CAF50',   mfc='#4CAF50')
df.loc[df.location == FilteredLoc2,'new_cases_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Cases'  ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',   mfc='#FF8C00')
df.loc[df.location == FilteredLoc2,'new_deaths_smoothed'].sort_values(ascending=False).plot(
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
ax.legend(loc='best', fontsize=15)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale(   'log')
plt.show()
st.pyplot(fig)
if table2.checkbox('Show Table Data 2', value=False):st.write(FilteredDF2)
st.divider()
with st.container():
     C1,  C2,C3,C4, C5 = st.columns(5)
     with C1:st.empty()
     with C2:st.empty()
     with C3:st.markdown('''©2023™''')
     with C4:st.empty()
     with C5:st.empty()
st.toast('Vaccinate!', icon='💉')
