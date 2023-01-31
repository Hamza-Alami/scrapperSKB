import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import os
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

if no == 0 :
    sdate = lyoum - datetime.timedelta(days=3)
    prevdate = lyoum - datetime.timedelta(days=4)
elif no == 1 :
    sdate = lyoum - datetime.timedelta(days=2)
    prevdate = lyoum - datetime.timedelta(days=4)
else:
     sdate = lyoum - datetime.timedelta(days=1)
     prevdate = lyoum - datetime.timedelta(days=2)

if no < 5 and ctime > starttime:
    selecteddate = lyoum
else:
    selecteddate = '2023-01-02'   
    
threeyrsago = lyoum.replace(year=lyoum.year-3)
oneyrago = lyoum.replace(year=lyoum.year-1)

st.text('Cours de référence BAM')
#Scrapping eur mad and usd mad from BAM
#scrap from BAM

'''
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
    params2 = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': sdate,
    })
  
    #####
    eurmad3 = 11.1592
    #####
    try:
        conn2 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn2.request("GET", "/cours/Version1/api/CoursVirement?%s" % params2, "{body}", headers)
        response2 = conn2.getresponse()
        data2 = response2.read()
        conn2.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    eur2 = data2.decode()
    euro2 = json.loads(eur2)
    #euro22 = euro2[0]
    eurmad2 = 11.0548 #euro22.get("moyen")
    ####

    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    eur = data.decode()
    euro = json.loads(eur)
    euro1 = euro[0]
    eurmad = euro1.get("moyen")
    return eurmad, eurmad2, eurmad3

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
    
    #####
    dolmad3 = 10.4477
    #####
    try:
        conn2 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn2.request("GET", "/cours/Version1/api/CoursVirement?%s" % params2, "{body}", headers)
        response2 = conn2.getresponse()
        data2 = response2.read()
        conn2.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    usd2 = data2.decode()
    dol2 = json.loads(usd2)
    #dol22 = dol2[0]
    dolmad2 = 10.1355 #dol22.get("moyen")
    #####

    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        dataus = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    usd = dataus.decode()
    usdt = json.loads(usd)
    usdt1 = usdt[0]
    dollarmad = usdt1.get("moyen")
    return dollarmad, dolmad2, dolmad3

dirhameuro = euromad()
st.write(dirhameuro)
eact = dirhameuro[0]
eprev = dirhameuro[1]
eeoy = dirhameuro[2]

dirhamdollar = usdmad()
st.write(dirhamdollar)
dact = dirhamdollar[0]
dprev = dirhamdollar[1]
deoy = dirhamdollar[2]
BAMcc = pd.DataFrame({'Cours en MAD': [eact, dact]},index=['EUR', 'USD'])

varmad = [((eact-eprev)/eact)*100, ((dact-dprev)/dact)*100]
vareoy = [((eact-eeoy)/eact)*100, ((dact-deoy)/dact)*100]
BAMcc['var %'] = varmad
BAMcc['var ytd %'] = vareoy
st.dataframe(BAMcc)
'''

#Scrap from yahoo finance

#                                        Indices
        
edate = lyoum

