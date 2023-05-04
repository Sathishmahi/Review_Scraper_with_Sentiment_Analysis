import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from ReviewScraperwithSentimentAnalysis.config import Configuration
import pandas as pd
import numpy as np


class ToExtractReviewsBulk:
  def __init__(self,product_name:str,Configuration=Configuration()):

    self.data_ingestion_config=Configuration.get_data_ingestion_config()
    searchString=product_name.replace(" ", "").replace("-", "")
    self.root_url="https://www.flipkart.com"
    self.flipkart_url =  self.root_url+"/search?q="+searchString


  @staticmethod
  def to_save_csv(all_reviews_list:list,file_path:str,columns_name:list):
    
    df=pd.DataFrame(all_reviews_list,columns=columns_name)
    df.to_csv(file_path,index=None)

  def to_return_html_content(self,content_url):
    uClient_demo= uReq(content_url)
    raw_content=uClient_demo.read()
    html_content=bs(raw_content,'html.parser')
    uClient_demo.close()
    return html_content
    # 
  def to_extract_front_page_details(self,front_page_url):
    classes_id=['_1fQZEK',"_2rpwqI"]
    for class_ in classes_id:
      flipkart_html=self.to_return_html_content(front_page_url)
      content_anchor=flipkart_html.findAll('a',{"class":class_})
      content=[self.root_url+anchor['href'] for anchor in content_anchor]
      if content:
        return content

    

  def to_featch_all_review_page_link(self,content_url):
    # content_url=self.root_url+href_link
    html_content=self.to_return_html_content(content_url)
    all_review_link_class_id="col JOpGWq"
    all_review_class_id="_1YokD2 _3Mn1Gg"
    return self.root_url+html_content.findAll('div',{"class":all_review_link_class_id})[0].a['href']

  def to_extract_single_page_reviews(self,content_url):
    review_class_id="t-ZTKy"
    html_content=self.to_return_html_content(content_url)
    review_html=html_content.findAll("div",{"class":review_class_id})
    return [review.div.div.text for review in review_html]

  def to_fetch_next_page_url(self,current_page_url):
    next_page_url_class_id="_1LKTO3"
    html_content=self.to_return_html_content(current_page_url)
    return self.root_url+html_content.findAll("a",{"class":next_page_url_class_id})[0]['href']

  def to_fetch_all_reviews(self,content_url):
    final_all_reviews=self.to_extract_single_page_reviews(content_url)
    # print(final_all_reviews)
    html_content=self.to_return_html_content(content_url)
    no_of_times_run_class_id="_2MImiq _1Qnn1K"
    no_of_times_run=html_content.findAll("div",{"class":no_of_times_run_class_id})[0].span.text.split()[-1]
    for _ in range(int(no_of_times_run)):
      next_page_url=self.to_fetch_next_page_url(content_url)
      all_reviews=self.to_extract_single_page_reviews(next_page_url)
      content_url=next_page_url
      print('======'*30)
      print(all_reviews)
      print('======'*30)
       
      if len(final_all_reviews)==100:
        break
      
      [final_all_reviews.append(review) for review in all_reviews]
      # final_all_reviews.append(all_reviews)
    return final_all_reviews

  def combine_all(self):
    all_reviews=[]
    front_page_url=self.flipkart_url
    all_front_page_link=self.to_extract_front_page_details(front_page_url)
    for link in all_front_page_link[:1]:
      all_review_page_link=self.to_featch_all_review_page_link(link)
      all_reviews.append(self.to_fetch_all_reviews(all_review_page_link))
      if len(all_reviews)==100:
        break
    print(all_reviews)
    self.to_save_csv(all_reviews_list=np.array(all_reviews).T, file_path='demo.csv', columns_name=['reviews'])

  
