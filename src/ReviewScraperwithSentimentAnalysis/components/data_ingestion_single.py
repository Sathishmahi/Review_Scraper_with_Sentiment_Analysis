import requests
import uuid
import os
import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from ReviewScraperwithSentimentAnalysis.entity import DataIngestionConfig
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis.constant import (
    COLUMNS_NAME,
    EXTRACT_PRODUCT_COLUMNS_NAME,
)
from ReviewScraperwithSentimentAnalysis.utils import to_save_csv, to_dataframe
from ReviewScraperwithSentimentAnalysis.constant import ToExtractImageEtcConstat, WAIT


data_ingestion_config = Configuration().get_data_ingestion_config()
extract_image_dir_name = data_ingestion_config.extract_image_dir_name
extract_product_csv_file_name = data_ingestion_config.extract_product_csv_file_name


wait = WAIT


def to_save_img(all_img_links: list):
    for li in tqdm(all_img_links, desc="to save image"):
        with open(
            os.path.join(extract_image_dir_name, f"img_{str(uuid.uuid1())}.jpg"), "wb"
        ) as img:
            with uReq(li) as req:
                img.write(req.read())
        time.sleep(wait)


def toExtractImage_etc(html_con):
    (
        image_urls_list,
        model_name_list,
        model_details_list,
        over_all_reviews_list,
        all_product_cost_list,
        all_product_offer_list,
        free_delivery_list,
    ) = ([], [], [], [], [], [], [])
    over_all_product_content = html_con.findAll(
        ToExtractImageEtcConstat.OVER_ALL_ELE_TYPE,
        {"class": ToExtractImageEtcConstat.OVER_ALL_CLASS},
    )

    for con in tqdm(over_all_product_content, desc="to extract info in html_content"):
        cost = con.findAll(
            ToExtractImageEtcConstat.PRODUCT_PRICE_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.PRODUCT_PRICE_CLASS},
        )
        offer = con.findAll(
            ToExtractImageEtcConstat.PRODUCT_OFFER_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.PRODUCT_OFFER_CLASS},
        )
        model_name = con.findAll(
            ToExtractImageEtcConstat.MODEL_NAME_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.MODEL_NAME_CLASS},
        )
        over_all_review = con.findAll(
            ToExtractImageEtcConstat.OVER_ALL_REVIEW_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.OVER_ALL_REVIEWS_CLASS},
        )
        image = con.findAll(
            ToExtractImageEtcConstat.PRODUCT_IMAGE_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.PRODUCT_IMAGE_CLASS},
        )
        free_delivery = con.findAll(
            ToExtractImageEtcConstat.FREE_DELIVERY_ELE_TYPE,
            {"class": ToExtractImageEtcConstat.FREE_DELIVERY_CLASS},
        )
        product_details = con.findAll(
            ToExtractImageEtcConstat.MODEL_DETAILS__ELE_TYPE,
            {"class": ToExtractImageEtcConstat.MODEL_DETAILS_CLASS},
        )

        over_all_product_details = None
        if product_details:
            over_all_product_details = " ".join(
                [detail.text for detail in product_details]
            )

        costModelNameReviewFreeDeliveryFun = lambda c: c[0].text if c else None
        offerFun = lambda o: o[0].span.text if o else None
        imageFun = lambda i: i[0]["src"] if i else None

        all_product_cost_list.append(costModelNameReviewFreeDeliveryFun(cost))
        all_product_offer_list.append(offerFun(offer))
        model_name_list.append(costModelNameReviewFreeDeliveryFun(model_name))
        over_all_reviews_list.append(
            costModelNameReviewFreeDeliveryFun(over_all_review)
        )
        image_urls_list.append(imageFun(image))
        free_delivery_list.append(costModelNameReviewFreeDeliveryFun(free_delivery))
        model_details_list.append(over_all_product_details)
        time.sleep(wait)

    # print(f"{len(image_urls_list)},{len(model_name_list)},{len(model_details_list)},{len(over_all_reviews_list)},{len(all_product_cost_list)},{len(all_product_offer_list)},{len(free_delivery_list)}")
    # print(f"{(image_urls_list)},{(model_name_list)},{(model_details_list)},{(over_all_reviews_list)},{(all_product_cost_list)},{(all_product_offer_list)},{(free_delivery_list)}")


def toExtractReviewsSingle(
    searchString: str, Configuration_cls=Configuration()
) -> DataIngestionConfig:
    searchString = searchString.replace(" ", "").replace("-", "")
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    toExtractImage_etc(html_con=flipkart_html)
    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
    del bigboxes[0:3]
    box = bigboxes[0]
    productLink = "https://www.flipkart.com" + box.div.div.div.a["href"]
    prodRes = requests.get(productLink)
    prodRes.encoding = "utf-8"
    prod_html = bs(prodRes.text, "html.parser")
    commentboxes = prod_html.find_all("div", {"class": "_16PBlm"})
    reviews, ratings = [], []
    for commentbox in tqdm(commentboxes, desc="to extract comment in html_page"):
        try:
            comtag = commentbox.div.div.find_all("div", {"class": ""})
            # custComment.encode(encoding='utf-8')
            custComment = comtag[0].div.text
            reviews.append(custComment)
        except Exception as e:
            reviews.append("no review")
        try:
            rating = commentbox.div.div.div.div.text
            ratings.append(rating)
        except:
            ratings.append("No Rating")

    file_path = Configuration_cls.get_data_ingestion_config().review_file_path
    to_save_csv({COLUMNS_NAME[0]: reviews, COLUMNS_NAME[1]: ratings}, file_path)
