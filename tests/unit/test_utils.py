import os
import pytest
import yaml
import pandas as pd
from src.ReviewScraperwithSentimentAnalysis.utils.common import (
    to_dataframe,
    to_load_pkl,
    to_save_csv,
    to_save_pkl,
    make_dirs,
    read_yaml,
)


temp_path = os.path.join("tests", "unit", "temp")
os.makedirs(temp_path, exist_ok=True)
file_paths = [os.path.join(temp_path, "test_1.pkl")]
contents = [list(range(10))]
columns_name = ["column_1"]
temp_dict = {"name": ["sathish", "kumar"]}


class TestUtils:
    def test_make_dirs(self, tmpdir):
        make_dirs(dirs_list=[tmpdir])
        assert os.path.isdir(tmpdir) == 1

    def test_save_pickle(self):
        to_save_pkl(contents, file_paths)
        assert all([os.path.exists(fp) for fp in file_paths]) == 1

    def test_to_load_pickle(self):
        val_final_li = []
        for fp, con, cn in zip(file_paths, contents, columns_name):
            temp_df = to_load_pkl(fp)
            pre_li = temp_df.values[0]
            # val_final_li.append(pre_li==con and cn == temp_df.index[0])
            val_final_li.append(pre_li == con)
        assert all(val_final_li) == 1

    def test_to_dataframe(self):
        with pytest.raises(expected_exception=ValueError) as exc_info:
            to_dataframe(data_dict=[1, 2, 1, 2, 1])

        assert type(to_dataframe(data_dict=temp_dict)) == pd.DataFrame

    def test_read_yaml(self):
        fp = os.path.join(temp_path, "temp.yaml")
        with open(fp, "w") as yf:
            yaml.safe_dump(temp_dict, yf)

        data = read_yaml(fp)
        assert data == temp_dict

    def test_to_save_csv(self):
        temp_csv_path = os.path.join(temp_path, "temp.csv")

        to_save_csv(all_reviews=[[1, 2, 1, 21], [1, 2, 1, 21]], file_path=temp_csv_path)
        assert os.path.exists(path=temp_csv_path) == 1
        os.remove(temp_csv_path)

        to_save_csv(all_reviews=[(1, 2, 1, 21), (1, 2, 1, 21)], file_path=temp_csv_path)
        assert os.path.exists(path=temp_csv_path) == 1
        os.remove(temp_csv_path)

        to_save_csv(all_reviews=temp_dict, file_path=temp_csv_path)
        assert os.path.exists(path=temp_csv_path) == 1
        os.remove(temp_csv_path)
