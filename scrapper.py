import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import os, sys
import base64
import plost
import requests
import io
import xlsxwriter
from io import BytesIO
import altair as alt
from bs4 import BeautifulSoup
import lxml
import json
import BVCscrap  as bvc
import http.client, urllib.request, urllib.parse, urllib.error, base64
import yfinance as yf
from datetime import date
import time
from fake_useragent import UserAgent

#GITHUB READING
# Downloading the csv file from your GitHub
url = "https://raw.githubusercontent.com/Hamza-Alami/scrapperSKB/main/suppscrap.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url).content
# Reading the downloaded content and making it a pandas dataframe
supportsc = pd.read_csv(io.StringIO(download.decode('utf-8')))
#end

lyoum = date.today()
no = lyoum.weekday()

now = dt.now()
ctime = now.strftime("%H:%M")
starttime = '11:45'

last_year = lyoum.year - 1
eoly = date(last_year, 12, 30).strftime('%Y-%m-%d')
edate = lyoum

base_date = st.sidebar.date_input('séléctionner la date de base pour la comparaison des indices et des commodities')
formatted_date2 = base_date.strftime('%Y-%m-%d')

start_date = st.sidebar.date_input('séléctionner la date pour les indices et les commodities')
formatted_date = start_date.strftime('%Y-%m-%d')

we_date = st.sidebar.date_input('séléctionner la fin de semaine pour la comparaison hebdo des indices et des commodities')
formatted_date3 = we_date.strftime('%Y-%m-%d')

if no == 0 :
    sdate = lyoum - datetime.timedelta(days=3)
   
elif no == 1 :
    sdate = lyoum - datetime.timedelta(days=1)
    
else:
    sdate = lyoum - datetime.timedelta(days=1)
    
#bamweek
bamweek = lyoum - datetime.timedelta(days=7)
#

if no < 5 and ctime > starttime:
    selecteddate = lyoum
else:
    selecteddate = '2023-01-02'
#end
    
#threeyrsago = lyoum.replace(year=lyoum.year-3)
oneyrago = lyoum.replace(year=lyoum.year-1)

st.text('Cours de référence BAM')
#Scrapping eur mad and usd mad from BAM
#scrap from BAM
def euromad():
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '4f64d048c9f34f62a748068e3827cbc9',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': selecteddate,
    })
    ####
    paramsprev = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': sdate,
    })
    
    paramsweekly = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': bamweek,
    })
    
    #####
    eurmad3 = 11.1592
    #####
        
    #current day
    
    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        eur = data.decode()
        euro = json.loads(eur)
        euro1 = euro[0]
        eurmad = euro1.get("moyen")
    except Exception as e:
        eurmad = 1
        
    ####
    #previous day

    try:
        conn2 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn2.request("GET", "/cours/Version1/api/CoursVirement?%s" % paramsprev, "{body}", headers)
        response2 = conn2.getresponse()
        data2 = response2.read()
        eur2 = data2.decode()
        conn2.close()
        euro2 = json.loads(eur2)
        euro22 = euro2[0]
        eurmad2 = euro22.get("moyen")
    except Exception as e:
        eurmad2 = 1
        
    ####
    #previous week
    try:
        conn3 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn3.request("GET", "/cours/Version1/api/CoursVirement?%s" % paramsweekly, "{body}", headers)
        response3 = conn3.getresponse()
        data3 = response3.read()
        eur3 = data2.decode()
        conn2.close()
        euro3 = json.loads(eur3)
        euro33 = euro3[0]
        eurmadw = euro33.get("moyen")
    except Exception as e:
        eurmadw = 1
        
    return eurmad, eurmad2, eurmadw, eurmad3

