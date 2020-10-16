from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from flask import json

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words_list = set(stopwords.words('english'))
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def to_lower_case(text):
    return text.lower()

def remove_URLs(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'', text)

def remove_HTMLs(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)

def remove_annotations(text):
    annotation = re.compile(r'\[[^]]*\]')
    return annotation.sub(r'', text)

def remove_punctuations(text):
    punctuation = re.compile(r'[^a-zA-Z0-9]+')
    return punctuation.sub(r' ', text)

def remove_stopwords(text):
    text = text.split()
    text = [word for word in text if word not in stop_words_list]
    return ' '.join(text)

def pos_recognition(tag):
    if (tag[0] == 'J'):
        return 'a'
    if (tag[0] == 'N'):
        return 'n'
    if (tag[0] == 'R'):
        return 'r'
    if (tag[0] == 'V'):
        return 'v'
    return ''

def lemmatization(text):
    text = nltk.pos_tag(text.split())
    for i in range(len(text)):
        if (pos_recognition(text[i][1]) != ''):
            text[i] = lemmatizer.lemmatize(text[i][0], pos = pos_recognition(text[i][1]))
        else:
            text[i] = lemmatizer.lemmatize(text[i][0])
    return ' '.join(text)

@app.route('/dataCleaning')
def dataCleaning():
    orginal_title = str(request.args.get('title'))
    orginal_content = str(str(request.args.get('content')))

    final_title = to_lower_case(orginal_title)
    final_content = to_lower_case(orginal_content)

    final_title = remove_URLs(final_title)
    final_content = remove_URLs(final_content)

    final_title = remove_HTMLs(final_title)
    final_content = remove_HTMLs(final_content)

    final_title = remove_annotations(final_title)
    final_content = remove_annotations(final_content)

    final_title = remove_punctuations(final_title)
    final_content = remove_punctuations(final_content)

    final_title = remove_stopwords(final_title)
    final_content = remove_stopwords(final_content)

    final_title = lemmatization(final_title)
    final_content = lemmatization(final_content)

    return jsonify(
        orginal_title = orginal_title,
        orginal_content = orginal_content,
        final_title = final_title,
        final_content = final_content
    )

import keras
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import load_model
import pickle

with open('./saved_model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

json_file = open('./saved_model/model_num.json', 'r')

loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("./saved_model/model_num.h5")

loaded_model.save('./saved_model/model_num.hdf5')
loaded_model = load_model('./saved_model/model_num.hdf5')

@app.route('/getTheTruth')
def getTheTruth():   #Load tokenizer
    test_input = [str(request.args.get('title'))+' '+str(str(request.args.get('content')))]

    tokenized_test = tokenizer.texts_to_sequences(test_input)
    test_input = keras.preprocessing.sequence.pad_sequences(tokenized_test, maxlen=300)

    prediction = loaded_model.predict_classes(test_input)
    answer = 1

    if (prediction[0][0] == 0):
        answer = 0

    return jsonify(
        answer = answer
    )

if __name__ == "__main__":
    app.run(port = 8001, debug = True)
