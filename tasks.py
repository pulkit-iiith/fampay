import requests
from data_preprocessing import Data_preprocessing
from service import Service
from flask import Flask, jsonify, request
app = Flask(__name__)

THIRD_PARTY_API_BASE_URL = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyCk_JQ8qohmT6uoucQQ4o7ULktfYSor9wc&q=modi&part=snippet'

@app.route('/', methods=['POST'])
def some_endpoint():
    # Make a request to a specific endpoint of the third-party API
    response = requests.get(THIRD_PARTY_API_BASE_URL)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response data and extract relevant information
        data = response.json()
        data_preprocess = Data_preprocessing()
        data_preprocess.trigger_processing(data)
        # Process the data as needed
        return jsonify(data)
    else:
        # Return an error response if the request was not successful
        return jsonify({'error': 'Failed to fetch data from third-party API'}), 500

@staticmethod
@app.route('/videos', methods=['GET'])
def get_videos():
    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default to page 1 if not provided
    per_page = int(request.args.get('per_page', 10))  # Default to 10 videos per page if not provided
    service = Service()
    response = service.get_videos(page,per_page)

    return jsonify(response)

@app.route('/search', methods=['GET'])
def search():
    # Get search queries from request parameters
    title_query = request.args.get('title')
    description_query = request.args.get('description')

    if title_query and description_query:
        service = Service()
        response = service.search_videos(title_query,description_query)
        print(response)
        return jsonify(response)

    else:
        return jsonify({'error': 'Both title and description query parameters are required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
