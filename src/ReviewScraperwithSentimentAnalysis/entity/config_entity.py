from collections import namedtuple


DataIngestionConfig=namedtuple("DataIngestionConfig", 
                    [
                        "root_dir",
                        "review_file_path"
                    ]
                    )


TextPreprocessingConfig=namedtuple("TextPreprocessingConfig", 
                                    [
                                        "root_dir",
                                        "processed_data_file_path"
                                    ]
                                    )