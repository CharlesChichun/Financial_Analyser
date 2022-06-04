from operator import index
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree, html

headers = {
    'Content-Type': 'application/x-www-form-urlencoded;',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'referer': 'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID=2332',
    'Cookie': 'CLIENT%5FID=20220604002816788%5F101%2E10%2E6%2E162'
}

TEMPATH = './template.html'
SEASON = [20214, 20201, 20182]
IS_M_QUAR = 'IS_M_QUAR'
BS_M_QUAR = 'BS_M_QUAR'


def postReq(url, payload):

    res = requests.request("POST", url, headers=headers, data=payload)
    res.encoding = 'utf-8'

    return res.text


def resHandler(text):
    soup = BeautifulSoup(text, "html.parser")
    with open(TEMPATH, 'r') as temPage:
        temSoup = BeautifulSoup(temPage, 'html.parser')

        soup.find('table').decompose()

        temSoup.find('body').append(soup)

        return pd.read_html(str(temSoup))


# RPT_CAT = IS_M_QUAR or BS_M_QUAR
# QRY_TIME = 20214, 20201 or 20182
def genUrlnPayload(sticker, type, session):
    url = "https://goodinfo.tw/tw/StockFinDetail.asp?STEP=DATA&STOCK_ID=%d&RPT_CAT=%s&QRY_TIME=%d" % (
        sticker, type, session)

    payload = 'STEP=DATA&STOCK_ID=%d&RPT_CAT=%s&QRY_TIME=%d' % (
        sticker, type, session)
    return url, payload


def cleanTrans(df):
    c = ['', '金額', '%', '金額', '%', '金額', '%',
         '金額', '%', '金額', '%', '金額', '%', '金額', '%']
    df.columns = c
    df = df.drop(['%'], axis=1)
    df = df.transpose()
    header_row = 0
    df.columns = df.iloc[header_row]
    df.drop(df.index[0], axis=0, inplace=True)

    df.reset_index(drop=True, inplace=True)
    return df.drop(df.columns[df.columns.duplicated()].values.tolist(), axis=1)


def addTimeNameIndux(df, sticker, season):
    switch = {
        20214: ['2021Q4', '2021Q3', '2021Q2',
                '2021Q1', '2020Q4', '2020Q3', '2020Q2'],
        20201: ['2020Q1', '2019Q4', '2019Q3',
                '2019Q2', '2019Q1', '2018Q4', '2018Q3'],
        20182:  ['2018Q2', '2018Q1', '2017Q4',
                 '2017Q3', '2017Q2', '2017Q1', '2016Q4']
    }
    timeSer = switch.get(season, "")

    tmp = pd.DataFrame(columns=['公司', '股票代號', '產業', '時間'])
    name, indus = getNameIndus(sticker)
    tmp['公司'] = [name]*7
    tmp['股票代號'] = [sticker]*7
    tmp['產業'] = [indus]*7
    tmp['時間'] = timeSer

    return pd.concat([tmp, df], axis=1)


def getNameIndus(sticker):
    url = 'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=%d' % (sticker)
    res = requests.request('get', url, headers=headers)
    byte_data = res.content
    source_code = html.fromstring(byte_data)
    nameXp = '/html/body/table[2]/tr/td[3]/table/tr[1]/td/table/tr/td[1]/table/tr[1]/th/table/tr/td[1]/nobr/a/text()'
    indXp = '/html/body/table[2]/tr/td[3]/table/tr[2]/td[3]/table[1]/tr[3]/td[2]/text()'
    return source_code.xpath(nameXp)[0][5:], source_code.xpath(indXp)[0]


def companyState(sticker=2330, stype=IS_M_QUAR):
    dfs = []
    for i in range(3):
        url, payload = genUrlnPayload(sticker, stype, SEASON[i])
        tmpDfs = resHandler(postReq(url, payload))
        df = cleanTrans(tmpDfs[0])
        dfs.append(addTimeNameIndux(df, sticker, SEASON[i]))

    return pd.concat(dfs, ignore_index=True)[:-1]


def wholeState(companies, stype):
    dfs = []
    for c in companies:
        dfs.append(companyState(c, stype))
        print(c, " done...")
    print("All companies down")
    return pd.concat(dfs, ignore_index=True)


if __name__ == '__main__':
    wholeState([2332, 2330, 1786], IS_M_QUAR).to_excel('IS_whole.xlsx')
