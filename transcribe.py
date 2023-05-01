# Importing required libraries

from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
from dotenv import load_dotenv, find_dotenv

# Using OpenAI API to generate text summaries
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

# Creating a function to generate text completion based on the given prompt using OpenAI API.
def get_completion(prompt, model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# This functionExtracts business ideas from a YouTube video transcript using OpenAI text generation API
def extract_ideas(vid_id):
    # Getting transcript from youtube video
    srt = YouTubeTranscriptApi.get_transcript(vid_id)
    # Creating an empty list to store ideas scrapped from parts of the video
    ideas = [] 
    # Splitting the entrire into batches so that doesn't exceed openai api limit
    for i in range(1,(len(srt)//100)+1):
        print(i)
        s1= srt[100*(i-1):i*100]
        prompt = f"""
        Your task is to summarise all business ideas being discussed in the YouTube video \
        from the transcript of the video. 
        Make sure you read through the entire transcript first and then summarise.
        The format should be
        Idea 1: ......
        Idea 2: ......
        .
        .
        Idea N: .....
        Summarize the transcript given below, delimited by triple 
        backticks. 
        output as a list
        transcript: ```{s1}```
        """

        response = get_completion(prompt)
        ideas.append(response)
    # Secondary prompt for 
    prompt1 = f"""
    Your task is to summarise all the business into full business ideas based on the \
    list of ideas given. Make sure first you go through all the ideas, then combine all the ideas\
    that are for same category and write them as one idea after summeririzing them.
    The format should be
    Idea 1 (Title of idea): Description of that entire idea
    Idea 2 (Title of idea): Description of that entire idea
    .
    .
    Idea N (Title of idea): Description of that entire idea
    Get the list of ideas given below, delimited by triple 
    backticks. 
    list ideas: ```{ideas}```
    """

    response1 = get_completion(prompt1)
    return response1

# Define the video ID for the YouTube video
video_id = "7x5M4lxK-dw"
# Calling the function defined above
list_idea = extract_ideas(video_id)
print(list_idea)