def usdmad():
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '4f64d048c9f34f62a748068e3827cbc9',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'USD',
        'date': selecteddate,
    })
    ####
    params2 = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'USD',
        'date': sdate,
    })
    
    paramsweekly = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'USD',
        'date': bamweek,
    })
    
    #####
    dolmad3 = 10.4477
    #####
    try:
        conn2 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn2.request("GET", "/cours/Version1/api/CoursVirement?%s" % params2, "{body}", headers)
        response2 = conn2.getresponse()
        data2 = response2.read()
        conn2.close()
        usd2 = data2.decode()
        dol2 = json.loads(usd2)
        dol22 = dol2[0]
        dolmad2 = dol22.get("moyen")
    except Exception as e:
        dolmad2 = 1
   
    #####

    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        dataus = response.read()
        conn.close()
        usd = dataus.decode()
        usdt = json.loads(usd)
        usdt1 = usdt[0]
        dollarmad = usdt1.get("moyen")
    except Exception as e:
        dollarmad = 1
        
    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % paramsweekly, "{body}", headers)
        response3 = conn.getresponse()
        dataus3 = response3.read()
        conn.close()
        usd3 = dataus3.decode()
        usdt3 = json.loads(usd3)
        usdt33 = usdt3[0]
        dollarmadweekly = usdt33.get("moyen")
    except Exception as e:
        dollarmadweekly = 1   
        
    return dollarmad, dolmad2, dollarmadweekly, dolmad3

dirhameuro = euromad()
st.write(dirhameuro)
eact = dirhameuro[0]
eprev = dirhameuro[1]
eweek = dirhameuro[2]
eeoy = dirhameuro[3]

dirhamdollar = usdmad()
st.write(dirhamdollar)
dact = dirhamdollar[0]
dprev = dirhamdollar[1]
dweek = dirhamdollar[2]
deoy = dirhamdollar[3]

BAMcc = pd.DataFrame({'Cours en MAD': [eact, dact]},index=['EUR', 'USD'])

varmad = [((eact-eprev)/eprev)*100, ((dact-dprev)/dprev)*100]
vareoy = [((eact-eeoy)/eeoy)*100, ((dact-deoy)/deoy)*100]
varmadweekly = [((eact-eweek)/eweek)*100, ((dact-dweek)/dweek)*100]

BAMcc['var %'] = varmad
BAMcc['var ytd %'] = vareoy
BAMcc['weekly var %'] = varmadweekly

with st.container(): 
    #ratio selection 
    bamselection = st.radio(
     "Quotidien ou Hebdo",
     ('Q', 'H'))
    
    if (bamselection == 'Q') :
        BAMccQ = BAMcc[['Cours en MAD','var %','var ytd %']]
        st.dataframe(BAMccQ)
        
    else :
        BAMccH = BAMcc
        st.dataframe(BAMccH)
        
##END OF BANK AL MAGHRIB TOOL


#Scrap from yahoo finance
#                                       Indices

