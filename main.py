from flask import Flask, request, jsonify

from algo_tfidf import FomoTfidf
from resource_data import ResourceEprint

app = Flask(__name__)

@app.route('/api/similar-titles', methods=['POST'])
def get_similar_titles():
    input_data = request.get_json()

    if 'title' not in input_data:
        return jsonify({"error": "Title is required"}), 400

    input_title = input_data['title']
    response = fomo_tfidf.search_similar(input_title)
    return jsonify(response)


if __name__ == '__main__':

    res = ResourceEprint([
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2015/JSON/if_2015.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2016/JSON/if_2016.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2017/JSON/if_2017.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2018/JSON/if_2018.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2019/JSON/if_2019.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2020/JSON/if_2020.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2021/JSON/if_2021.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2022/JSON/if_2022.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2023/JSON/if_2023.js",
        "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2024/JSON/if_2024.js"
    ])
    collections = res.process()
    fomo_tfidf = FomoTfidf()
    fomo_tfidf.save_data_on_initialization(collections)
    app.run(debug=True)
