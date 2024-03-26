import requests
from service import Service
import constants
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def some_endpoint():

    # Make a request to a specific endpoint of the third-party API
    params = {
            'key': constants.BACK_UP_API_KEY,
            'q': constants.Query, 
            'part': constants.Snippet,
        }
    response = requests.get(constants.THIRD_PARTY_API_BASE_URL,params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response data and extract relevant information
        data = response.json()
        service = Service()
        service.preprocess_data_and_insert(data)

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
def search_videos():
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
