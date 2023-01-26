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

lyoum = date.today()
no = lyoum.weekday()

now = dt.now()
ctime = now.strftime("%H:%M")
starttime = '11:45'
EOY = '30-12-2022'

if no == 0 :
    sdate = lyoum - datetime.timedelta(days=3)
    prevdate = lyoum - datetime.timedelta(days=2)
elif no == 1 :
    sdate = lyoum - datetime.timedelta(days=4)
    prevdate = lyoum - datetime.timedelta(days=3)
else:
     sdate = lyoum - datetime.timedelta(days=2)
     prevdate = lyoum - datetime.timedelta(days=1)

if no < 5 and ctime > starttime:
    selecteddate = lyoum
else:
    selecteddate = '2023-01-02'
    
threeyrsago = lyoum.replace(year=lyoum.year-3)
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
    params2 = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': prevdate,
    })
    
    params3 = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'EUR',
        'date': EOY,
    })

    try:
        conn3 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn3.request("GET", "/cours/Version1/api/CoursVirement?%s" % params3, "{body}", headers)
        response3 = conn3.getresponse()
        data3 = response3.read()
        conn3.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    eur3 = data3.decode()
    euro3 = json.loads(eur3)
    euro33 = euro3[0]
    eurmad3 = euro33.get("moyen")
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
    euro22 = euro2[0]
    eurmad2 = euro22.get("moyen")
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
        'date': prevdate,
    })
    
    params3 = urllib.parse.urlencode({
        # Request parameters
        'libDevise': 'USD',
        'date': EOY,
    })

    try:
        conn3 = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn3.request("GET", "/cours/Version1/api/CoursVirement?%s" % params2, "{body}", headers)
        response3 = conn3.getresponse()
        data3 = response3.read()
        conn3.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    usd3 = data3.decode()
    dol3 = json.loads(usd3)
    dol33 = dol3[0]
    dolmad3 = dol33.get("moyen")
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
    dol22 = dol2[0]
    dolmad2 = dol22.get("moyen")
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
eact = dirhameuro[0]
eprev = dirhameuro[1]
eeoy = dirhameuro[2]

dirhamdollar = usdmad()
dact = dirhamdollar[0]
dprev = dirhamdollar[1]
deoy = dirhamdollar[2]
BAMcc = pd.DataFrame({'Cours en MAD': [eact, dact]},index=['EUR', 'USD'])

varmad = [((eact-eprev)/eact)*100, ((dact-dprev)/dact)*100]
vareoy = [((eact-eeoy)/eact)*100, ((dact-deoy)/dact)*100]
BAMcc['var %'] = varmad
BAMcc['var ytd %'] = vareoy
st.dataframe(BAMcc)

#Scrap from yahoo finance

#                                        Indices
        
edate = lyoum

def indices():
    
    #Dow jones
    dj = yf.download("^DJI", sdate, edate)
    dj30 = dj.Close[1]
    dj30var = ((dj.Close[1]-dj.Close[0])*100)/dj.Close[0]

    #spoos
    sp = yf.download("^GSPC", sdate, edate)
    sp500 = sp.Close[1]
    sp500var = ((sp500-sp.Close[0])*100)/sp.Close[0]

    #nasdaq
    nas = yf.download("^IXIC", sdate, edate)
    nasdaq = nas.Close[1]
    nasdaqvar = ((nasdaq-nas.Close[0])*100)/nas.Close[0]

    #cac40
    cac4 = yf.download("^FCHI", sdate, edate)
    cac = cac4.Close[1]
    cacvar = ((cac-cac4.Close[0])*100)/cac4.Close[0]

    #DAX
    dax3 = yf.download("^GDAXI", sdate, edate)
    dax = dax3.Close[1]
    daxvar = ((dax-dax3.Close[0])*100)/dax3.Close[0]

    #nikkei
    jp1 = yf.download("^N225", sdate, edate)
    jp = jp1.Close[1]
    jpvar = ((jp-jp1.Close[0])*100)/jp1.Close[0]

    #hangseng
    #hk = yf.download("^HSI", sdate, edate)
    #hk = hk.Close[1]
    
    return dj30, sp500, nasdaq, cac, dax, jp, dj30var, sp500var, nasdaqvar, cacvar, daxvar, jpvar #, hk

