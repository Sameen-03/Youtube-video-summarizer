import os
import assemblyai as aai
from pytubefix import YouTube
import ollama

# Set AssemblyAI API Key
aai.settings.api_key = "Your_API_key"  # Set your API key as an environment variable
yt_link = input("Enter the YouTube video URL: ")
yt_object = YouTube(yt_link,'WEB')
# Function to download the YouTube video
def download_video():
    try:
        yt_object = YouTube(yt_link,'WEB')
        print(f"Downloading: {yt_object.title}")
        video = yt_object.streams.get_highest_resolution()

        # Set the download path
        video.download()
        print(f"Video downloaded successfully to")

    except Exception as e:
        print(f"An error occurred when downloading the video: {e}")
        return None

# Function to get the transcript
def get_transcript():
    try:
        print("Transcribing video...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(f'{yt_object.title}.mp4')
        print("Transcription completed.")
        subtitles = transcript.export_subtitles_srt()
        return subtitles
    except Exception as e:
        print(f"An error occurred when transcribing the video: {e}")
        return None

# Function to summarize the transcript with Ollama
def summarize_transcript(transcript):
    try:
        print("Summarizing the transcript using Ollama...")
        client = ollama.Client()
        model = 'name_of_your_local_model' #example: 'llama3.2:2b'
        prompt = f"Summarize this video transcript for me:\n\n{transcript}"

        response = client.generate(model=model, prompt=prompt)
        print("Video summary:\n")
        print(response.response)
    except Exception as e:
        print(f"An error occurred when summarizing the transcript: {e}")

# Main Process
if __name__ == "__main__":
    # Step 1: Download the video
    download_video()
    transcript = get_transcript()
    summarize_transcript(transcript)
