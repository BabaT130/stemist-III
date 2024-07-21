import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

from bs4 import BeautifulSoup
import requests

from flask import Flask, request, render_template

#handling flask
app = Flask(__name__) #create flask instance

company = ""
summary = ""
sentiment_report = ""
confidence = 0

#get company name from form
@app.route("/", methods = ['GET', 'POST'])
def index():
    global company, summary
    if request.method == 'POST':
        company = request.form.get('company')
        market_analyzer(company)
        return render_template('index.html', summary = summary, sentiment_report = sentiment_report, confidence = confidence)
    
    return render_template('index.html')


#company = input("Company: ")
def market_analyzer(company):
    global summary, sentiment_report, confidence
    sentiment_report = ""
    ######################### Web Scraping #########################

    #List to store individual article links
    yahooArticles = []

    def get_articles():
        #Searches main webpages for relevant articles
        url = "https://finance.yahoo.com/topic/economic-news/"

        page = requests.get(url)

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

    get_articles()

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

    ######################### Sentiment Analysis #########################

    full_story = ""

    for article in allStates:
        full_story += str(article) + "."

    spacy_model = spacy.load('en_core_web_sm')

    article = (full_story.lower())
    segmented_article = article.split('.')

    market_sentiments = {
        "very-low": "highly negative",
        "low" : "negative",
        "neutral" : "steady",
        "high" : "positive",
        "very-high" : "highly positive"
    }

    #look for keywords, use regex to single out additional finance sentences
    keywords = ["profit", "loss", "loan", "finance", "money", "dollars", "value", "users", "customers", "investors", "investments"]

    #container to hold finance-related parts of article
    article_data = []

    #get all finance-related parts of article
    for segment in segmented_article:
        text = spacy_model(segment)

        for entity in text.ents:
            if entity.label_ == 'MONEY':
                article_data.append(segment)
            else:
                if segment not in article_data:
                    for item in keywords:
                        if re.search(item, segment): #look for sentence with keywords
                            article_data.append(segment)

    #get seperate headline and article sentiment
    analyzer = SentimentIntensityAnalyzer()
    article_sentiment = analyzer.polarity_scores(full_story)

    #assign sentiment number to stock future forecast
    net_sentiment = ""
    confidence = 0
    if article_sentiment['compound'] > 0.15 and article_sentiment['compound'] <= 0.5:
        net_sentiment = market_sentiments['high']
        confidence = 0.5
    elif article_sentiment['compound'] > 0.5 and article_sentiment['compound'] < 0.95:
        net_sentiment = market_sentiments['high']
        confidence = 0.7
    elif article_sentiment['compound'] >= 0.95:
        net_sentiment = market_sentiments['very-high']
        confidence = 0.9
    elif article_sentiment['compound'] < -0.15 and article_sentiment['compound'] >= -0.5:
        net_sentiment = market_sentiments['low']
        confidence = 0.5
    elif article_sentiment['compound'] < -0.15 and article_sentiment['compound'] > -0.95:
        net_sentiment = market_sentiments['low']
        confidence = 0.7
    elif article_sentiment['compound'] <= -0.95:
        net_sentiment = market_sentiments['very-low']
        confidence = 0.9
    else:
        net_sentiment = market_sentiments['neutral']
        confidence = 1

    #collect all finance parts of article and put into string
    article_finance_string = ""
    for segment in article_data:
        article_finance_string += segment + "."

    #display market sentiment / forecast
    if len(article_finance_string) > 0:
        sentiment_report = (f"Based on recent market sentiment, {company.upper()} seems to be moving towards {net_sentiment} growth in the near future.")
    else:
        sentiment_report = ("No Report")
        print("DISCLAIMER: All given results are predictions. We do not guarantee results.")

    #summarize all finance parts of article if they exist
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    if len(article_finance_string) > 0:
        if len(article_finance_string) < 2000:
            summary = summarizer(article_finance_string, min_length=15, max_length=700)
            generated_text = summary[0]['summary_text']
            summary = (f"Summary of {company.upper()}'s related financial news reports: {generated_text}")
        else:
            summary = "News Summary could not be Generated, too Many Articles"
    else:
        summary = "No Articles Found :( Please try again Later"

#run flask app
if __name__ == '__main__':
    app.run(debug=True)