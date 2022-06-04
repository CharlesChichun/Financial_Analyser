from email import header
from xml.dom.pulldom import START_ELEMENT
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse


ss = pd.read_html('./template.html')
ss[0].to_excel('outtt2.xlsx')