def indices():
    
    #Dow jones
    dj = yf.download("^DJI", eoly, edate)
    try:   
        dj30 = dj.loc[formatted_date, "Close"]
    except Exception as e:
        dj30 = 1
        
    try: 
        dj30prev = dj.loc[formatted_date2, "Close"]
    except Exception as e:
        dj30prev = 1
    
    try: 
        dj30we = dj.loc[formatted_date3, "Close"]
    except Exception as e:
        dj30we = 1
        
    dj30var = ((dj30-dj30prev)*100)/dj30prev
    dj30wvar = ((dj30-dj30we)*100)/dj30we
    
    #eoy
    djeoye = dj.loc[eoly, "Close"]
    djvarytd = ((dj30-djeoye)*100)/djeoye

    #spoos
    sp = yf.download("^GSPC", eoly, edate)
    try: 
        sp500 = sp.loc[formatted_date, "Close"]
    except Exception as e:
        sp500 = 1
        
    try: 
        sp500prev = sp.loc[formatted_date2, "Close"]
    except Exception as e:
        sp500prev = 1
    
    try: 
        sp500we = sp.loc[formatted_date3, "Close"]
    except Exception as e:
        sp500we = 1
        
    sp500var = ((sp500-sp500prev)*100)/sp500prev
    sp500wvar = ((sp500-sp500we)*100)/sp500we
    
    #eoy
    speoye = sp.loc[eoly, "Close"]
    spvarytd = ((sp500-speoye)*100)/speoye

    #nasdaq
    nas = yf.download("^IXIC", eoly, edate)
    try:
        nasdaq = nas.loc[formatted_date, "Close"]
    except Exception as e:
        nasdaq = 1
        
    try: 
        nasdaqprev = nas.loc[formatted_date2, "Close"]
    except Exception as e:
        nasdaqprev = 1 
    
    try: 
        nasdaqwe = nas.loc[formatted_date3, "Close"]
    except Exception as e:
        nasdaqwe = 1   
    
    nasdaqvar = ((nasdaq-nasdaqprev)*100)/nasdaqprev
    nasdaqwvar = ((nasdaq-nasdaqwe)*100)/nasdaqwe
    
    #eoy
    naseoye = nas.loc[eoly, "Close"]
    nasvarytd = ((nasdaq-naseoye)*100)/naseoye

    #cac40
    cac4 = yf.download("^FCHI", eoly, edate)
    
    try:        
        cac = cac4.loc[formatted_date, "Close"]
    except Exception as e:
        cac = 1
        
    try: 
        cacprev = cac4.loc[formatted_date2, "Close"]
    except Exception as e:
        cacprev = 1   
    
    try: 
        cacwe = cac4.loc[formatted_date3, "Close"]
    except Exception as e:
        cacwe = 1   
    
    cacvar = ((cac-cacprev)*100)/cacprev
    cacwvar = ((cac-cacwe)*100)/cacwe
    #eoy
    caceoye = cac4.loc[eoly, "Close"]
    cacvarytd = ((cac-caceoye)*100)/caceoye

    #DAX
    dax3 = yf.download("^GDAXI", eoly, edate)
    
    try:
        dax = dax3.loc[formatted_date, "Close"]
    except Exception as e:
        dax = 1
    
    try: 
        daxprev = dax3.loc[formatted_date2, "Close"]
    except Exception as e:
        daxprev = 1   
    
    try: 
        daxwe = dax3.loc[formatted_date3, "Close"]
    except Exception as e:
        daxwe = 1   
    
    daxvar = ((dax-daxprev)*100)/daxprev
    daxwvar = ((dax-daxwe)*100)/daxwe
    
    #eoy
    daxeoye = dax3.loc[eoly, "Close"]
    daxvarytd = ((dax-daxeoye)*100)/daxeoye 

    #nikkei
    jp1 = yf.download("^N225", eoly, edate)
    
    try:
        jp = jp1.loc[formatted_date, "Close"]
    except Exception as e:
        jp = 1
        
    try: 
        jpprev = jp1.loc[formatted_date2, "Close"]
    except Exception as e:
        jpprev = 1   
    
    try: 
        jpwe = jp1.loc[formatted_date3, "Close"]
    except Exception as e:
        jpwe = 1   
    
    jpvar = ((jp-jpprev)*100)/jpprev
    jpwvar = ((jp-jpwe)*100)/jpwe
    #eoy
    jpeoye = jp1.loc[eoly, "Close"]
    jpvarytd = ((jp-jpeoye)*100)/jpeoye

    #hangseng
    hk1 = yf.download("^HSI", eoly, edate)
    
    try:     
        hk = hk1.loc[formatted_date, "Close"]
    except Exception as e:
        hk = 1
        
    try: 
        hkprev = hk1.loc[formatted_date2, "Close"]
    except Exception as e:
        hkprev = 1       
    
    try: 
        hkwe = hk1.loc[formatted_date3, "Close"]
    except Exception as e:
        hkwe = 1       
    
    hkvar = ((hk-hkprev)*100)/hkprev
    hkwvar = ((hk-hkwe)*100)/hkwe
    #eoy
    hkeoye = hk1.loc[eoly, "Close"]
    hkvarytd = ((hk-hkeoye)*100)/hkeoye
    
    return dj30, sp500, nasdaq, cac, dax, jp, hk, dj30var, sp500var, nasdaqvar, cacvar, daxvar, jpvar, hkvar, djvarytd, spvarytd, nasvarytd, cacvarytd, daxvarytd, jpvarytd, hkvarytd, dj30wvar, sp500wvar, nasdaqwvar, cacwvar, daxwvar, jpwvar, hkwvar

#                                        Commodities

