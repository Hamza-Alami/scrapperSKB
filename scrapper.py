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
BAMcc = pd.DataFrame({'Cours en MAD': [euromad(), usdmad()]},index=['EUR', 'USD'])
st.dataframe(BAMcc)

#Scrap from yahoo finance

#                                        Indices
def indices():
    #Dow jones
    dj30 = yf.Ticker("^DJI")
    dj30 = dj30.info['previousClose']

    #spoos
    sp500 = yf.Ticker("^GSPC")
    sp500 = sp500.info['previousClose']

    #nasdaq
    nasdaq = yf.Ticker("^IXIC")
    nasdaq = nasdaq.info['previousClose']

    #cac40
    cac = yf.Ticker("^FCHI")
    cac = cac.info['previousClose']

    #DAX
    dax = yf.Ticker("^GDAXI")
    dax = dax.info['previousClose']

    #nikkei
    jp = yf.Ticker("^N225")
    jp = jp.info['previousClose']

    #hangseng
    hk = yf.Ticker("^HSI")
    hk = hk.info['previousClose']
    
    return dj30, sp500, nasdaq, cac, dax, jp, hk


#                                        Commodities


def commodities():
    #Gold
    gld = yf.Ticker("GC=F")
    gld = gld.info['previousClose']

    #Brent
    oil = yf.Ticker("BZ=F")
    oil = oil.info['previousClose']

    #silver
    silver = yf.Ticker("SI=F")
    silver = silver.info['previousClose']
    return gld, oil, silver

#                                          FX

#eurodollar
eurusd = yf.Ticker("EURUSD=X")
eurusd = eurusd.info['previousClose']

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


#testing 

response_API = requests.get('https://medias24.com/content/api?method=getAllStocks&format=json')
x = response_API.content
y = json.loads(x)
z = y['result']
trntrn = z[0]
    
seance = []
for i, val in enumerate(z):
    seance.append({'Ticker': val["name"],'Cours': val["cours"], 'Cloture': val["cloture"],'Variation': val["variation"], 'Volume Titre': val["volumeTitre"],"derniere transaction" : val["datetime"]})
    fulldf = pd.DataFrame(seance)
    
fulldf['derniere transaction'] = pd.to_datetime(fulldf['derniere transaction'], infer_datetime_format=True)

fulldf['derniere transaction'] = fulldf['derniere transaction'].dt.date

tradedtoday = fulldf['derniere transaction'] < lyoum
st.write(tradedtoday)

st.dataframe(fulldf)
