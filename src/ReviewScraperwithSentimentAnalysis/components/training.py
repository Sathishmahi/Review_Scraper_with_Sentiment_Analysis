import tensorflow as tf
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis.entity import TrainingConfig


class Training:
    def __init__(self, Configuration=Configuration()):
        self.training_config = Configuration.get_training_config()

    def to_split_train_evaluation(
        self, df: pd.DataFrame, out_column_name: str
    ) -> tuple:
        eval_per = self.training_config.eval_data_per
        x_train, x_test, y_train, y_test = train_test_split(
            df.iloc[:, 0], df[out_column_name], test_size=eval_per, random_state=100
        )
        return x_train, x_test, y_train, y_test

    def apply_buffer_and_batch_size(self, x_train, x_test, y_train, y_test):
        buffer_size = self.training_config.buffer_size
        batch_size = self.training_config.batch_size
        train_data = (
            tf.data.Dataset.from_tensor_slices((x_train, y_train))
            .shuffle(buffer_size)
            .batch(batch_size)
            .prefetch(tf.data.experimental.AUTOTUNE)
        )
        eval_data = (
            tf.data.Dataset.from_tensor_slices((x_test, y_test))
            .batch(batch_size)
            .prefetch(tf.data.experimental.AUTOTUNE)
        )
        return train_data, eval_data

    def model_training(self, train_data):
        vocab_size = self.training_config.vocab_size
        embedding_dim = self.training_config.embedding_dim
        birnn_units = self.training_config.BiRnnUnits
        no_of_classes = self.training_config.no_classes
        # birnn_units=self.training_config.BiRnnUnits

        encoder = tf.keras.layers.TextVectorization(vocab_size)
        # encoder.save('my_model', save_format='tf')
        encoder.adapt(train_data.map(lambda txt, label: txt))

        embedding_layer = tf.keras.layers.Embedding(
            input_dim=len(encoder.get_vocabulary()),
            output_dim=embedding_dim,
            mask_zero=True,
        )

        LAYERS = [
            encoder,
            embedding_layer,
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=birnn_units)),
            tf.keras.layers.Dense(units=64, activation="relu"),
            tf.keras.layers.Dense(no_of_classes, activation="softmax"),
        ]

        model = tf.keras.Sequential(LAYERS)
        model.summary()
        return model

    def compile_model(self, model: tf.keras.Model):
        model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"],
        )
        return model

    def fit_model(self, train_data, eval_data, model):
        epochs = self.training_config.epochs
        model.fit(train_data, validation_data=eval_data, epochs=epochs)
        return model

    def save_model(self, path: Path, model: tf.keras.Model):
        model.save(path, save_format="tf")

    def combine_all(self):
        model_path = self.training_config.model_file_name
        data_path = self.training_config.data_path
        df = pd.read_csv("flipkart_data.csv")
        df["label"] = df.rating.apply(lambda rating: 0 if rating <= 3 else 1)
        x_train, x_test, y_train, y_test = self.to_split_train_evaluation(
            df, self.training_config.output_columns_name
        )
        train_data, test_data = self.apply_buffer_and_batch_size(
            x_train, x_test, y_train, y_test
        )

        model = self.model_training(train_data)
        model = self.compile_model(model)
        model = self.fit_model(train_data, test_data, model)
        self.save_model(Path("model_path"), model)

        model = tf.keras.models.load_model("model_path")
        print(model.predict([["this product very good and awesome"]]))
        print(f"======== finish ============")


if __name__ == "__main__":
    training = Training()
    training.combine_all()
