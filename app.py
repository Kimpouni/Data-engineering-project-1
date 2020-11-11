from flask import Flask, request, render_template

import json
import pickle
import nltk
import string
import re
import nltk.stem
import numpy
#from nltk.classify import NaiveBayesClassifier
#from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)
#preprocess the text
def Preprocessing(data):
	nltk.download('stopwords')
	nltk.download('PorterStemmer')
	stemmer = nltk.stem.PorterStemmer("english")
	data = re.sub(r"http\S+", "", data).lower().replace('.','').replace(';','').replace('-','').replace(':','')
	stopwords = set(nltk.corpus.stopwords.words('english'))
	words = [stemmer.stem(i) for i in data.split() if not i in stopwords]
	return (" ".join(words))
#def preprocessing2(txt):
#	tweet=[]
#	tweet.append(txt)
	
#	vectorizer = CountVectorizer(analyzer="word")
#	return vectorizer.fit_transform(tweet)
#load the trained model and do prediction

def predict (txt):
	
	prediction = model.classify(txt)
	return prediction

#return the prediction 
def submit_txt(txt):
	txt = Preprocessing(txt)
	
	#txt=preprocessing2(txt)
	category = predict(txt)
	if category==1 :
		return 'Positive'
	if category==-1 :
		return 'Negative'
	if category==0 :
		return 'Neutral'
	return 'FAIL'
	
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		details = request.form	
		if details['form_type'] == 'submit_txt':
			return submit_txt(details['txt'])
	return render_template('Interface.html')

if __name__ == '__main__':
	model = pickle.load(open('PredictionsCategory.pkl', 'rb'))
	app.run(host='127.0.0.1')