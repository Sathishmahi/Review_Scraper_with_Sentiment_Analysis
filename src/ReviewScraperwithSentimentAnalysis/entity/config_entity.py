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


TrainingConfig=namedtuple("TrainingConfig", 
                        [
                            "root_dir",
                            "model_dir",
                            "model_file_name",
                            "data_path",
                            "epochs",
                            "batch_size",
                            "buffer_size",
                            "vocab_size",
                            "BiRnnUnits",
                            "eval_data_per",
                            "embedding_dim",
                            "no_classes",
                            "output_columns_name"
                        ]
                        )