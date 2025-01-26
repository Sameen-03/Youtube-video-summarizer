import streamlit as st
import assemblyai as aai
from pytubefix import YouTube
import ollama

# Streamlit App
st.title("YouTube Video Summarizer")

# User input: YouTube video link
yt_link = st.text_input("Enter the YouTube video URL:")

# Set AssemblyAI API Key
aai.settings.api_key = "ed7a2d6f98c941a18a7b640c6bc35a1b"  # Replace with your actual API key

def download_video(link):
    """Download the YouTube video and return the file path."""
    try:
        yt_object = YouTube(link,'WEB')
        video = yt_object.streams.get_highest_resolution()
        video_path = video.download()
        return video_path, yt_object.title
    except Exception as e:
        st.error(f"An error occurred when downloading the video: {e}")
        return None, None

def get_transcript(video_path):
    """Transcribe the video and return the subtitles."""
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(video_path)
        subtitles = transcript.export_subtitles_srt()
        return subtitles
    except Exception as e:
        st.error(f"An error occurred when transcribing the video: {e}")
        return None

def summarize_transcript(transcript):
    """Summarize the transcript using Ollama and return the summary."""
    try:
        client = ollama.Client()
        model = 'llama3.2:1b'
        prompt = f"Summarize this video transcript for me:\n\n{transcript}"
        response = client.generate(model=model, prompt=prompt)
        return response.response
    except Exception as e:
        st.error(f"An error occurred when summarizing the transcript: {e}")
        return None

# Process Workflow
if yt_link:
    with st.spinner("Downloading video..."):
        video_path, video_title = download_video(yt_link)

    if video_path:
        st.success(f"Video '{video_title}' downloaded successfully.")

        with st.spinner("Transcribing video..."):
            transcript = get_transcript(video_path)

        if transcript:
            st.success("Transcription completed.")
            st.text_area("Transcript", transcript, height=300)

            with st.spinner("Summarizing transcript..."):
                summary = summarize_transcript(transcript)

            if summary:
                st.success("Summary completed.")
                st.text_area("Video Summary", summary, height=200)

# Note: Replace YOUR_ASSEMBLYAI_API_KEY with your AssemblyAI API key to make it work.
