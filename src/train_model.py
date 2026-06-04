import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

data = pd.read_csv("dataset/training_data.csv")

X = data["question"]
y = data["sql"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

pickle.dump(model, open("models/sql_generator.pkl","wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl","wb"))

print("Model Trained")