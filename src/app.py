import streamlit as st
from phi.tools.youtube_tools import YouTubeTools
from db_functions import save_video_info
# import logging
from logger_config import setup_logger
from assistant import get_chunk_summarizer, get_video_summarizer  

logger = setup_logger('ai-youtube')

st.set_page_config(
    page_title="Youtube Video Summaries",
)
st.title("Local Video Summaries")

LIST_MODELS = ["llama3", "phi3", "qwen2", "mistral"]
llm_model = "llama3"
transcript = ""

def main() -> None:
    # Get model
    llm_model = st.sidebar.selectbox("Select Model", options=LIST_MODELS)
    logger.debug(f"Selected model: {llm_model}")
    # Set assistant_type in session state
    if "llm_model" not in st.session_state:
        st.session_state["llm_model"] = llm_model
    # Restart the assistant if assistant_type has changed
    elif st.session_state["llm_model"] != llm_model:
        st.session_state["llm_model"] = llm_model
        st.rerun()

    # Get chunker limit
    chunker_limit = st.sidebar.slider(
        ":heart_on_fire: Words in chunk",
        min_value=1000,
        max_value=10000,
        value=4500,
        step=500,
        help="Set the number of characters to chunk the text into.",
    )

    # Get video url
    video_url = st.sidebar.text_input(":video_camera: Video URL")
    logger.debug(f"Video URL: {video_url}")
    # Button to generate report
    generate_report = st.sidebar.button("Generate Summary")
    if generate_report:
        st.session_state["youtube_url"] = video_url

    video_data = None # starting empty
    if "youtube_url" in st.session_state:
        _url = st.session_state["youtube_url"]
        youtube_tools = YouTubeTools()
        video_captions = None
        video_summarizer = get_video_summarizer(model=llm_model)
        logger.debug(f"video_summarizer: {video_summarizer}")   
        with st.status("Parsing Video", expanded=False) as status:
            with st.container():
                video_container = st.empty()
                video_container.video(_url)

            # Get video data from youtube
            video_data = youtube_tools.get_youtube_video_data(_url)

            with st.container():
                video_data_container = st.empty()
                video_data_container.json(video_data)
            status.update(label="Video", state="complete", expanded=False)

        with st.status("Reading Captions", expanded=False) as status:
            video_captions = youtube_tools.get_youtube_video_captions(_url)
            logger.debug(f"Video captions: {video_captions[:300]}")
            with st.container():
                video_captions_container = st.empty()
                video_captions_container.write(video_captions)
            status.update(label="Captions processed", state="complete", expanded=False)

        if not video_captions:
            logger.error("No video captions found.")
            st.write("Sorry could not parse video. Please try again or use a different video.")
            return

        chunks = []
        num_chunks = 0
        words = video_captions.split()
        for i in range(0, len(words), chunker_limit):
            num_chunks += 1
            chunks.append(" ".join(words[i : (i + chunker_limit)]))
        logger.debug(f"Chunks: {chunks}")   
        if num_chunks > 1:
            chunk_summaries = []
            for i in range(num_chunks):
                with st.status(f"Summarizing chunk: {i+1}", expanded=False) as status:
                    chunk_summary = ""
                    chunk_container = st.empty()
                    chunk_summarizer = get_chunk_summarizer(model=llm_model)
                    chunk_info = f"Video data: {video_data}\n\n"
                    chunk_info += f"{chunks[i]}\n\n"
                    for delta in chunk_summarizer.run(chunk_info):
                        chunk_summary += delta  # type: ignore
                        chunk_container.markdown(chunk_summary)
                    chunk_summaries.append(chunk_summary)
                    status.update(label=f"Chunk {i+1} summarized", state="complete", expanded=False)
            logger.debug(f"Chunk summaries: {chunk_summaries}") 
            with st.spinner("Generating Summary"):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += "Summaries:\n\n"
                for i, chunk_summary in enumerate(chunk_summaries, start=1):
                    video_info += f"Chunk {i}:\n\n{chunk_summary}\n\n"
                    video_info += "---\n\n"

                for delta in video_summarizer.run(video_info):
                    summary += delta  # type: ignore
                    summary_container.markdown(summary)
        else:
            with st.spinner("Generating Summary"):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += f"Captions: {video_captions}\n\n"

                for delta in video_summarizer.run(video_info):
                    summary += delta  # type: ignore
                    summary_container.markdown(summary)
    else:
        st.write("Please provide a video URL.")

    if video_data is not None:
        save_video_info(video_url, video_data, video_captions, transcript, summary, llm_model)  
    else:
        logger.error("No video data found.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.rerun()

main()
