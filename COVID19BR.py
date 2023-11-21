# Libraries:
import numpy               as np
import pandas              as pd
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gs
import matplotlib.ticker   as ticker
import matplotlib.dates    as mdates
import seaborn             as sns
import streamlit           as st
import datetime
st.set_page_config(page_title='COVID19BR', page_icon='😷', initial_sidebar_state='collapsed')
DATA     = 'https://covid.ourworldindata.org/data/owid-covid-data-old.csv'
@st.cache_data
def LoadData():
    data = pd.read_csv(DATA, index_col=0)
# Selecting Coluns:
    df   = data[['date',
                 'location',
                 'total_cases',
                 'total_deaths',
                 'new_cases_smoothed',
                 'new_deaths_smoothed',
                 'new_vaccinations_smoothed']].copy()
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.set_index('date',         inplace=True)
    df.sort_index(inplace=True)
    return df
RAW      = LoadData()
# Filling Missing Data:
X        = RAW.copy() 
num      = X.select_dtypes(include=['number']).columns
X[num]   = X[num].fillna(0)
nan      = X.select_dtypes(exclude=['number']).columns
X[nan]   = X[nan].fillna('N/A')
OWID     = X.copy()
# SIDE:
st.sidebar.header(   'COVID-19 in Brazil')
st.sidebar.subheader('Data Analysis')
st.sidebar.divider()
st.sidebar.markdown('''Source:    [Our World in Data](https://covid.ourworldindata.org/)''')
st.sidebar.write(    'Johns Hopkins University daily reports from 2020.01.01 to 2023.03.07')
st.sidebar.markdown('''Reference: [Data Cleaning Techniques in Python: the Ultimate Guide](https://www.justintodata.com/data-cleaning-techniques-python-guide/)''')
st.sidebar.divider()
with st.sidebar.container():
     C1,  C2,  C3 = st.columns(3)
     with C1:st.empty()
     with C2:st.markdown('''©2023™''')
     with C3:st.empty()
# MAIN:
st.title(   'The case of COVID-19 in Brazil')
st.markdown('''
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kauefs-blue.svg)](https://www.linkedin.com/in/kauefs/)
[![GitHub](https://img.shields.io/badge/GitHub-kauefs-black.svg)](https://github.com/kauefs/)
[![](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![GPLv3 license](https://img.shields.io/badge/License-Apache2-black.svg)](http://perso.crans.org/besson/LICENSE.html)
            ''')
st.write('23 November 2023')
st.markdown('''
Brazil is the fifth largest country in the world and the seventh in population with over 200 million inhabitants.
When COVID-19 outbreak begun on the eve of 2020; and even though the first case had been registered at the end of February,
with the first death coming the following month, fifteen days later, the country had been relatively 'safe' during the first semester of 2020.
Signs of how the country was going to deal with the outbreak though were less hopeful. A month into 'lockdown' the then Minister of Health,
a physician, was fired by the then President because the Minister was trying to keep the population safe from the pandemic,
following the World Health Organization (WHO) directives. The then President, however was against it saying it would damage the economy.
From there on the then President became the _de facto_ Minister of Health, instating new ministers that would only 'follow orders'.
The then President diminished the disease and discredited vaccines.
            ''')

st.subheader('Chart 1: Top 5 Countries with most Deaths')
fig,ax = plt.subplots(figsize=(15,5), tight_layout=True)
deaths = (OWID.loc[(OWID.index[-1]), ['location', 'total_deaths']].sort_values(by='total_deaths', ascending=False).iloc[9:14])
sns.barplot(x='location',   y='total_deaths', data=deaths, ax=ax, palette='autumn', saturation=.75)
ax.set_title('COVID-19: Top 5 Countries with Most Deaths', fontsize=22, fontweight='bold')
for spine in ['top', 'right', 'left', 'bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(True)
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
    tick.set_fontsize(15)
plt.tick_params(axis  = 'both',
                which = 'both',
                bottom=  False)
for c in ax.containers:
    values = deaths.value_counts(ascending=False).iloc[9:14].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=13, padding=10, fontweight='bold')
