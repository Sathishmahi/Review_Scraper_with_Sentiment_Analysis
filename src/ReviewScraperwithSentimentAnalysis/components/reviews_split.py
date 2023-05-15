from ReviewScraperwithSentimentAnalysis.config import Configuration
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import os
from ReviewScraperwithSentimentAnalysis.constant import COLUMNS_NAME,CAMERA_LABELS,BATTERY_LABELS,DISPLAY_LABELS


class SplitReviews:
    def __init__(self,configuration=Configuration())->None:
        self.camera_list,self.display_list,self.battery_list,self.overall_list=[],[],[],[]
        self.review_split_config=configuration.get_review_split_config()

    @staticmethod
    def to_read_csv(csv_file_path:Path,specific_column:list[str]=None):

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"csv file not found {csv_file_path}")
        if specific_column:
            try:
                df=pd.read_csv(csv_file_path,usecols=specific_column)
                return df

            except ValueError as e:
                raise ValueError("columns not found")
        df=pd.read_csv(csv_file_path)
        return df

    def to_split_reviews(self)->pd.DataFrame:

        csv_file_path=self.review_split_config.review_csv_path
        review_col_name=COLUMNS_NAME[0]
        review_df=self.to_read_csv(csv_file_path=csv_file_path,specific_column=[review_col_name])
        reviews_list=pd.Series(review_df.iloc[:,0]).to_list()
        comma_list,full_list=self.to_split_comma_full(review_list=reviews_list)
        self.updated_list(combine_reviews_list=comma_list+full_list)


    @staticmethod
    def to_split_comma_full(review_list:list[str])->tuple[list]:
        com_li,full_li=[],[]
        nothing=[(com_li.append(review.split(',')),full_li.append(review.split('.'))) for review in review_list ]
        del nothing
        return (sum(com_li,[]),sum(full_li,[]))

    
    def _helper_updated_list(self,review:str):
        if review:
            if 'camera' in review:
                self.camera_list.append(review)
            elif 'battery' in review:
                self.battery_list.append(review)
            elif 'display' in full:
                self.display_list.append(review)
            else:
                self.overall_list.append(review)

    def updated_list(self,combine_reviews_list:list[str])->tuple[list]:
        for review in combine_reviews_list:
            self._helper_updated_list(review=review)


        
        
        
