a quick start guide on how to use this:

first collect the proper api keys:
GROQ_API_KEY=your_groq_key
GCP_PROJECT_ID=your_gcp_project
S3_BUCKET=your_bucket_name
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
here is a .env file for you to replicate

first complete these installs:
pip install fastapi uvicorn google-cloud-speech groq boto3 python-dotenv
npm install react react-dom websocket

then start the servers:
uvicorn server:app --reload
npm start

this app is able to:
record audio from browser, process it with GCP, summarize it with Grpq and then store the data using S3.
The browser is updated in real time. 

####   TO DO #####
add zoom integratoin
