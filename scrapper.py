import streamlit as st
import pandas as pd
import numpy as np
import datetime
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

#recap=bvc.getIndexRecap()
st.text('onga bounga')

recap=bvc.getIndexRecap()
data=bvc.loadata('BCP',start='2021-09-01',end='2021-09-10')
st.write(recap['Plus forte hausse'])
