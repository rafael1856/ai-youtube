# db_functions.py
import os
import json
import sqlite3
from datetime import datetime


# Read configuration file
script_dir = os.path.dirname(os.path.realpath(__file__))
relative_config_path = os.path.join(script_dir, '..', 'conf', 'system_config.json')
config_path = os.path.abspath(relative_config_path)
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract database parameters
db_name = config['db_name']
linux_data_folder = config['linux_data_folder']
# USER = config['db_user']
# PASSWORD = config['db_password']

DATABASE = linux_data_folder + db_name + '.db'

def create_connection():

    print("DATABASE = ", DATABASE)

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    return conn


def create_table():
   
   conn = create_connection()
   cursor = conn.cursor()
   
   cursor.execute('''CREATE TABLE IF NOT EXISTS videos (                    
                  id INTEGER PRIMARY KEY,                      
                  video_title TEXT NOT NULL, 
                  video_url TEXT NOT NULL, 
                  author_url TEXT NOT NULL, 
                  author_name TEXT NOT NULL,                           
                  caption TEXT,                          
                  transcript TEXT,                           
                  summary TEXT NOT NULL,                           
                  model TEXT NOT NULL,                          
                  timestamp TEXT NOT NULL);''' )
   
   conn.commit()
   cursor.close()
   conn.close()

def save_video_info(video_url, video_data, caption, transcript, summary, model):

    # print("\n\n----------------- video_data", video_data)
    
    if isinstance(video_data, str):
        video_data = json.loads(video_data)

    video_title = video_data['title']
    author_url = video_data['author_url']
    author_name = video_data['author_name']
    timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # print(f"Video title: {video_title}, URL: {video_url}, Author: {author_name}, Timestamp: {timestamp}\n\n")

    try:
        conn = create_connection()
    except Exception as e:
        print(e)
        return None
    
    query = '''INSERT INTO videos(video_title, video_url, author_url, author_name, caption, transcript, summary, model, timestamp) 
                VALUES(?,?,?,?,?,?,?,?,?);'''
   
    cursor = conn.cursor()
    cursor.execute(query, (video_title, video_url, author_url, author_name, caption, transcript, summary, model, timestamp))
    conn.commit()
    
    cursor.close()
    conn.close()

def main():
     # Example video_data structure: [video_title, author_name, author_url, video_url, caption, transcript, summary, model]

    #  save_video_info(video_url, video_data, caption, transcript, summary, model)
     save_video_info( "http://video.url", "video_data", "Sample Caption", "Sample Video transcript", "Sample Summary", "Sample Model")

    # video_data = ["http://video.url", "video_data", "Sample Caption", "Sample Video transcript", "Sample Transcript", "Sample Summary", "Sample Model"]
    # "Author Name", "http://author.url",

    # insert_video_data(video_data)
    # create_connection()
    # create_table()
    # pass

if __name__ == "__main__":
    main()