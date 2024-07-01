import re
from typing import Generator
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st

def get_transcript(url):
    url_data = urlparse(url)
    try:
        video_id = parse_qs(url_data.query)["v"][0]
        if not video_id:
            st.error('Video ID not found.')
        formatter = TextFormatter()
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
        text = formatter.format_transcript(transcript)
        text = re.sub('\s+', ' ', text).replace('--', '')
        return text

    except Exception as e:
        st.warning(f"Please Not Upload YouTube Short Video Link", icon="⚠️")
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
