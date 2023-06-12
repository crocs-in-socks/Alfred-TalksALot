import json
import random
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

import tensorflow as tf

lemmatizer = WordNetLemmatizer()

intents = json.loads(open(r"Code\\intents.json").read())
inputs = pickle.load(open(r'inputs.pkl', 'rb'))
categories = pickle.load(open(r'categories.pkl', 'rb'))
model = tf.keras.models.load_model(r'alfred_model.h5')

def clean_query(query):
    query_words = nltk.word_tokenize(query)
    query_words = [lemmatizer.lemmatize(word.lower()) for word in query_words]
    return query_words

def one_hot_encode(query):
    query_words = clean_query(query)
    bag = [0] * len(inputs)
    for query_word in query_words:
        for idx, word in enumerate(inputs):
            if word == query_word:
                bag[idx] = 1
    
    return bag

def predict_tag(query):
    bag = one_hot_encode(query)
    # model.predict returns a list with one item inside it. To unwrap that item we do [0]
    predictions = model.predict(np.array([bag]))[0]
    
    ERROR_THRESHOLD = 0.25
    predictions = [[i, p] for i, p in enumerate(predictions) if p > ERROR_THRESHOLD]

    predictions.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for prediction in predictions:
        return_list.append({"intent": categories[prediction[0]], "probability": str(prediction[1])})
    return return_list

def respond(query):
    predicted_tag = predict_tag(query)[0]["intent"]

    response = "I couldn't quite catch that."

    for intent in intents["intents"]:
        if intent["tag"] == predicted_tag:
            response = random.choice(intent["responses"])
            if(response == "Your next line will be..."):
                print(response)
                response = input()
            # doinator(predicted_tag)
            break

    return response

def doinator(predicted_tag):

    if predicted_tag == "ThinkAlfredThink":
        print("What is the corrected tag smartass?")
        corrected_tag = input()
        for intent in intents["intents"]:
            if intent["tag"] == corrected_tag:
                intent["patterns"].append(query)
                break
        # with open(r"Code\\intents.json", "w") as intents_file:
        #     json.dump(intents, intents_file, indent=4)
        print("You said ", query)
        print("The intents file has been updated.")
    
    return

query = input()
history = [query]

while query != "bye":
    print(respond(query))
    query = input()
    history.append(query)
