import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
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


if no < 5 and ctime > starttime:
    selecteddate = lyoum
else:
    selecteddate = '2022-12-02'
    
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

    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    eur = float(data.decode()[-25:-18])
    return eur

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

    try:
        conn = http.client.HTTPSConnection('api.centralbankofmorocco.ma')
        conn.request("GET", "/cours/Version1/api/CoursVirement?%s" % params, "{body}", headers)
        response = conn.getresponse()
        dataus = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    usd = float(dataus.decode()[-25:-18])
    return usd
#BAMcc = pd.DataFrame({'Cours en MAD': [euromad(), usdmad()]},index=['EUR', 'USD'])
#st.dataframe(BAMcc)


#Scrap from yahoo finance

#                                        Indices

#Previous method
#Dow jones
#dj30 = yf.Ticker("^DJI")
#dj30 = dj30.info['previousClose']

sdate = '2022-12-16'
edate = '2022-12-17'

def indices():
    
    #Dow jones
    dj30 = yf.download("^DJI", sdate, edate)
    dj30 = dj30.Close[0]

    #spoos
    sp500 = yf.download("^GSPC", sdate, edate)
    sp500 = sp500.Close[0]

    #nasdaq
    nasdaq = yf.download("^IXIC", sdate, edate)
    nasdaq = nasdaq.Close[0]

    #cac40
    cac = yf.download("^FCHI", sdate, edate)
    cac = cac.Close[0]

    #DAX
    dax = yf.download("^GDAXI", sdate, edate)
    dax = dax.Close[0]

    #nikkei
    jp = yf.download("^N225", sdate, edate)
    jp = jp.Close[0]

    #hangseng
    hk = yf.download("^HSI", sdate, edate)
    hk = hk.Close[0]
    
    return dj30, sp500, nasdaq, cac, dax, jp, hk


#                                        Commodities


def commodities():
    #Gold
    gld = yf.download("GC=F", sdate, edate)
    gld = gld.Close[0]


    #Brent
    oil = yf.download("BZ=F", sdate, edate)
    oil = oil.Close[0]

    #silver
    silver = yf.download("SI=F", sdate, edate)
    silver = silver.Close[0]
    return gld, oil, silver

#                                          FX

#eurodollar
eurusd = yf.download("EURUSD=X", sdate, edate)
eurusd = eurusd.Close[0]

#calling funcs to lists
indiceslist = indices()
commolist = commodities()

FXCOM = pd.DataFrame({'Cours': [eurusd, commolist[1], commolist[0], commolist[2]]},index=['EUR/USD','Brent', 'Gold', 'Silver'])
intlindices = pd.DataFrame({'Cours': [indiceslist[0], indiceslist[1], indiceslist[2], indiceslist[3], indiceslist[4], indiceslist[5], indiceslist[6]]},index=['Dow Jones','S&P500', 'Nasdaq', 'CAC40', 'DAX30', 'NIKKEI','Hang Seng'])

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
    seance.append({'Ticker': val["name"],'Cours': val["cours"], 'Cloture': val["cloture"],'Variation': val["variation"], 'Volume Titre': val["volumeTitre"],"derniere transaction" : stripped]})
    fulldf = pd.DataFrame(seance)
    
#fulldf['derniere transaction'] = pd.to_datetime(fulldf['derniere transaction'], infer_datetime_format=True)

#fulldf['derniere transaction'] = fulldf['derniere transaction'].dt.date

#tradedtoday = fulldf['derniere transaction'] < lyoum
#fulldf.loc[tradedtoday, 'Volume Titre'] = 0
#fulldf.loc[tradedtoday, 'Variation'] = 0 

st.dataframe(fulldf)

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