def indices():
    
    #Dow jones
    dj = yf.download("^DJI", prevdate, edate)
    dj30 = dj.Close[1]
    dj30var = ((dj30-dj.Close[0])*100)/dj.Close[0]
    #eoy
    djeoy = yf.download("^DJI", "2022-12-30", "2022-12-31")
    djeoye = djeoy.Close[0]
    djvarytd = ((dj30-djeoye)*100)/djeoye


    #spoos
    sp = yf.download("^GSPC", prevdate, edate)
    sp500 = sp.Close[1]
    sp500var = ((sp500-sp.Close[0])*100)/sp.Close[0]
    #eoy
    speoy = yf.download("^GSPC", "2022-12-30", "2022-12-31")
    speoye = speoy.Close[0]
    spvarytd = ((sp500-speoye)*100)/speoye

    #nasdaq
    nas = yf.download("^IXIC", prevdate, edate)
    nasdaq = nas.Close[1]
    nasdaqvar = ((nasdaq-nas.Close[0])*100)/nas.Close[0]
    #eoy
    naseoy = yf.download("^IXIC", "2022-12-30", "2022-12-31")
    naseoye = naseoy.Close[0]
    nasvarytd = ((nasdaq-naseoye)*100)/naseoye

    #cac40
    cac4 = yf.download("^FCHI", prevdate, edate)
    cac = cac4.Close[1]
    cacvar = ((cac-cac4.Close[0])*100)/cac4.Close[0]
    #eoy
    caceoy = yf.download("^FCHI", "2022-12-30", "2022-12-31")
    caceoye = naseoy.Close[0]
    cacvarytd = ((cac-caceoye)*100)/caceoye

    #DAX
    dax3 = yf.download("^GDAXI", prevdate, edate)
    dax = dax3.Close[1]
    daxvar = ((dax-dax3.Close[0])*100)/dax3.Close[0]
    #eoy
    daxeoy = yf.download("^GDAXI", "2022-12-30", "2022-12-31")
    daxeoye = daxeoy.Close[0]
    daxvarytd = ((dax-daxeoye)*100)/daxeoye

    #nikkei
    jp1 = yf.download("^N225", prevdate, edate)
    jp = jp1.Close[1]
    jpvar = ((jp-jp1.Close[0])*100)/jp1.Close[0]
    #eoy
    jpeoy = yf.download("^N225", "2022-12-30", "2022-12-31")
    jpeoye = jpeoy.Close[0]
    jpvarytd = ((jp-jpeoye)*100)/jpeoye

    #hangseng
    hk1 = yf.download("^HSI", prevdate, edate)
    hk = hk1.Close[1]
    hkvar = ((hk-hk1.Close[0])*100)/hk1.Close[0]
    #eoy
    hkeoy = yf.download("^HSI", "2022-12-30", "2022-12-31")
    hkeoye = hkeoy.Close[0]
    hkvarytd = ((hk-hkeoye)*100)/hkeoye
    
    return dj30, sp500, nasdaq, cac, dax, jp, hk, dj30var, sp500var, nasdaqvar, cacvar, daxvar, jpvar, hkvar, djeoye, speoye, naseoye, caceoye, daxeoye, jpeoye, hkeoye, djvarytd, spvarytd, nasvarytd, cacvarytd, daxvarytd, jpvarytd, hkvarytd

#                                        Commodities

def commodities():
    #Gold
    gld1 = yf.download("GC=F", prevdate, edate)
    gld = gld1.Close[1]
    gldvar = ((gld-gld1.Close[0])*100)/gld1.Close[0]
    #eoy
    gldeoy = yf.download("GC=F", "2022-12-30", "2022-12-31")
    gldeoye = gldeoy.Close[0]
    gldvarytd = ((gld/gldeoye)*100)/gldeoye

    #Brent
    oil1 = yf.download("BZ=F", prevdate, edate)
    oil = oil1.Close[1]
    oilvar = ((oil/oil1.Close[0])*100)/oil1.Close[0]
    #eoy
    oileoy = yf.download("BZ=F", "2022-12-30", "2022-12-31")
    oileoye = oileoy.Close[0]
    oilvarytd = ((oil-oileoye)*100)/oileoye

    #silver
    silver1 = yf.download("SI=F", prevdate, edate)
    silver = silver1.Close[0]
    silvervar = ((silver-silver1.Close[0])*100)/silver1.Close[0]
    #eoy
    silvereoy = yf.download("SI=F", "2022-12-30", "2022-12-31")
    silvereoye = silvereoy.Close[0]
    silvervarytd = ((silver-silvereoye)*100)/silvereoye
    
    return gld, oil, silver, gldvar, oilvar, silvervar, gldeoye, oileoye, silvereoye, gldvarytd, oilvarytd, silvervarytd

#                                          FX


