# Load model
import keras
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text
import json


def make_model():
    model_path = r"./Data/BERT"
    preprocess_path = r"Data/preprocess"

    preprocessor = hub.KerasLayer(
        hub.load(preprocess_path))

    encoder = hub.KerasLayer(
        hub.load(model_path),
        trainable=True)
    with open('./Data/Model/mlb_keys.json') as f:
        mlb_keys = json.load(f)
    n_labels = len(mlb_keys)
    text_input = keras.layers.Input(shape=(), dtype=tf.string)
    encoder_inputs = preprocessor(text_input)
    outputs = encoder(encoder_inputs)

    pooled_output = outputs["pooled_output"]

    x = keras.layers.Dense(256)(pooled_output)
    out = keras.layers.Dense(n_labels, activation='sigmoid')(x)

    bert_model = keras.Model(text_input, out)
    bert_model.load_weights(r'Data/Model/model.h5')
    return mlb_keys, bert_model
