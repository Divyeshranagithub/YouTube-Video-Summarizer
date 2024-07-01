from groq import Groq
import streamlit as st
import validators
from preprocess import get_transcript, generate_chat_responses

client = Groq(
    api_key=st.secrets["groq_api"],
)
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.image('youtube logo.png', width=50 , )
st.subheader("YouTube Summarizer", divider="rainbow", anchor=False)
if url := st.text_input("Enter YouTube video URL:"):
    if validators.url(url) and "youtube.com" in url:
        prompt = get_transcript(url)
        st.session_state.messages.append({"role": "user", "content": prompt})
        if not prompt:
            st.stop()
        try:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the content of the YouTube video provided below. Your summary should be concise and capture the main points of the video. Please ensure that the summary is coherent and free of grammatical errors."
                    },
                    {
                        "role": "user",
                        "content": st.session_state.messages[0]['content']
                    },
                    # {"role": m['role'], "content": m['content']}for m in st.session_state.messages
                ],
                max_tokens=8192,
                stream=True,
            )

            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)
            if isinstance(full_response, str):
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                combined_response = "\n".join(str(item) for item in full_response)
                st.session_state.messages.append({"role": "assistant", "content": combined_response})
        except Exception as e:
            st.error(e, icon="🚨")
    else:
        st.warning("Please enter a valid YouTube video URL!",  icon="⚠️")
        st.stop()









