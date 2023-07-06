import requests
import uuid
import os
import time
import string
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from ReviewScraperwithSentimentAnalysis.entity import DataIngestionConfig
from ReviewScraperwithSentimentAnalysis import logging
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
STAGE_NAME = "toExtractReviewsSingle"


def to_save_img(
    all_img_links: list[str],
    image_name_list: list[str],
    remove_prevoius_image: bool = True,
):
    """
    func to save all product images

    Args:
        all_img_links (list[str]): all product image url
        image_name_list (list[str]): image path list

    raise:
        FileNotFoundError: to raise FileNotFoundError exception if root image dir not found

    """
    if not os.path.exists(extract_image_dir_name):
        raise FileNotFoundError(f"No such file or directory {extract_image_dir_name} ")
    all_pre_imgs_li = os.listdir(extract_image_dir_name)
    if remove_prevoius_image and len(all_pre_imgs_li) > 0:
        nothing = [
            os.remove(os.path.join(extract_image_dir_name, im))
            for im in all_pre_imgs_li
        ]
        del nothing
    try:
        for li, img_name in zip(all_img_links, image_name_list):
            with open(
                os.path.join(extract_image_dir_name, f"{img_name}.jpg"), "wb"
            ) as img:
                with uReq(li) as req:
                    img.write(req.read())
            time.sleep(wait)
    except Exception as e:
        raise e


def toExtractImage_etc(html_con) -> dict:
    """
    this func to extract reviews , image url etc., from Internet

    Args:
        html_con (Any): html source of the product

    Returns:
        dict: extracted reviews , image urls etc..,

    raise:
        Exception: base exception
    """

    try:
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

        for con in tqdm(
            over_all_product_content, desc="to extract info in html_content"
        ):
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

        final_dict = {
            EXTRACT_PRODUCT_COLUMNS_NAME[0]: image_urls_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[1]: model_name_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[2]: model_details_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[3]: over_all_reviews_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[4]: all_product_cost_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[5]: all_product_offer_list,
            EXTRACT_PRODUCT_COLUMNS_NAME[6]: free_delivery_list,
        }
        image_name_list = [
            img_name.replace(" ", "_")
            .replace(",", "_")
            .replace("(", "")
            .replace(")", "")
            for img_name in model_name_list
        ]
        to_save_img(all_img_links=image_urls_list, image_name_list=image_name_list)
        return final_dict

    except Exception as e:
        raise e


def toExtractReviewsSingle(searchString: str, configuration=Configuration()) -> None:
    try:
        all_special_cher = [*string.punctuation, " "]
        searchString = "".join([c for c in searchString if c not in all_special_cher])
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        uClient = uReq(flipkart_url)
        flipkartPage = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkartPage, "html.parser")
        extract_content_details_dict = toExtractImage_etc(html_con=flipkart_html)
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
                custComment = comtag[0].div.text
                reviews.append(custComment)
            except Exception as e:
                reviews.append("no review")
            try:
                rating = commentbox.div.div.div.div.text
                ratings.append(rating)
            except:
                ratings.append("No Rating")

        data_ingestion_content = configuration.get_data_ingestion_config()
        file_path = data_ingestion_content.review_file_path
        extract_product_csv_file_path = (
            data_ingestion_content.extract_product_csv_file_name
        )
        df = pd.DataFrame({COLUMNS_NAME[0]: reviews, COLUMNS_NAME[1]: ratings}).dropna()
        logging.info(f" reviews stored into {file_path} ")
        to_save_csv(df, file_path)
        df = pd.DataFrame(extract_content_details_dict).dropna()
        logging.info(
            f" all product details stored into {extract_product_csv_file_path} "
        )
        to_save_csv(df, extract_product_csv_file_path)

    except Exception as e:
        logging.exception(msg=e)
        raise e


if __name__ == "__main__":
    logging.info(msg=f" >>>>>>  START {STAGE_NAME}    >>>>>>")
    toExtractReviewsSingle(searchString="redminote7s")
    logging.info(msg=f" >>>>>>  END {STAGE_NAME}    >>>>>>")
