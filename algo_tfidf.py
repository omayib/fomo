import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib

class FomoTfidf:
    def __init__(self):
        self.VECTOR_FILE = "model/title_vectors.joblib"
        self.VECTORIZER_FILE = "model/vectorizer.joblib"
        self.TITLES_FILE = "model/existing_titles.joblib"
        self.COLLECTION_FILE = "model/existing_collection.joblib"

    def save_data_on_initialization(self, collections):
        titles = [project['title'] for project in collections]
        # Check if the files already exist
        if not (os.path.exists(self.VECTOR_FILE)
                and os.path.exists(self.VECTORIZER_FILE)
                and os.path.exists(self.TITLES_FILE)
                and os.path.exists(self.COLLECTION_FILE)):
            print("Files not found, initializing and saving data...")

            vectorizer = TfidfVectorizer().fit(titles)
            title_vectors = vectorizer.transform(titles)

            joblib.dump(title_vectors, self.VECTOR_FILE)
            joblib.dump(vectorizer, self.VECTORIZER_FILE)
            joblib.dump(titles, self.TITLES_FILE)
            joblib.dump(collections, self.COLLECTION_FILE)

            print("Data initialized and saved.")
        else:
            print("Files already exist. No need to reinitialize.")

    def load_data(self):
        if os.path.exists(self.TITLES_FILE) \
                and os.path.exists(self.VECTOR_FILE) \
                and os.path.exists(self.VECTORIZER_FILE) \
                and os.path.exists(self.COLLECTION_FILE):
            existing_titles = joblib.load(self.TITLES_FILE)
            vectorizer = joblib.load(self.VECTORIZER_FILE)
            title_vectors = joblib.load(self.VECTOR_FILE)
            collections = joblib.load(self.COLLECTION_FILE)
            return existing_titles, vectorizer, title_vectors, collections
        else:
            return [], None, None, None

    # Save the updated titles, vectorizer, and vectors
    def save_data(self, titles, vectorizer, vectors, collection):
        joblib.dump(titles, self.TITLES_FILE)
        joblib.dump(vectorizer, self.VECTORIZER_FILE)
        joblib.dump(vectors, self.VECTOR_FILE)
        joblib.dump(collection, self.COLLECTION_FILE)

    def search_similar(self,input_title):
        # Vectorize the input title
        title, vectorizer, title_vectors, collections = self.load_data()

        input_vector = vectorizer.transform([input_title])

        # Compute the cosine similarity between the input and existing titles
        cosine_similarities = cosine_similarity(input_vector, title_vectors).flatten()

        # Get the indices of the most similar titles (e.g., top 3)
        top_indices = cosine_similarities.argsort()[-3:][::-1]

        # Retrieve the most similar titles along with their similarity scores
        similar_titles = [{"title": collections[i]['title'],
                           "date": collections[i]['date'],
                           "author": collections[i]['author'],
                           "nim": collections[i]['nim'],
                           "supervisor": collections[i]['supervisor'],
                           "similarity": cosine_similarities[i]} for i in top_indices if
                          cosine_similarities[i] > 0.1]
        # Return the results as a JSON response
        result = {"input_title": input_title, "similar_titles": similar_titles}
        return result
