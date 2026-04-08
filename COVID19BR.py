# Libraries:
import      numpy          as np
import     pandas          as pd
import  streamlit          as st
import matplotlib.gridspec as gs
import matplotlib.pyplot   as plt
import matplotlib.ticker   as ticker
import matplotlib.dates    as mdates
import    seaborn          as sns
import   datetime
# Configurations:
pd.options.plotting.matplotlib.register_converters=True
pd.options.display.max_columns         =           None
plt.rcParams[  'figure.autolayout']    =           True
plt.rcParams[    'font.family']        =                                        'sans-serif'
sns.set_theme(context='notebook', style='whitegrid', palette='colorblind', font='sans-serif', font_scale=1.15, color_codes=True, rc={'grid.color':'1','grid.linestyle':':'})
st.set_page_config(page_title='COVID19BR', page_icon='😷', layout='wide', initial_sidebar_state='collapsed')
# DATA:
#         'https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv'
#         'https://github.com/owid/covid-19-data/raw/refs/heads/master/public/data/owid-covid-data-old.csv'
#         'https://github.com/owid/covid-19-data/raw/refs/heads/master/public/data/jhu/COVID-19%20-%20Johns%20Hopkins%20University.csv'
DATA     ='https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv'

@st.cache_data
def LoadData( ):
    data =pd.read_csv(DATA, parse_dates=['date'])
   # Selecting Columns:
    df   =data[  ['date',
                  'country',
                  'new_cases',
                  'new_deaths',
                  'new_vaccinations',
                  'new_cases_smoothed',
                  'new_deaths_smoothed',
                  'new_vaccinations_smoothed',
                  'total_cases' ,
                  'total_deaths',
                  'total_vaccinations']].copy( )
    df.set_index ('date',inplace=True)
    df.sort_index(       inplace=True)
    return df
