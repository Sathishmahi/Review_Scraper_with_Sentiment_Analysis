import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from ReviewScraperwithSentimentAnalysis.entity import DataIngestionConfig 
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis.utils import to_save_csv

def ToExtractReviewsSingle(searchString:str,Configuration_cls=Configuration())->DataIngestionConfig:

    searchString = searchString.replace(" ","").replace("-", "")
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
    del bigboxes[0:3]
    box = bigboxes[0]
    productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
    prodRes = requests.get(productLink)
    prodRes.encoding='utf-8'
    prod_html = bs(prodRes.text, "html.parser")
    commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
    reviews,ratings =[],[]
    for commentbox in commentboxes:
        try:
            comtag = commentbox.div.div.find_all('div', {'class': ''})
            #custComment.encode(encoding='utf-8')
            custComment = comtag[0].div.text
            reviews.append(custComment)
        except Exception as e:
            reviews.append('no review')
        try:
            rating = commentbox.div.div.div.div.text
            ratings.append(rating)
        except:
            ratings.append('No Rating')

    file_path=Configuration_cls.get_data_ingestion_config().review_file_path
    to_save_csv({"reviews":reviews,"ratings":ratings},file_path)
        
        