def commodities():
    #Gold
    gld1 = yf.download("GC=F", eoly, edate)
    try:
        gld = gld1.loc[formatted_date, "Close"]
    except Exception as e:
        gld = 1
        
    try: 
        gldprev = gld1.loc[formatted_date2, "Close"]
    except Exception as e:
        gldprev = 1       
    
    try: 
        gldwe = gld1.loc[formatted_date3, "Close"]
    except Exception as e:
        gldwe = 1       
        
    gldvar = ((gld-gldprev)*100)/gldprev
    goldvarw = ((gld-gldwe)*100)/gldwe
    
    #eoy
    gldeoye = gld1.loc[eoly, "Close"]
    gldvarytd = ((gld/gldeoye)-1)*100

    #Brent    
    oil1 = yf.download("BZ=F", eoly, edate)
    try:
        oil = oil1.loc[formatted_date, "Close"]
    except Exception as e:
        oil = 1
        
    try: 
        oilprev = oil1.loc[formatted_date2, "Close"]
    except Exception as e:
        oilprev = 1       
    
    try: 
        oilwe = oil1.loc[formatted_date3, "Close"]
    except Exception as e:
        oilwe = 1       
        
    oilvar = ((oil-oilprev)*100)/oilprev
    oilvarw = ((oil-oilwe)*100)/oilwe
    
    #eoy
    oileoye = oil1.loc[eoly, "Close"]
    oilvarytd = ((oil/oileoye)-1)*100

    #silver
    silver1 = yf.download("SI=F", eoly, edate)
    try:
        silver = silver1.loc[formatted_date, "Close"]
    except Exception as e:
        silver = 1
        
    try: 
        silverprev = silver1.loc[formatted_date2, "Close"]
    except Exception as e:
        silverprev = 1       
    
    try: 
        silverwe = silver1.loc[formatted_date3, "Close"]
    except Exception as e:
        silverwe = 1       
        
    silvervar = ((silver-silverprev)*100)/silverprev
    silvervarw = ((silver-silverwe)*100)/silverwe
    
    #eoy
    silvereoye = silver1.loc[eoly, "Close"]
    silvervarytd = ((silver/silvereoye)-1)*100
    
    return gld, oil, silver, gldvar, oilvar, silvervar, gldeoye, oileoye, silvereoye, gldvarytd, oilvarytd, silvervarytd, gldwe, oilwe, silverwe, goldvarw, oilvarw, silvervarw

#                                          FX

#calling funcs to lists
indiceslist = indices()
commolist = commodities()

st.write(commolist[6], commolist[7], commolist[8], commolist[9], commolist[10], commolist[11])

#putting data into lists
Cours1 = [indiceslist[0], indiceslist[1], indiceslist[2], indiceslist[3], indiceslist[4], indiceslist[5], indiceslist[6]]
var1 = [indiceslist[7], indiceslist[8], indiceslist[9], indiceslist[10], indiceslist[11], indiceslist[12], indiceslist[13]]

vari = [indiceslist[14], indiceslist[15], indiceslist[16], indiceslist[17], indiceslist[18], indiceslist[19], indiceslist[20]]
varw = [indiceslist[21], indiceslist[22], indiceslist[23], indiceslist[24], indiceslist[25], indiceslist[26], indiceslist[27]]

Cours2 =  [commolist[0], commolist[1], commolist[2]]
var2 =  [commolist[3], commolist[4], commolist[5]]

vari2 =  [commolist[9], commolist[10], commolist[11]]
Coursw2 = [commolist[12], commolist[13], commolist[14]]
varw2 = [commolist[15], commolist[16], commolist[17]]

# dictionary of lists 
dictin = {'Cours': Cours1, 'var %': var1}
dictin2 = {'Cours': Cours2, 'var %': var2}

FXCOM = pd.DataFrame(dictin2,index=['Gold','Brent','Silver'])
FXCOM['var ytd %'] = vari2
FXCOM['Cours j-7'] = Coursw2
FXCOM['var weekly %'] = varw2

intlindices = pd.DataFrame(dictin,index=['Dow Jones','S&P500', 'Nasdaq', 'CAC40', 'DAX30', 'NIKKEI','Hang Seng'])
intlindices['var ytd %'] = vari
intlindices['var weekly %'] = varw

st.text('FX & commodities')

st.text('Indices internationaux')

if (bamselection == 'Q') :
    intlindicesQ = intlindices[['Cours','var %','var ytd %']]
    FXCOMQ = FXCOM[['Cours','var %','var ytd %']]
    st.dataframe(intlindicesQ)
    st.dataframe(FXCOMQ)
        
else :
    st.dataframe(intlindices)
    st.dataframe(FXCOM)

#Scraping stock data from le Boursier 
              
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response_API = requests.get('https://medias24.com/content/api?method=getAllStocks&format=json', headers=headers)
x = response_API.content

