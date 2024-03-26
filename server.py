import asyncio
import requests
from data_preprocessing import Data_preprocessing
from service import Service
from flask import Flask, jsonify, request
import threading
app = Flask(__name__)

YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyCk_JQ8qohmT6uoucQQ4o7ULktfYSor9wc&q=modi&part=snippet'

# YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyAyfaoLiqvPnuFbFlBazUuNoUsAb4qR_-Emodi&part=snippet'

async def fetch_data():
    while True:
        # Make a request to the YouTube API
        response = requests.get(YOUTUBE_API_BASE_URL)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data and extract relevant information
            data = response.json()
            data_preprocess = Data_preprocessing()
            data_preprocess.trigger_processing(data)
            # Process the data as needed
            print("Data fetched successfully:")
        else:
            # Log an error if the request was not successful
            print("Failed to fetch data from YouTube API")

        # Sleep for 10 seconds before making the next request
        await asyncio.sleep(10)

# @app.route('/some-endpoint')
# def some_endpoint():
#     # Dummy endpoint for demonstration purposes
#     return jsonify({'message': 'Hello from Flask!'})
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
        return jsonify(response)

    else:
        return jsonify({'error': 'Both title and description query parameters are required'}), 400

# if __name__ == '__main__':
#     # Start the background task
#     asyncio.run(fetch_data())
    
#     # Run the Flask application
#     app.run(debug=True)

if __name__ == '__main__':
    # Start the background task in a separate thread
    asyncio.run(fetch_data())
    # threading.Thread(target=app.run, kwargs={'debug': True}).start()
    threading.Thread(target=app.run, kwargs={'debug': True, 'port': 5002}).start()

