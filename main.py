from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resource_data import ResourceEprint
import os
import joblib

app = Flask(__name__)

VECTOR_FILE = "model/title_vectors.joblib"
VECTORIZER_FILE = "model/vectorizer.joblib"
TITLES_FILE = "model/existing_titles.joblib"
COLLECTION_FILE = "model/existing_collection.joblib"

# Example list of existing titles to compare with the input
# collections = [
#     {'title': 'sistem monitoring akuarium berbasis internet of things',
#      'date': '2023-03-27',
#      'author': 'ahmad irsyad zulfikar',
#      'nim': '18.11.2322',
#      'supervisor': 'sudarmawan sudarmawan'},
#
#     {'title': 'sistem monitoring akuarium berbasis internet of things',
#      'date': '2023-03-27',
#      'author': 'ahmad irsyad zulfikar',
#      'nim': '18.11.2322',
#      'supervisor': 'sudarmawan sudarmawan'}
# ]



# Precompute the TF-IDF vectors for the existing titles
# vectorizer = TfidfVectorizer().fit(titles)
# title_vectors = vectorizer.transform(titles)


def save_data_on_initialization(collections):
    titles = [project['title'] for project in collections]
    # Check if the files already exist
    if not (os.path.exists(VECTOR_FILE)
            and os.path.exists(VECTORIZER_FILE)
            and os.path.exists(TITLES_FILE)
            and os.path.exists(COLLECTION_FILE)):
        print("Files not found, initializing and saving data...")

        # Initialize the TfidfVectorizer and vectorize the initial titles
        vectorizer = TfidfVectorizer().fit(titles)
        title_vectors = vectorizer.transform(titles)

        # Save the vectorizer, vectors, and titles to files using joblib
        joblib.dump(title_vectors, VECTOR_FILE)
        joblib.dump(vectorizer, VECTORIZER_FILE)
        joblib.dump(titles, TITLES_FILE)
        joblib.dump(collections, COLLECTION_FILE)

        print("Data initialized and saved.")
    else:
        print("Files already exist. No need to reinitialize.")

def load_data():
    if os.path.exists(TITLES_FILE) \
            and os.path.exists(VECTOR_FILE) \
            and os.path.exists(VECTORIZER_FILE) \
            and os.path.exists( COLLECTION_FILE):
        existing_titles = joblib.load(TITLES_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
        title_vectors = joblib.load(VECTOR_FILE)
        collections = joblib.load(COLLECTION_FILE)
        return existing_titles, vectorizer, title_vectors, collections
    else:
        return [], None, None, None

# Save the updated titles, vectorizer, and vectors
def save_data(titles, vectorizer, vectors, collection):
    joblib.dump(titles, TITLES_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    joblib.dump(vectors, VECTOR_FILE)
    joblib.dump(collection, COLLECTION_FILE)


@app.route('/api/similar-titles', methods=['POST'])
def get_similar_titles():
    # Get the input title from the JSON request body
    input_data = request.get_json()

    if 'title' not in input_data:
        return jsonify({"error": "Title is required"}), 400

    input_title = input_data['title']

    # Vectorize the input title
    title, vectorizer, title_vectors, collections = load_data()

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
    return jsonify({"input_title": input_title, "similar_titles": similar_titles})


if __name__ == '__main__':

    res = ResourceEprint([
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2024/JSON/if_2024.js"
    ])
    collections = res.process()

    save_data_on_initialization(collections)
    app.run(debug=True)
