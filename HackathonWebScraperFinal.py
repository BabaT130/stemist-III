from bs4 import BeautifulSoup
import requests
import re

#List to store individual article links
yahooArticles = []

#Searches main webpages for relevant articles
url = "https://finance.yahoo.com/topic/economic-news/"

page = requests.get(url)

company = input("Company Name: ")

soup = BeautifulSoup(page.text, "html.parser")

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        yahooArticles.append(a["href"])


url = "https://finance.yahoo.com/topic/earnings/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/commodities/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/world-indices/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/topic/stock-market-news/"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/u/yahoo-finance/watchlists/tech-stocks-that-move-the-market"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])
        yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/u/yahoo-finance/watchlists/the-berkshire-hathaway-portfolio"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

url = "https://finance.yahoo.com/u/yahoo-finance/watchlists/most-added"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

unique = 0

for a in soup.find_all("a", href=True):
    if str(company) in a["href"]:
        for links in yahooArticles:
            if str(a["href"]) == links:
                unique = 1
        if unique == 0:
            yahooArticles.append(a["href"])

#List containing data from a single article
stateList = []

#List containing data from every article
allStates = []

#Works through every article linked gathered
for article in yahooArticles:
    link = article
    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.text, "html.parser")
    
    #Scrapes the article body
    statments = []
    statments = soup2.find_all("p", href=False)

    #Cleans up unnesscary tags
    for sentence in statments:
        if str(sentence).find("<a") == -1:
            stateList.append(sentence)
        else:
            while str(sentence).find("<a") != -1:
                startInd = str(sentence).find("<a")
                endInd = str(sentence).find("</a>")
                sentence = str(sentence)[0:startInd] + str(sentence)[endInd+4:len(str(sentence))]
            stateList.append(sentence)

    #Further cleans up text
    cleanList = []
    for states in stateList:
        if str(states).find("<p>") != -1:
            states = str(states).replace("<p>", "")
        if str(states).find("</p>") != -1:
            cleanList.append(str(states).replace("</p>", ""))
    
    #Adds text from every article into 1 list
    allStates.append(cleanList)

print(allStates)


