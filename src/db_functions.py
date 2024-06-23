# This database is designed to support operations such as inserting new video entries, querying existing ones based on various criteria (e.g., author, video title, or timestamp), and potentially updating or deleting records. The use of a primary key (`id`) facilitates efficient retrieval and manipulation of specific video records.

import os
import json
import sqlite3
from datetime import datetime
import logging
from logger_config import setup_logger
logger = setup_logger('ai-youtube')

# Read configuration file
script_dir = os.path.dirname(os.path.realpath(__file__))
relative_config_path = os.path.join(script_dir, '..', 'conf', 'system_config.json')
config_path = os.path.abspath(relative_config_path)
with open(config_path, 'r') as file:
    config = json.load(file)

# Extract database parameters
db_name = config['db_name']
linux_data_folder = config['linux_data_folder']


DATABASE = linux_data_folder + db_name + '.db'

def create_connection():
    """
    Creates a connection to the SQLite database.

    Returns:
        conn (sqlite3.Connection): The connection object to the database.
    """
    logger.info(f"connecting to DATABASE = {DATABASE}")

    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")
        return None
    
    return conn


def create_table():
    """
    Creates the 'videos' table in the database if it doesn't exist.
    """
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
    """
    Saves video information to the database.

    Args:
        video_url (str): The URL of the video.
        video_data (str or dict): The data of the video in JSON format or a dictionary.
        caption (str): The caption of the video.
        transcript (str): The transcript of the video.
        summary (str): The summary of the video.
        model (str): The model used for processing the video.

    Returns:
        None
    """
    if isinstance(video_data, str):
        video_data = json.loads(video_data)

    video_title = video_data['title']
    author_url = video_data['author_url']
    author_name = video_data['author_name']
    timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    logger.debug(f"Video title: {video_title}, URL: {video_url}, Author: {author_name}, Timestamp: {timestamp}\n\n")

    try:
        conn = create_connection()
    except Exception as e:
        logger.error(f"Error in save_video_info to the DB: {e}")
        return None
    
    query = '''INSERT INTO videos(video_title, video_url, author_url, author_name, caption, transcript, summary, model, timestamp) 
                VALUES(?,?,?,?,?,?,?,?,?);'''
   
    cursor = conn.cursor()
    cursor.execute(query, (video_title, video_url, author_url, author_name, caption, transcript, summary, model, timestamp))
    conn.commit()
    
    cursor.close()
    conn.close()

def main():
    # This art of the script can be used to create the database and the table, just once or for testing purposes.

    # create_connection()
    # create_table()

    # Example for testing video_data structure: [video_title, author_name, author_url, video_url, caption, transcript, summary, model]
    # save_video_info( "http://video.url", "video_data", "Sample Caption", "Sample Video transcript", "Sample Summary", "Sample Model")

    pass

if __name__ == "__main__":
    main()