#eurodollar
eurusd1 = yf.download("EURUSD=X", sdate, edate)
eurusd = eurusd1.Close[1]
#eoy
eurusdeoy = yf.download("EURUSD=X", "2022-12-30", "2022-12-31")
eurusdeoye = eurusdeoy.Close[0]

eurusdvarytd = ((eurusd-eurusdeoye)*100)/eurusdeoye
eurusdvar = ((eurusd-eurusd1.Close[0])*100)/eurusd1.Close[0]

#calling funcs to lists
indiceslist = indices()
commolist = commodities()

#putting data into lists
Cours1 = [indiceslist[0], indiceslist[1], indiceslist[2], indiceslist[3], indiceslist[4], indiceslist[5], indiceslist[6]]
var1 = [indiceslist[7], indiceslist[8], indiceslist[9], indiceslist[10], indiceslist[11], indiceslist[12], indiceslist[13]]

vari = [indiceslist[21], indiceslist[21], indiceslist[22], indiceslist[23], indiceslist[24], indiceslist[25], indiceslist[26]]

Cours2 =  [eurusd, commolist[1], commolist[0], commolist[2]]
var2 =  [eurusdvar, commolist[3], commolist[4], commolist[5]]

vari2 =  [eurusdvarytd, commolist[9], commolist[10], commolist[11]]

# dictionary of lists 
dictin = {'Cours': Cours1, 'var %': var1}
dictin2 = {'Cours': Cours2, 'var %': var2}

FXCOM = pd.DataFrame(dictin2,index=['EUR/USD','Brent', 'Gold', 'Silver'])
FXCOM['var ytd %'] = vari2

intlindices = pd.DataFrame(dictin,index=['Dow Jones','S&P500', 'Nasdaq', 'CAC40', 'DAX30', 'NIKKEI','Hang Seng'])
intlindices['var ytd %'] = vari

st.text('FX & commodities')
st.dataframe(FXCOM)

st.text('Indices internationaux')
st.write(indices())
st.dataframe(intlindices)

#BVCscrapper

#loading indices

#indices
index=bvc.getIndex()
dfindex = pd.DataFrame(index['Resume indice']).transpose()

#sectorial
dfsect = pd.DataFrame(index['Indices sectoriels']).transpose()

st.text('Indices BVC')

dfindex['Var %'] = dfindex['Var %'].apply(lambda x: x.replace(" %", ""))
dfindex['Var % 31/12'] = dfindex['Var % 31/12'].apply(lambda x: x.replace(" %", ""))
dfindex['Var % 31/12'] = dfindex['Var % 31/12'].apply(lambda x: x.replace(",", "."))
dfindex['Var %'] = dfindex['Var %'].apply(lambda x: x.replace(",", "."))

dfindex['Var % 31/12'] = pd.to_numeric(dfindex['Var % 31/12'], errors='coerce')
dfindex['Var %'] = pd.to_numeric(dfindex['Var %'], errors='coerce')

dfindex['Var %'] = dfindex['Var %'].fillna(0)
dfindex['Var % 31/12'] = dfindex['Var % 31/12'].fillna(0)

st.dataframe(dfindex)

st.text('Indices sectoriaux')
dfsect['Var%'] = dfsect['Var%'].apply(lambda x: x.replace(" %", ""))
dfsect['Var% 31/12'] = dfsect['Var% 31/12'].apply(lambda x: x.replace(" %", ""))
dfsect['Var% 31/12'] = dfsect['Var% 31/12'].apply(lambda x: x.replace(",", "."))
dfsect['Var%'] = dfsect['Var%'].apply(lambda x: x.replace(",", "."))

dfsect['Var% 31/12'] = pd.to_numeric(dfsect['Var% 31/12'], errors='coerce')
dfsect['Var%'] = pd.to_numeric(dfsect['Var%'], errors='coerce')

dfsect['Var%'] = dfsect['Var%'].fillna(0)
dfsect['Var% 31/12'] = dfsect['Var% 31/12'].fillna(0)

