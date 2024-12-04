from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from google.cloud import speech
from groq import Groq
import boto3
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize clients
s3 = boto3.client('s3')
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
speech_client = speech.SpeechClient()

# Configure speech recognition
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code="en-US",
    enable_automatic_punctuation=True,
)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_data')
def handle_audio_data(audio_data):
    try:
        # Process audio with GCP Speech-to-Text
        response = speech_client.recognize(
            config=config,
            audio=speech.RecognitionAudio(content=audio_data)
        )
        
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            
            # Generate summary with Groq
            summary = groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Summarize this lecture segment: {transcript}"
                }],
                model="mixtral-8x7b-32768"
            )
            
            # Store in S3
            timestamp = datetime.now().isoformat()
            s3.put_object(
                Bucket=os.getenv('S3_BUCKET'),
                Key=f"lectures/{timestamp}",
                Body=transcript
            )
            
            # Send back to client
            emit('transcription', {
                'transcript': transcript,
                'summary': summary.choices[0].message.content
            })
            
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)