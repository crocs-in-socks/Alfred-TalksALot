import json
import random
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer = WordNetLemmatizer()

intents = json.loads(open("Code\intents.json").read())

words = []
data = []
categories = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        data.append((tokens, intent['tag']))
        if intent['tag'] not in categories:
            categories.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words]
words = sorted(set(words))
categories = sorted(categories)

pickle.dump(words, open('inputs.pkl', 'wb'))
pickle.dump(categories, open('categories.pkl', 'wb'))

training_data = []

for datum in data:
    pattern = datum[0]
    pattern = [lemmatizer.lemmatize(word.lower()) for word in pattern]
    bag = []
    output = []
    for word in words:
        if word in pattern:
            bag.append(1)
        else:
            bag.append(0)
    for category in categories:
        if category == datum[1]:
            output.append(1)
        else:
            output.append(0)
    training_data.append([bag, output])

# So essentially individual words are features for our model, and every row in the dataset we train our model on consists of the one-hot encoded values of the words as features and the one-hot encoded values of the categories as outputs.

random.shuffle(training_data)
training_data = np.array(training_data, dtype='object')

X_train = list(training_data[:,0])
y_train = list(training_data[:,1])

# building the model

model = tf.keras.models.Sequential()

input_layer = tf.keras.layers.Dense(256, activation='relu', input_shape=(len(X_train[0]),))
input_dropout = tf.keras.layers.Dropout(0.5)
layer_1 = tf.keras.layers.Dense(128, activation='relu')
layer_1_dropout = tf.keras.layers.Dropout(0.5)
layer_2 = tf.keras.layers.Dense(64, activation='relu')
layer_2_dropout = tf.keras.layers.Dropout(0.5)
output_layer = tf.keras.layers.Dense(len(y_train[0]), activation='softmax')

model.add(input_layer)
model.add(input_dropout)
model.add(layer_1)
model.add(layer_1_dropout)
model.add(layer_2)
model.add(layer_2_dropout)
model.add(output_layer)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

alfred = model.fit(np.array(X_train), np.array(y_train), epochs=256, batch_size=4, verbose=1)
model.save('alfred_model.h5', alfred)

print("Alfred has been potty trained.")