st.dataframe(dfsect)

#Pondération et cours
courspond = pd.DataFrame(bvc.getPond())
#st.dataframe(courspond)

#test
st.text('Volume de la séance :')
recap=bvc.getIndexRecap()
st.write(recap['Volume Global'])

#Scraping stock data from le Boursier 

response_API = requests.get('https://medias24.com/content/api?method=getAllStocks&format=json')
x = response_API.content
y = json.loads(x)
z = y['result']
trntrn = z[0]
    
seance = []
for i, val in enumerate(z):
    sep = ' '
    stripped = val["datetime"].split(sep, 1)[0]
    #val["datetime"] = dt.strptime(val["datetime"],  '%y%m%d %H%M%S.%f')
    seance.append({'Ticker': val["name"],'Cours': val["cours"], 'Cloture': val["cloture"],'Variation': val["variation"], 'Volume Titre': val["volumeTitre"],"derniere transaction" : stripped})
    fulldf = pd.DataFrame(seance)
    
fulldf['derniere transaction'] = pd.to_datetime(fulldf['derniere transaction'], infer_datetime_format=True)

fulldf['derniere transaction'] = fulldf['derniere transaction'].dt.date

tradedtoday = fulldf['derniere transaction'] < lyoum
fulldf.loc[tradedtoday, 'Volume Titre'] = 0
fulldf.loc[tradedtoday, 'Variation'] = 0

#renaming for merge
fulldf.rename(columns = {'Ticker':'Scrappername'}, inplace = True)
courspond.rename(columns = {'Instrument':'BVC'}, inplace = True)
courspond.rename(columns = {'Cours':'Cours BVC'}, inplace = True)

#merging
df_merge_col = pd.merge(fulldf, supportsc, on='Scrappername')
df_merge_2 = pd.merge(courspond, df_merge_col, on='BVC')

df_merge_2['Cloture'] = df_merge_2['Cloture'].apply(lambda x: x.replace(" ", ""))

df_merge_2['Cours'] = df_merge_2['Cours'].astype(float)
df_merge_2['Variation'] = df_merge_2['Variation'].astype(float)
df_merge_2['Volume Titre'] = df_merge_2['Volume Titre'].astype(float)
df_merge_2['Nombre de titres'] = df_merge_2['Volume Titre'].astype(float)
df_merge_2['Var Ytd'] = ((df_merge_2['Cours']-df_merge_2['COURS AU 31/12/2022'])*100)/df_merge_2['COURS AU 31/12/2022']

df_merge_2['Capitalisation'] = (df_merge_2['Cours']*df_merge_2['NofS'])
FinalDF = df_merge_2[['soge', 'TICKER','Cours', 'Variation', 'Var Ytd', 'Volume Titre', 'Capitalisation']]

st.write(FinalDF)


masi1=bvc.loadata('MASI',start=oneyrago,end=lyoum)
masi3=bvc.loadata('MASI',start=threeyrsago,end=lyoum)

#to excel sheets
buffer = io.BytesIO()

# Create a Pandas Excel writer using XlsxWriter as the engine.

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    
    # Write each dataframe to a different worksheet.
    #BAMcc.to_excel(writer, sheet_name='Cours de change BAM')
    FXCOM.to_excel(writer, sheet_name='FX & commodities')
    intlindices.to_excel(writer, sheet_name='Indices internationaux')
    dfindex.to_excel(writer, sheet_name='Indices BVC')
    dfsect.to_excel(writer, sheet_name='Indices sectoriaux')
    FinalDF.to_excel(writer, sheet_name='Cours & Variations')
    masi1.to_excel(writer, sheet_name='Masi Hist 1YR')
    masi3.to_excel(writer, sheet_name='Masi Hist 3YR')


    # Close the Pandas Excel writer and output the Excel file to the buffer
    
    writer.save()

    st.download_button(
        label="Scrap and download data",
        data=buffer,
        file_name="ds.xlsx"
    )
