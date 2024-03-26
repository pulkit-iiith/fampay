# YouTube Video Fetch API

This project provides an API for fetching the latest videos from YouTube based on a predefined search query.
The API continuously calls the YouTube API in the background with a specified interval to fetch the latest videos,
stores them in a database, and provides endpoints for retrieving and searching the stored video data.


## Setup Instructions


### Prerequisites:
1. Python 3.x
2. MySQL Server


### Installation
  1. Clone the repository:
     ```
     git clone https://github.com/yourusername/youtube-video-fetch-api.git
      ```
     
  3. Navigate to the project directory:
     ```
     cd youtube-video-fetch-api
     ```
     
  5. Install dependencies:
     ```
     pip3 install -r requirements.txt
     ```
     
  7. Set up MySQL database:
     - Install MySQL server if not already installed.
     - Create a MySQL database and configure the connection parameters in config.py.


### Usage
  1. Run the server:
     ```
     python3 server.py
     ```
  3. Access the API endpoints.
  



## API Endpoints:

  1. Fetch Latest Videos
      - Endpoint: /videos
      - Method: GET
      - Parameters:
            - page (optional): Page number for pagination (default: 1)
            - per_page (optional): Number of videos per page (default: 10)
  2. Search Videos
      - Endpoint: /videos
      - Method: GET
      - Parameters:
            - title (optional): Search query for video title
            - description (optional): Search query for video description
   
## Testing the API :

  You can test the API endpoints using tools like cURL or Postman. Here are some examples:

      1. Fetch Latest Videos
      
      curl http://localhost:5000/videos
      
      2. Search Videos
      
      curl 'http://localhost:5000/search?title=your_query_here'
  