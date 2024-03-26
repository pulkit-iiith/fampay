import asyncio
import requests
from service import Service
import constants
from flask import Flask, jsonify, request
import threading
app = Flask(__name__)


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
        return jsonify(response)

    else:
        return jsonify({'error': 'Both title and description query parameters are required'}), 400


async def fetch_data():
    while True:
        params = {
            'key': constants.API_KEY,
            'q': constants.Query, 
            'part': constants.Snippet,
        }
        # Make a request to the YouTube API
        response = requests.get(constants.THIRD_PARTY_API_BASE_URL,params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data and extract relevant information
            data = response.json()
            service = Service()
            service.trigger_processing(data)
            # Process the data as needed
            print("Data fetched successfully:")
        else:
            # Log an error if the request was not successful
            print("Failed to fetch data from YouTube API")

        # Sleep for 10 seconds before making the next request
        await asyncio.sleep(10)

def start_fetch_data():
    asyncio.run(fetch_data())

if __name__ == '__main__':
    # Start fetching data in a separate thread
    threading.Thread(target=start_fetch_data, daemon=True).start()
    # Run the Flask application
    app.run(debug=True, port=5000)


