import nltk
import string
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from pathlib import Path
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from ReviewScraperwithSentimentAnalysis.constant import DATA_SET_PATH,COLUMNS_NAME
from ReviewScraperwithSentimentAnalysis.config import Configuration
import pandas as pd
stem=PorterStemmer()




class TextPreprocessing:

    def __init__(self,Configuration=Configuration()):
        self.text_preprocessing_config=Configuration.get_text_preprocessing_config()
        self.processed_data_file_path=self.text_preprocessing_config.processed_data_file_path
    
    @staticmethod
    def remove_unwanted_columns(csv_path:Path)->pd.DataFrame:
        df=pd.read_csv(csv_path).drop(columns=COLUMNS_NAME[1])
        return df

    def to_remove_stop_punctuation(self,df:pd.DataFrame)->pd.DataFrame:

        all_punctuation=string.punctuation
        df[COLUMNS_NAME[0]]=df[COLUMNS_NAME[0]].str.lower()
        all_stop=[stop.lower() for stop in stopwords.words('english') if ('no' not in stop) and ("n'" not in stop) and ("won" not in stop)]
        df[COLUMNS_NAME[0]]=df[COLUMNS_NAME[0]].apply( lambda sen:' '.join([stem.stem(word) for word in nltk.word_tokenize(sen) if word not in all_punctuation and all_stop]))
        df[COLUMNS_NAME[0]]=df[COLUMNS_NAME[0]].apply(lambda s : s.encode('ascii','ignore').decode())

        return df


    @staticmethod
    def to_save_csv(df:pd.DataFrame,file_path:Path):
        df.to_csv(file_path,index=False)
    
    def train_combine_all(self,csv_path:Path=Path(DATA_SET_PATH)):

        df=self.remove_unwanted_columns(csv_path)
        df=self.to_remove_stop_punctuation(df)
        self.to_save_csv(df=df, file_path=self.processed_data_file_path)


    def review_combine_all(self,csv_path:Path):

        df=pd.read_csv(csv_path)
        df=self.to_remove_stop_punctuation(df)
        self.to_save_csv(df=df, file_path=self.processed_data_file_path)
    