y = json.loads(x)
z = y['result']
trntrn = z[0]
        
seance = []
for i, val in enumerate(z):
    sep = ' '
    stripped = val["datetime"].split(sep, 1)[0]
    seance.append({'Ticker': val["name"],'Cours': val["cours"], 'Cloture': val["cloture"],'Variation': val["variation"], 'Volume Titre': val["volumeTitre"],"derniere transaction" : stripped})
    fulldf = pd.DataFrame(seance)
    
fulldf['derniere transaction'] = pd.to_datetime(fulldf['derniere transaction'], infer_datetime_format=True)

fulldf['derniere transaction'] = fulldf['derniere transaction'].dt.date

tradedtoday = fulldf['derniere transaction'] < lyoum
fulldf.loc[tradedtoday, 'Volume Titre'] = 0
fulldf.loc[tradedtoday, 'Variation'] = 0

#renaming for merge
fulldf.rename(columns = {'Ticker':'Scrappername'}, inplace = True)

#merging
df_merge_col = pd.merge(fulldf, supportsc, on='Scrappername')

#cleaning and calculating
df_merge_col['Cloture'] = df_merge_col['Cloture'].apply(lambda x: x.replace(" ", ""))
df_merge_col['Cours'] = df_merge_col['Cours'].astype(float)
df_merge_col['Variation'] = df_merge_col['Variation'].astype(float)
df_merge_col['Volume Titre'] = df_merge_col['Volume Titre'].astype(float)
df_merge_col['Nombre de titres'] = df_merge_col['Volume Titre'].astype(float)
df_merge_col['Var Ytd'] = ((df_merge_col['Cours']-df_merge_col['COURS AU 31/12/2022'])*100)/df_merge_col['COURS AU 31/12/2022']
df_merge_col['Capitalisation'] = (df_merge_col['Cours']*df_merge_col['NofS'])

FinalDF = df_merge_col[['soge', 'TICKER','Cours', 'Variation', 'Var Ytd', 'Volume Titre', 'Capitalisation']]

mapping = {'StÃ© Boissons du Maroc': 'Sté Boissons du Maroc',
           'CrÃ©dit Du Maroc': 'Crédit du Maroc',
           'OulmÃ¨s': 'Oulmès',
           'Maghreb OxygÃ¨ne':'Maghreb Oxygène'
          }

FinalDF.soge = FinalDF.soge.replace(mapping, regex=True)
st.write(FinalDF)


#iIndex hsit

masi1=bvc.loadata('MASI',start=oneyrago,end=lyoum)
msi20=bvc.loadata('MSI20',start=oneyrago,end=lyoum)

# Get today's date
today = datetime.datetime.now().date()

#date fr
# Get the day of the week as an integer (Monday is 0, Tuesday is 1, etc.)
day_of_week = today.weekday()

# Define a list of days of the week in French
days_of_week_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Print today's date and day of the week in French
aujd = (days_of_week_fr[day_of_week], today.strftime("%d/%m/%Y"))
data0 = [[aujd[0], aujd[1]]]
aujddf = pd.DataFrame(data0, columns=['Jour', 'Date'])
st.write(aujddf)
###

#empty sheets temporary
dfindex = pd.DataFrame()
voldf = pd.DataFrame()

#to excel sheets
buffer = io.BytesIO()

# Create a Pandas Excel writer using XlsxWriter as the engine.

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    
    # Write each dataframe to a different worksheet.
    BAMcc.to_excel(writer, sheet_name='Cours de change BAM')
    FXCOM.to_excel(writer, sheet_name='FX & commodities')
    intlindices.to_excel(writer, sheet_name='Indices internationaux')
    dfindex.to_excel(writer, sheet_name='Indices BVC')
    FinalDF.to_excel(writer, sheet_name='Cours & Variations')
    voldf.to_excel(writer, sheet_name='Volume global')
    masi1.to_excel(writer, sheet_name='Masi Hist 1YR')
    msi20.to_excel(writer, sheet_name='Msi20 Hist 1YR')
    aujddf.to_excel(writer, sheet_name='Date')

    # Close the Pandas Excel writer and output the Excel file to the buffer
    
    writer.close()

    st.download_button(
        label="Scrap and download data",
        data=buffer,
        file_name="ds.xlsx"
    )