ax.set(xlabel=None)
plt.show()
st.pyplot(fig)
st.markdown('''
The consequences could not have been more sinister. Brazil has become the country with the second highest death toll,
only behind the United States. A death toll rate that was almost twice the worldwide rate of 1% of deaths from registered cases.
            ''')

st.subheader('Chart 2: Line Evolution for COVID-19 WorldWide (Cases & Deaths)')
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12,8), tight_layout=True)
OWID.loc[OWID.location =='World', 'total_cases'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax1     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',    mfc='#FF8C00')
ax1.annotate('{:,.0f}'.format(OWID['total_cases'].sort_values(ascending=False)[0]),
                xy=(1, OWID['total_cases'].sort_values(ascending=False)[0]),
                xycoords=('axes fraction', 'data'),
                xytext=(-85,1.15),
                textcoords='offset points',
                color='#FF4500',
                fontsize=12,
                fontweight='semibold')
ax1.set_title('COVID-19: WorldWide Cases', fontsize=15, fontweight='bold')
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax1.grid(linestyle=':', linewidth=1, color='#DCDCDC', mouseover=True)
ax1.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax1.set_yticks([0, 100000000, 200000000, 300000000, 400000000,  500000000,  600000000], minor=False)
#ax1.set_xticks(['2020-01','2020-06','2021-01','2021-06','2022-01','2022-06','2023-01'], minor=False)
ax1.set(xlabel=None)
ax1.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
OWID.loc[OWID.location =='World', 'total_deaths'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax2     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F',     mfc='#FF103F')
ax2.annotate('{:,.0f}'.format(OWID['total_deaths'].sort_values(ascending=False)[0]),
                xy=(1, OWID['total_deaths'].sort_values(ascending=False)[0]),
                xycoords=('axes fraction', 'data'),
                xytext=(-70,1.15),
                textcoords='offset points',
                color='#FF103F',
                fontsize=12,
                fontweight='semibold')
ax2.set_title('COVID-19: WorldWide Deaths', fontsize=15, fontweight='bold')
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax2.grid(linestyle=':',  linewidth=1, color='#DCDCDC')
ax2.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax2.set_yticks([0,1000000, 2000000 , 3000000 , 4000000 , 5000000 , 6000000],            minor=False)
ax2.set_xticks(['2020-01','2020-06','2021-01','2021-06','2022-01','2022-06','2023-01'], minor=False)
ax2.set(xlabel=None)
ax2.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
plt.rcParams['font.family']='sans-serif'
plt.show()
st.pyplot(fig)
st.markdown('''
The world has lost a population of about the size the one that lives in the metropolitan area of Rio de Janeiro,
and about 10% of the worldwide deaths happened in Brazil!
            ''')

st.subheader('Chart 3: Linear Evolution for COVID-19 in Brazil (Cases & Deaths)')
BR = OWID.loc[OWID.location == 'Brazil'].copy()
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12,8), tight_layout=True)
OWID.loc[OWID.location =='Brazil', 'total_cases'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax1     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00',    mfc='#FF8C00')
ax1.annotate('{:,.0f}'.format(BR['total_cases'].sort_values(ascending=False)[0]),
                xy=(1, BR['total_cases'].sort_values(ascending=False)[0]),
                xycoords=('axes fraction', 'data'),
                xytext=(-105,1.15),
                textcoords='offset points',
                color='#FF4500',
                fontsize=12,
                fontweight='semibold')
ax1.set_title('COVID-19: Cases in Brazil', fontsize=15, fontweight='bold')
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax1.grid(linestyle=':',  linewidth=1, color='#DCDCDC')
ax1.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax1.set_yticks([0, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000, 35000000], minor=False)
ax1.set_xticks(['2020-01' ,'2020-06','2021-01','2021-06','2022-01','2022-06','2023-01'], minor=False)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax1.xaxis.set_tick_params(rotation=0)
ax1.set(xlabel=None)
ax1.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
OWID.loc[OWID.location =='Brazil', 'total_deaths'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax2     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F',     mfc='#FF103F')
ax2.annotate('{:,.0f}'.format(BR['total_deaths'].sort_values(ascending=False)[0]),
                xy=(1, BR['total_deaths'].sort_values(ascending=False)[0]),
                xycoords=('axes fraction', 'data'),
                xytext=(-85,1.15),
                textcoords='offset points',
                color='#FF103F',
                fontsize=12,
                fontweight='semibold')
ax2.set_title('COVID-19: Deaths in Brazil', fontsize=15, fontweight='bold')
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
ax2.grid(linestyle=':', linewidth=1, color='#DCDCDC')
ax2.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax2.set_yticks([0,100000 , 200000  , 300000  , 400000  , 500000  , 600000 ],            minor=False)
ax2.set_xticks(['2020-01','2020-06','2021-01','2021-06','2022-01','2022-06','2023-01'], minor=False)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax2.xaxis.set_tick_params(rotation=360)
ax2.set(xlabel=None)
ax2.spines[[ 'top','right',  'left', 'bottom']].set_visible(False)
plt.rcParams['font.family'] ='sans-serif'
plt.show()
st.pyplot(fig)
st.markdown('''
Brazil has always had a history of vaccinations with a National Program of Immunization efficient and effective,
famous for the eradication of polio for which the vaccination campaign _Zé Gotinha_ ('Droplet Joe') mascot was created in 1986 and became a symbol in saving lives.
            ''')
with st.container():
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:st.empty()
    with c2:st.empty()
    with c3:st.image('https://www.gov.br/saude/pt-br/campanhas-da-saude/2023/vacinacao/ze-gotinha/ze-gotinha/@@govbr.institucional.banner/f0ed8b09-fbd2-47b6-b441-d54c6fa4a87b/@@images/201a5721-4a35-4010-a373-c3e89f3399b2.gif', width=250)
    with c4:st.empty()
    with c5:st.empty()
st.markdown('''The following chart makes it cristal clear how the vaccines were very effective in fighting the disease,
so much so the world has pretty much outcome it and life has basically returned to what it used to be in many ways, no more lockdowns and no more masks.
            ''')

st.subheader('Chart 4: Logarithmic Evolution for COVID-19 in Brazil (Vaccination & Cases & Deaths)')
fig , ax = plt.subplots(figsize=(12,8), tight_layout=True)
RAW.loc[RAW.location == 'Brazil','new_vaccinations_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Vaccination',
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#4CAF50',
                linewidth  ='2.25'   ,
                ms=.01, mec='#4CAF50',mfc='#4CAF50')
RAW.loc[RAW.location == 'Brazil','new_cases_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Cases'  ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00', mfc='#FF8C00')
RAW.loc[RAW.location == 'Brazil','new_deaths_smoothed'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                label      ='Deaths' ,
                ax         = ax      ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F',   mfc='#FF103F')
ax.set_title('COVID-19 in Brazil: Vaccination & Cases & Deaths (Log Scale)', fontsize=18, fontweight='bold')
ax.grid(linestyle=':' , linewidth=1  , color='#DCDCDC')
ax.tick_params(axis   ='both',
                which ='both',
                left  = False,
                bottom= False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b'))
ax.xaxis.set_tick_params(rotation=0)
ax.set(xlabel=None)
ax.spines[['top',  'right', 'left', 'bottom']].set_visible(False)
ax.legend(loc='best', fontsize=13)
plt.rcParams[ 'font.family']=    'sans-serif'
plt.yscale(   'log')
plt.show()
st.pyplot(fig)
st.markdown('''
Nonetheless, has any lesson been learned at all? Is the world better equipped to deal with another pandemic?
It was fortunate a vaccine so effective could had been produced somewhat so quickly; lucky may not be around another time.
''')
st.toast('Vaccinate!', icon='💉')
