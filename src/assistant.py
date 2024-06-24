# This file (assistant.py) serves as a utility within a project focused on processing and summarizing YouTube video content. Its primary purpose is to define and configure two specialized assistants, get_chunk_summarizer and get_video_summarizer, which are designed to work with video data extracted from YouTube. These assistants leverage advanced natural language processing (NLP) capabilities to perform specific tasks related to video summarization.


from textwrap import dedent
from phi.llm.ollama import Ollama
from phi.assistant import Assistant
from read_config import PROMPT_CHUNK_DESCRIPTION, PROMPT_CHUNK_INSTRUCTIONS, PROMPT_CHUNK_ADD_TO_PROMPT, PROMPT_SUMM_DESCRIPTION, PROMPT_SUMM_INSTRUCTIONS, PROMPT_SUMM_ADD_TO_PROMPT

def get_chunk_summarizer(
    model: str = "llama3",
    debug_mode: bool = True,
) -> Assistant:
    """
    Returns an Assistant object for chunk summarization of a YouTube video transcript.

    Args:
        model (str, optional): The model to be used for summarization. Defaults to "llama3".
        debug_mode (bool, optional): Whether to enable debug mode. Defaults to True.

    Returns:
        Assistant: The Assistant object for chunk summarization.
    """

    return Assistant(
        name="youtube_pre_processor_ollama",
        llm=Ollama(model=model),
        description=PROMPT_CHUNK_DESCRIPTION,
        instructions=PROMPT_CHUNK_INSTRUCTIONS,
        add_to_system_prompt=dedent(PROMPT_CHUNK_ADD_TO_PROMPT),
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )


def get_video_summarizer(
    model: str = "llama3",
    debug_mode: bool = True,
) -> Assistant:
    """
    Returns an Assistant object for summarization of a YouTube video.

    Args:
        model (str, optional): The model to be used for summarization. Defaults to "llama3".
        debug_mode (bool, optional): Whether to enable debug mode. Defaults to True.

    Returns:
        Assistant: The Assistant object for video summarization.
    """
    return Assistant(
        name="video_summarizer_ollama",
        llm=Ollama(model=model),
        description=PROMPT_SUMM_DESCRIPTION,
        instructions=PROMPT_SUMM_INSTRUCTIONS,
        add_to_system_prompt=dedent(PROMPT_SUMM_ADD_TO_PROMPT),
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
