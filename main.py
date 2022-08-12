from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests
import re
import json


ticker = "AAPL"
stats = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"
financials = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
profile = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"


headers = {'User Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
rf = requests.get(financials.format(ticker, ticker), headers)
soup1 = BeautifulSoup(rf.text, 'html.parser')


# Use regex to find the pattern within the code to get the data we need
pat1 = re.compile(r'\s--\sData\s--\s')
data1 = soup1.find('script', text=pat1).contents[0]
# Finding the characters within the slices of data
start1 = data1.find('context')-2
jsonData = json.loads(data1[start1:-12])


# Profile Data (Executive/Officers Info)
rp2 = requests.get(profile.format(ticker, ticker), headers)
soup2 = BeautifulSoup(rp2.text, 'html.parser')
pat2 = re.compile(r'\s--\sData\s--\s')
data2 = soup2.find('script', text=pat2).contents[0]
start2 = data2.find('context')-2
jsonData2 = json.loads(data2[start2:-12])






# Financial Data (Quarterly, Annually) Balance Sheet, Income Statement, Cash Flow

annualIS = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterlyIS = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']

annualCF = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterlyCF = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']


annualBS = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterlyBS = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']

annual_IncomeStatement = []
annual_CashFlowStatement = []
annual_BalanceSheetStatement = []

for values in annualIS:
    temp = {}
    for key, val in values.items():
        try:
            temp[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_IncomeStatement.append(temp)
print(annual_IncomeStatement[0])



#Statistics Data

rp3 = stats.get(profile.format(ticker, ticker), headers)
soup3 = BeautifulSoup(rp3.text, 'html.parser')
pat3 = re.compile(r'\s--\sData\s--\s')
data3 = soup3.find('script', text=pat3).contents[0]
start3 = data3.find('context')-2
jsonData3 = json.loads(data3[start3:-12])



historical_data = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1628745097&period2=1660281097&interval=1d&events=history&includeAdjustedClose=true"
rp4 = requests.get(historical_data, headers)

historical_results = []

historical = pd.DataFrame(historical_results)
historical.to_csv('historical_data.csv')


#def scrapedata(ticker):
#url = f"https://finance.yahoo.com/quote/{ticker}"
#headers = {"User Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
#r = requests.get(url, headers)
#soup = BeautifulSoup(r.content, 'html.parser')
#return soup



