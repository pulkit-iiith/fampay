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


class KeysExhaustedError(Exception):
    pass

async def fetch_data():

    primary_key = constants.API_KEY
    backup_key = constants.BACK_UP_API_KEY
    current_key = primary_key  # Start with the primary key

    while True:
        params = {
            'key': current_key,
            'q': constants.Query, 
            'part': constants.Snippet,
        }
        url = constants.THIRD_PARTY_API_BASE_URL
        # Make a request to the YouTube API
        response = requests.get(url,params=params)

        try:
            # Make a request to the YouTube API
            response = requests.get(url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response data and extract relevant information
                data = response.json()
                service = Service()
                service.preprocess_data_and_insert(data)
                # Process the data as needed
                print("Data fetched successfully:")
            elif response.status_code == 403 and current_key == primary_key:
                # If primary key is exhausted, switch to backup key
                print("Primary API key exhausted, switching to backup key")
                current_key = backup_key
            elif response.status_code == 403 and current_key == backup_key:
                # If backup key is also exhausted, raise custom exception
                raise KeysExhaustedError("Both API keys are exhausted")
            else:
                # Log an error if the request was not successful
                print("Failed to fetch data from YouTube API")
        except (requests.exceptions.ConnectionError, KeysExhaustedError) as e:
            # Handle connection error and raise custom exception
            print(e)
            break


        # Sleep for 10 seconds before making the next request
        await asyncio.sleep(10)

def start_fetch_data():
    asyncio.run(fetch_data())

if __name__ == '__main__':
    # Start fetching data in a separate thread
    threading.Thread(target=start_fetch_data, daemon=True).start()
    # Run the Flask application
    app.run(debug=True, port=5000)