RAW       =LoadData( )
# Filling Missing Data:
X         =RAW.copy( ) 
num       =X.select_dtypes(include=['number']).columns
X[num]    =X[num].fillna(0)
nan       =X.select_dtypes(exclude=['number']).columns
X[nan]    =X[nan].fillna('np.nan')
OWID      =X.copy( )
BR        =OWID.loc[OWID.country=='Brazil'].copy( )
# SIDE:
st.sidebar.title    ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.divider  (                     )
st.sidebar.header   ('COVID-19 in Brazil' )
st.sidebar.subheader('Data Analysis'      )
st.sidebar.divider  (                     )
st.sidebar.markdown ('''Source:    [Our World in Data](https://github.com/owid/covid-19-data)''')
st.sidebar.write    ('OWID daily reports from {} to {}'.format(RAW.index.min( ), RAW.index.max( )))
st.sidebar.markdown ('''Reference: [Data Cleaning Techniques in Python: the Ultimate Guide](https://www.justintodata.com/data-cleaning-techniques-python-guide/)''')
st.sidebar.divider  (                       )
st.sidebar.markdown ('''
![2023.11.23   ](https://img.shields.io/badge/2023.11.23-000000)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2025&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.divider (                    )
st.title   ('COVID-19 in Brazil')
st.divider (                    )
st.markdown('''
Brazil is the fifth largest country in the world and the seventh in population with over 200 million inhabitants.
When COVID-19 outbreak begun on the eve of 2020; and even though the first case in the country had been registered at the end of February,
with the first death coming the following month, fifteen days later, the country had been relatively 'safe' during the first semester of 2020.
Signs of how it was going to deal with the outbreak though were less hopeful. A month into 'lockdown' the then Minister of Health,
a physician, was fired by the then President because the Minister was trying to keep the population safe from the pandemic,
following the World Health Organization (WHO) directives. The then President, however, was against it, saying it would damage the economy.
From there on the then President became the _de facto_ Minister of Health, instating new ministers that would only 'follow orders',
diminishing the disease and discrediting vaccines.
            ''')

st.subheader('Chart 1: Top 5 Countries with most Deaths')
filter = OWID.index[OWID['total_deaths']!=0.][-1]
deaths = OWID.loc[filter].sort_values(by ='total_deaths', ascending=False)
rows   = deaths.loc[(deaths['country']  =='United States')|(deaths['country']=='Brazil')|(deaths['country']=='India')|(deaths['country']=='Russia')|(deaths['country']=='Mexico')]
top    =             rows.sort_values(by ='total_deaths', ascending=False)
fig,ax = plt.subplots(figsize=(12,6), tight_layout=True)
sns.barplot(x='country',   y='total_deaths', data=top, ax=ax, hue='country', palette='autumn', saturation=.75, legend=False)
ax.set_title('COVID-19: Top 5 Countries with Most Deaths', fontsize=20, fontweight='bold')
for spine in ['top','right','left','bottom']:ax.spines[spine].set_visible(False)
plt.gca( ).axes.get_yaxis( ).set_visible(False)
plt.gca( ).axes.get_xaxis( ).set_visible(True)
for tick in ax.get_xticklabels( ):
    tick.set_fontweight('semibold')
    tick.set_fontsize    (15)
plt.tick_params(axis  = 'both',
                which = 'both',
                bottom=  False)
for c in ax.containers:
    values = top.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=13, padding=10, fontweight='semibold')
ax.set(xlabel=None)
st.pyplot(fig)
st.markdown('''
The consequences could not have been more sinister. Brazil has become the country with the second highest death toll,
only behind the United States. A death toll rate that was almost twice the worldwide rate of 1% of deaths from registered cases.
            ''')

st.subheader('Chart 2: Linear Evolution for COVID-19 WorldWide (Cases & Deaths)')
fig,(ax1,ax2)=plt.subplots(nrows=2, ncols=1, figsize=(12,6), tight_layout=True)
RAW.loc[RAW.country=='World','total_cases'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax1     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00', mfc='#FF8C00')
ax1.annotate('{:,.0f}'.format(RAW['total_cases'].sort_values(ascending=False).iloc[0]),
                xy=( 1,       RAW['total_cases'].sort_values(ascending=False).iloc[0]),
                xycoords  =('axes fraction','data'),
                xytext    =(-85, 1.15),
                textcoords='offset points',
                color     ='#FF4500',
                fontsize  =    13   ,
                fontweight='semibold')
ax1.set_title('COVID-19: WorldWide Cases', fontsize=15, fontweight='bold')
ax1.grid(linestyle=':', linewidth=1, color='#DCDCDC'  , mouseover = True )
ax1.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax1.set_yticks([0, 1e8, 2e8, 3e8, 4e8, 5e8, 6e8], minor=False)
# ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# ax1.xaxis.set_major_formatter(mdates.DateFormatter     ('%Y\n%b'))
# ax1.xaxis.set_tick_params(rotation=0)
ax1.set(xlabel=None)
ax1.spines[['top','right','left','bottom'] ].set_visible(          False)
RAW.loc[RAW.country=='World','total_deaths'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax2     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F', mfc='#FF103F')
ax2.annotate('{:,.0f}'.format(RAW['total_deaths'].sort_values(ascending=False).iloc[0]),
                xy=( 1,       RAW['total_deaths'].sort_values(ascending=False).iloc[0]),
                xycoords  =('axes fraction','data'),
                xytext    =(-70,1.15),
                textcoords='offset points',
                color     ='#FF103F',
                fontsize  =    13   ,
                fontweight='semibold')
ax2.set_title('COVID-19: WorldWide Deaths', fontsize=15, fontweight='bold')
ax2.grid(linestyle=':', linewidth=1,  color='#DCDCDC'  , mouseover = True )
ax2.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax2.set_yticks([0, 1e6, 2e6, 3e6, 4e6, 5e6, 6e6], minor=False)
# ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# ax2.xaxis.set_major_formatter(mdates.DateFormatter     ('%Y\n%b'))
# ax2.xaxis.set_tick_params(rotation=360)
ax2.set(xlabel=None)
ax2.spines[['top','right','left','bottom']].set_visible(False)
st.pyplot(fig)

W =OWID.loc[OWID[        'country']=='World'].copy (  )
D =   W.index[W [      'new_deaths_smoothed']!=0.0][-1].strftime('%d %b %Y')
C =   W.index[W [       'new_cases_smoothed']!=0.0][-1].strftime('%d %b %Y')
V =   W.index[W ['new_vaccinations_smoothed']!=0.0][-1].strftime('%d %b %Y')
# st.write('• Last       death entry on the dataset for the World: {}'.format(D))
# st.write('• Last        case entry on the dataset for the World: {}'.format(C))
# st.write('• Last vaccination entry on the dataset for the World: {}'.format(V))

st.markdown('''
The world has lost a population about the size the one that lives in the metropolitan area of Rio de Janeiro;
about {}% of those deaths happened in Brazil!
            '''.format(round(((BR['total_deaths'].sort_values(ascending=False).iloc[0])/(RAW['total_deaths'].sort_values(ascending=False).iloc[0]))*100)), 2)

st.subheader('Chart 3: Linear Evolution for COVID-19 in Brazil (Cases & Deaths)')
fig,(ax1,ax2)=plt.subplots(nrows=2, ncols=1, figsize=(12,6), tight_layout= True)
OWID.loc[OWID.country=='Brazil','total_cases'].sort_values      (ascending=False).plot(
                kind       ='line'   ,
                ax         = ax1     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF8C00',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF8C00', mfc='#FF8C00')
ax1.annotate('{:,.0f}'.format(BR['total_cases'].sort_values(ascending=False).iloc[0]),
                xy=( 1,       BR['total_cases'].sort_values(ascending=False).iloc[0]),
                xycoords  =('axes fraction','data'),
                xytext    =(-105,1.15),
                textcoords='offset points',
                color     ='#FF4500',
                fontsize  =    13   ,
                fontweight='semibold')
ax1.set_title('COVID-19: Cases in Brazil', fontsize=15, fontweight='bold')
ax1.grid(linestyle=':', linewidth=1, color='#DCDCDC'  , mouseover = True )
ax1.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax1.set_yticks([0, 5e6, 1e7, 1.5e7, 2e7, 2.5e7, 3e7, 3.5e7],    minor=False)
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# ax1.xaxis.set_major_formatter(mdates.DateFormatter     ('%Y\n%b'))
# ax1.xaxis.set_tick_params(rotation=0)
ax1.set(xlabel=None)
ax1.spines[['top','right','left','bottom']    ].set_visible          (False)
OWID.loc[OWID.country=='Brazil','total_deaths'].sort_values(ascending=False).plot(
                kind       ='line'   ,
                ax         = ax2     ,
                marker     ='o'      ,
                linestyle  ='solid'  ,
                color      ='#FF103F',
                linewidth  ='2.25'   ,
                ms=.01, mec='#FF103F', mfc='#FF103F')
ax2.annotate('{:,.0f}'.format(BR['total_deaths'].sort_values(ascending=False).iloc[0]),
                xy=( 1,       BR['total_deaths'].sort_values(ascending=False).iloc[0]),
                xycoords  =('axes fraction','data'),
                xytext    =(-85,1.15),
                textcoords='offset points',
                color     ='#FF103F',
                fontsize  =    13   ,
                fontweight='semibold')
ax2.set_title('COVID-19: Deaths in Brazil', fontsize=15, fontweight='bold')
ax2.grid(linestyle=':', linewidth=1, color='#DCDCDC'   , mouseover = True )
ax2.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
ax2.set_yticks([0,      1e5,   2e5, 3e5,   4e5, 5e5,   6e5], minor=False)
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
#ax2.xaxis.set_major_formatter(mdates.DateFormatter     ('%Y\n%b'))
#ax2.xaxis.set_tick_params(rotation=360)
ax2.set(xlabel=None)
ax2.spines[['top','right','left','bottom']].set_visible(False)
st.pyplot  (fig)
st.markdown('''
Brazil has always had a history of vaccinations with a National Immunization Program efficient and effective,
famous for the eradication of polio for which the vaccination campaign _Zé Gotinha_ ('Droplet Joe') mascot was created in 1986 and became a symbol in saving lives.
            ''')
with st.container( ):
    Cols      =  st.columns(3)
    with Cols[0]:st.empty  ( )
    with Cols[1]:st.image('https://www.gov.br/saude/pt-br/campanhas-da-saude/2023/vacinacao/ze-gotinha/ze-gotinha/@@govbr.institucional.banner/f0ed8b09-fbd2-47b6-b441-d54c6fa4a87b/@@images/201a5721-4a35-4010-a373-c3e89f3399b2.gif', width=250)
    with Cols[2]:st.empty  ( )
st.markdown('''
The following chart makes it cristal clear how the vaccines were very effective in fighting the disease,
so much so the world has pretty much outcome it and life has basically resumed to what it used to be in many ways with no more lockdowns or masks.
            ''')

st.subheader('Chart 4: Logarithmic Evolution for COVID-19 in Brazil (Vaccination & Cases & Deaths)')
x=BR[BR['new_vaccinations_smoothed']!=0.]
y=BR[BR[       'new_cases_smoothed']!=0.]
z=BR[BR[      'new_deaths_smoothed']!=0.]
fig,ax=plt.subplots(figsize=(12,6), tight_layout=True)
x['new_vaccinations_smoothed'].plot(
                kind       ='line'    ,
                label      ='Vaccination',
                ax         = ax       ,
                marker     ='o'       ,
                linestyle  ='solid'   ,
                color      ='#4CAF50' ,
                linewidth  ='2.25'    ,
                ms=.01, mec='#4CAF50' , mfc='#4CAF50')
y['new_cases_smoothed'].plot(
                kind       ='line'    ,
                label      ='Cases'   ,
                ax         = ax       ,
                marker     ='o'       ,
                linestyle  ='solid'   ,
                color      ='#FF8C00' ,
                linewidth  ='2.25'    ,
                ms=.01, mec='#FF8C00' , mfc='#FF8C00')
z['new_deaths_smoothed'].plot(
                kind       ='line'    ,
                label      ='Deaths'  ,
                ax         = ax       ,
                marker     ='o'       ,
                linestyle  ='solid'   ,
                color      ='#FF103F' ,
                linewidth  ='2.25'    ,
                ms=.01, mec='#FF103F' , mfc='#FF103F')
ax.set_title('COVID in Brazil: Vaccination & Cases & Deaths', fontsize=18, fontweight='bold')
ax.grid(linestyle=':' , linewidth=1  , color='#DCDCDC')
ax.tick_params(axis   ='both',
                which ='both',
                left  = False,
                bottom= False)
ax.set(xlabel=None)
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.legend(loc='best', fontsize=13, frameon=False)
plt.gca( ).set_ylim(    bottom=10**0)
plt.gca( ).set_xlim(      left=None )
plt.yscale ('log')
st.pyplot   (fig)

d =  BR.index[BR[      'new_deaths_smoothed']!=0.][-1].strftime('%d %b %Y')
c =  BR.index[BR[       'new_cases_smoothed']!=0.][-1].strftime('%d %b %Y')
v =  BR.index[BR['new_vaccinations_smoothed']!=0.][-1].strftime('%d %b %Y')
# st.write('• Last       death entry on the dataset for Brazil: {}'.format(d))
# st.write('• Last        case entry on the dataset for Brazil: {}'.format(c))
# st.write('• Last vaccination entry on the dataset for Brazil: {}'.format(v))
st.markdown('''
Vaccinations have been ongoing but perhaps not reported anymore, as well as some cases.
Deaths indeed seems to have, fortunantelly, pretty much ended. Nonetheless, has any lesson been learned at all? Is the world better equipped to deal with another pandemic?
It was fortunate a vaccine so effective could had been produced somewhat so quickly; lucky may not be around another time.
            ''')
st.divider(    )
st.toast('Vaccinate!', icon='💉')