#                                        Commodities

def commodities():
    #Gold
    gld1 = yf.download("GC=F", sdate, edate)
    gld = gld1.Close[1]
    gldvar = ((gld-gld1.Close[0])*100)/gld1.Close[0]

    #Brent
    oil1 = yf.download("BZ=F", sdate, edate)
    oil = oil1.Close[1]
    oilvar = ((oil-oil1.Close[0])*100)/oil1.Close[0]

    #silver
    silver1 = yf.download("SI=F", sdate, edate)
    silver = silver1.Close[0]
    silvervar = ((silver-silver1.Close[0])*100)/silver1.Close[0]
    
    return gld, oil, silver, gldvar, oilvar, silvervar

#                                          FX

#eurodollar
eurusd1 = yf.download("EURUSD=X", sdate, edate)
eurusd = eurusd1.Close[1]
eurusdvar = ((eurusd-eurusd1.Close[0])*100)/eurusd1.Close[0]

#calling funcs to lists
indiceslist = indices()
commolist = commodities()

#putting data into lists
Cours1 = [indiceslist[0], indiceslist[1], indiceslist[2], indiceslist[3], indiceslist[4], indiceslist[5]]
var1 = [indiceslist[6], indiceslist[7], indiceslist[8], indiceslist[9], indiceslist[10], indiceslist[11]]

Cours2 =  [eurusd, commolist[1], commolist[0], commolist[2]]
var2 =  [eurusdvar, commolist[3], commolist[4], commolist[5]]

# dictionary of lists 
dictin = {'Cours': Cours1, 'var %': var1}
dictin2 = {'Cours': Cours2, 'var %': var2}


FXCOM = pd.DataFrame(dictin2,index=['EUR/USD','Brent', 'Gold', 'Silver'])

intlindices = pd.DataFrame(dictin,index=['Dow Jones','S&P500', 'Nasdaq', 'CAC40', 'DAX30', 'NIKKEI']) #, indiceslist[6],'Hang Seng'

st.text('testing')
djeoy = yf.download("^DJI", "30-12-2022", "31-12-2022")
djeoye = djeoy.Close[0]
st.write(djeoye)

st.text('FX & commodities')
st.dataframe(FXCOM)

st.text('Indices internationaux')
st.dataframe(intlindices)

#BVCscrapper

#loading indices

#indices
index=bvc.getIndex()
dfindex = pd.DataFrame(index['Resume indice']).transpose()

#sectorial
dfsect = pd.DataFrame(index['Indices sectoriels']).transpose()

st.text('Indices BVC')
st.dataframe(dfindex)

st.text('Indices sectoriaux')
st.dataframe(dfsect)

#Pondération et cours
st.text('Pondérations')
courspond = pd.DataFrame(bvc.getPond())
st.dataframe(courspond)

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

st.dataframe(fulldf)

masi1=bvc.loadata('MASI',start=oneyrago,end=lyoum)
masi3=bvc.loadata('MASI',start=threeyrsago,end=lyoum)

#to excel sheets

buffer = io.BytesIO()

# Create a Pandas Excel writer using XlsxWriter as the engine.

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    
    # Write each dataframe to a different worksheet.
    
    BAMcc.to_excel(writer, sheet_name='Cours de change BAM')
    FXCOM.to_excel(writer, sheet_name='FX & commodities')
    intlindices.to_excel(writer, sheet_name='Indices internationaux')
    dfindex.to_excel(writer, sheet_name='Indices BVC')
    dfsect.to_excel(writer, sheet_name='Indices sectoriaux')
    courspond.to_excel(writer, sheet_name='Pondérations')
    fulldf.to_excel(writer, sheet_name='Cours & Variations')
    masi1.to_excel(writer, sheet_name='Masi Hist 1YR')
    masi3.to_excel(writer, sheet_name='Masi Hist 3YR')


    # Close the Pandas Excel writer and output the Excel file to the buffer
    
    writer.save()

    st.download_button(
        label="Scrap and download data",
        data=buffer,
        file_name="ds.xlsx"
    )
