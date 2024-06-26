# YouTube Video Fetch API

This project provides an API for fetching the latest videos from YouTube based on a predefined search query.
The API continuously calls the YouTube API in the background with a specified interval to fetch the latest videos,
stores them in a database, and provides endpoints for retrieving and searching the stored video data.


## Setup Instructions

### Prerequisites:
1. Python 3.x
2. MySQL Server


### Installation
To run the server and test the API locally, follow these steps:
  1. Clone the repository:
     ```
     git clone https://github.com/pulkit-iiith/fampay.git
      ```
     
  3. Navigate to the project directory:
     ```
     cd fampay
     ```
  3. Build and start docker server:
     ```
     docker-compose up -d
     ```
    
Once the containers are up and running, you can access the API endpoints.

## API Endpoints:

  1. Fetch Latest Videos
      - Endpoint: /videos
      - Method: GET
      - Parameters:
    
        
            - page (optional): Page number for pagination (default: 1)
            - per_page (optional): Number of videos per page (default: 10)
  2. Search Videos
      - Endpoint: /search
      - Method: GET
      - Parameters:
    
        
            - title (optional): Search query for video title
            - description (optional): Search query for video description
   
## Testing the API :

  You can test the API endpoints using tools like cURL or Postman. Here are some examples:

      1. Fetch Latest Videos
      
      curl http://localhost:5001/videos
      
      2. Search Videos
      
      curl http://localhost:5001/search?title=your_query_here

## Updating key and Query:

We have a docker-compose.yml file which contains all the environments variables which looks like:-
```
version: '3'

services:
  flask-app:
    build: .
    ports:
     - "5001:5000"
    volumes:
     - .:/app
    depends_on:
      - mysql
    environment:
      - YOUTUBE_API_BASE_URL=https://www.googleapis.com/youtube/v3/search
      - API_KEY=AIzaSyCWwKUkm6ENnEEao3agXpteS9UBWRkv41w
      - BACK_UP_API_KEY=AIzaSyB2qJK3vjvKE-Egpbrs0IXFX5A3lMm3MpI
      - QUERY = modi
      - MYSQL_HOST=mysql
      - MYSQL_USER=admin
      - MYSQL_PASSWORD=admin 
      - MYSQL_DATABASE=test

  mysql:
    image: mysql:latest
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=admin
      - MYSQL_PASSWORD=admin
      - MYSQL_DATABASE=test
      - MYSQL_ROOT_PASSWORD=admin

    ports:
      - "3306:3306"

```
Here you can change below details accordingly
- API_KEY=AIzaSyCWwKUkm6ENnEEao3agXpteS9UBWRkv41w
- BACK_UP_API_KEY=AIzaSyB2qJK3vjvKE-Egpbrs0IXFX5A3lMm3MpI
- QUERY = modi
      
  
