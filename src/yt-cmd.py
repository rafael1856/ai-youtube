import argparse
from phi.tools.youtube_tools import YouTubeTools
from db_functions import save_video_info
import logging
from logger_config import setup_logger
from assistant import get_chunk_summarizer, get_video_summarizer
from read_config import LIST_MODELS, DATA_FOLDER

logger = setup_logger('ai-youtube-cmd')
print("LIST_MODELS: ", LIST_MODELS )

llm_model = "llama3"
chunker_limit = 4500


def process_video(video_url):
    transcript = ""
    video_data = ""
    video_captions = ""

    youtube_tools = YouTubeTools()
    video_captions = None
    video_summarizer = get_video_summarizer(model=llm_model)

    logger.debug(f"video_summarizer: {video_summarizer}")     
    # Get video data from youtube
    video_data = youtube_tools.get_youtube_video_data(video_url)
    logger.debug(f"Video data: {video_data}")    

    video_captions = youtube_tools.get_youtube_video_captions(video_url)
    logger.debug(f"Video captions: {video_captions[:300]}")
        
    if not video_captions:
        logger.error("No video captions found.")
        return
    
    # chunks = [video_captions]
    chunks = []
    num_chunks = 0
    words = video_captions.split()
    for i in range(0, len(words), chunker_limit):
        num_chunks += 1
        chunks.append(" ".join(words[i : (i + chunker_limit)]))
    logger.debug(f"Chunks: {chunks}")   

    if num_chunks < 1:
        print("Error: ",num_chunks)
        return

    if num_chunks > 1:
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            chunk_summary = ""
            chunk_summarizer = get_chunk_summarizer(model=llm_model)
            chunk_info = f"Video data: {video_data}\n\n"
            chunk_info += f"{chunk}\n\n"
            for delta in chunk_summarizer.run(chunk_info):
                chunk_summary += delta  
            chunk_summaries.append(chunk_summary)
            logger.debug(f"Chunk summaries: {chunk_summaries}")    
            
            summary = ""
            for delta in video_summarizer.run("\n".join(chunk_summaries)):
                summary += delta 
    else: # case chunk = 1
        logger.debug("Going to summarize directly - chunk = 1")
        summary = ""
        video_info = f"Video URL: {video_url}\n\n"
        video_info += f"Video Data: {video_data}\n\n"
        video_info += f"Captions: {video_captions}\n\n"

        for delta in video_summarizer.run(video_info):
            logger.debug("delta: ", delta)
            summary += delta  

    # save to database
    if video_data is not None:
        save_video_info(video_url, video_data, video_captions, transcript, summary, llm_model)  
    else:
        logger.error("No video data found.")

    # Save results to a text document, at the data folder
    # with video_title name
    video_title = video_data['title']
    output =  f"{DATA_FOLDER}{video_title}_summary.txt"
    with open(output, "w") as file:
        file.write(f"Video URL: {video_url}\n\n")
        file.write(f"Video Data: {video_data}\n\n")
        file.write(f"Captions: {video_captions}\n\n")
        file.write(f"Summary:\n\n{summary}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a YouTube video.')
    parser.add_argument('--video-url', required=True, help='URL of the YouTube video to process.')
    args = parser.parse_args()

    process_video(args.video_url)