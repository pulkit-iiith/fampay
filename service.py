from insert_data_in_database import Insert_data_in_database


class Service:
    def get_videos(self,page,per_page):

        insert_data_in_database = Insert_data_in_database()
        # Fetch video data
        video_data = insert_data_in_database.fetch_videos(page, per_page)

        # Format response
        response = []
        for video in video_data:
            response.append({
                'title': video[1],
                'description': video[2],
                'publishing_datetime': str(video[3]),
                'thumbnails': {
                    'default': video[4],
                    'medium': video[5],
                    'high': video[6]
                }
            })

        return response
    
    def search_videos(self,title_query,description_query):

        insert_data_in_database = Insert_data_in_database()
        # Perform search
        search_results = insert_data_in_database.search_videos(title_query, description_query)

        # Format response
        response = []
        for video in search_results:
            response.append({
                'title': video[1],
                'description': video[2],
                'publishing_datetime': str(video[3]),
                'thumbnails': {
                    'default': video[4],
                    'medium': video[5],
                    'high': video[6]
                }
            })
        return response