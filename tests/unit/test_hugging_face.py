import os
from src.ReviewScraperwithSentimentAnalysis.components.hugging_face_pretrained import PreTrained
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration

c=Configuration()
pretrained_config=c.get_pretrained_config()

def test_huggingface():
    
    p=PreTrained()
    p.combine_all()
    save_model_path = pretrained_config.pretrained_model_dir

    assert os.path.exists(save_model_path) == 1
    assert len(os.listdir(save_model_path)) >= 1