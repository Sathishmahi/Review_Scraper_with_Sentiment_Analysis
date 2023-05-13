import requests
import uuid
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from ReviewScraperwithSentimentAnalysis.entity import DataIngestionConfig 
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis.constant import COLUMNS_NAME
from ReviewScraperwithSentimentAnalysis.utils import to_save_csv
from ReviewScraperwithSentimentAnalysis.constant import ToExtractImageEtc


data_ingestion_config=Configuration().get_data_ingestion_config()
extract_image_dir_name=data_ingestion_config.extract_image_dir_name

def to_save_img(all_img_links:list):
    print(all_img_links)
    for li in all_img_links:
        with open (os.path.join(extract_image_dir_name,f'img_{str(uuid.uuid1())}.jpg'),'wb') as img:
            with uReq(li) as req:
                print(f'img write {li}')
                img.write(req.read())
                
def toExtractImage_etc(html_co):

    all_price_raw_co=html_co.findAll(ToExtractImageEtc.PRICE_CLASS_TAG,{"class",ToExtractImageEtc.PRICE_CLASS})
    all_price_li=[co.text for co in all_price_raw_co]

    all_offer_raw_co=html_co.findAll(ToExtractImageEtc.OFFER_CLASS_TAG,{"class",ToExtractImageEtc.OFFER_CLASS})
    all_offer_li=[co.text for co in all_offer_raw_co]

    all_spec_raw_co=html_co.findAll(ToExtractImageEtc.SPEC_CLASS_TAG,{"class",ToExtractImageEtc.SPEC_CLASS_TAG})
    all_spec_li=[co.text for co in all_spec_raw_co]

    all_img_li=html_co.findAll(ToExtractImageEtc.IMG_CLASS_TAG,{"class",ToExtractImageEtc.IMG_CLASS})
    all_img_links,all_sample_product_details=[],[]
    nothing=[ (all_img_links.append(co['src']),all_sample_product_details.append(co['alt'])) for co in all_img_li]
    to_save_img(all_img_links=all_img_links)
    del nothing

def toExtractReviewsSingle(searchString:str,Configuration_cls=Configuration())->DataIngestionConfig:

    searchString = searchString.replace(" ","").replace("-", "")
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    toExtractImage_etc(html_co=flipkart_html)
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
    to_save_csv({COLUMNS_NAME[0]:reviews,COLUMNS_NAME[1]:ratings},file_path)
        
        