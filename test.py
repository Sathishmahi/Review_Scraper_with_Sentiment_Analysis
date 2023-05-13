from ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import toExtractReviewsSingle


toExtractReviewsSingle("redminote7s")




# from ReviewScraperwithSentimentAnalysis.components.text_preprocessing import TextPreprocessing
# from ReviewScraperwithSentimentAnalysis.components.training import Training
# import pandas as pd
# import numpy as np
# # t=TextPreprocessing()
# import tensorflow as tf
# # t.combine_all()


# df=pd.read_csv('flipkart_data.csv')
# df['label']=df.rating.apply(lambda rating: 0 if rating<=3 else 1)

# t=Training()
# x_train,x_test,y_train,y_test=t.to_split_train_evaluation(df.drop(columns='rating'),'label')
# traindata,test_data=t.apply_buffer_and_batch_size(x_train,x_test,y_train,y_test)
# model=t.model_training(traindata)
# model=t.compile_model(model)
# t.fit_model(traindata,test_data,model)



# from transformers import pipeline
# model_name="distilbert-base-uncased"
# model=pipeline('zero-shot-classification')
# out=model(['hello how are you i am sathish i am fine',"i love you"],candidate_labels=[
#     'positive','negative'
# ]
# )
# print(out)

# from ReviewScraperwithSentimentAnalysis.components.hugging_face_pretrained import PreTrained

# p=PreTrained()
# p.combine_all()



# from ReviewScraperwithSentimentAnalysis.components.text_preprocessing import TextPreprocessing

# text_preprocessing=TextPreprocessing()
# df=text_preprocessing.review_combine_all("artifact/data_ingestion/review.csv")
