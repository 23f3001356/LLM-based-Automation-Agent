import os
import openai

def execute_task_b8(audio_path, output_file):
    """
    Transcribes audio from an MP3 file using OpenAI's Whisper model and saves it to a text file.
    Args:
        audio_path (str): Path to the MP3 audio file.
        output_file (str): Path where transcription will be saved.
    Returns:
        str: Success or error message.
    """
    try:
        # Set API key from environment variable
        openai.api_key = os.environ["AIPROXY_TOKEN"]

        # Open the audio file
        with open(audio_path, "rb") as audio_file:
            # Call OpenAI Whisper API for transcription
            response = openai.Audio.transcribe("whisper-1", audio_file)
        
        # Extract transcription text
        transcription = response.get("text", "").strip()

        # Save transcription to the output file
        with open(output_file, "w") as f:
            f.write(transcription)

        return f"Task B8 completed successfully. Transcription saved to {output_file}."
    
    except Exception as e:
        return f"Error executing Task B8: {str(e)}"