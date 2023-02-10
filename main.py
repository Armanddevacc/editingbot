from pydub import AudioSegment
import requests
import json
import openai
from moviepy.editor import *
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_videoclips as mp




# Language of the soundtrack
language = 'en'

#variable initialisation:
outputs = []
urls=[]
video_path='video.mp4'

# API key for Pexels API
API_KEY = "YOUR KEY HERE"
# API key for OpenIA API
openai.api_key = "YOUR KEY HERE"


#text example
text1="""The sun was shining brightly on the green grass as Jenny strolled through the park. She felt the warmth on her skin and breathed in the fresh air. She smiled, feeling grateful for the beautiful day.

Jenny's best friend, Sarah, was waiting for her on a bench under a large tree. Sarah had brought a picnic basket filled with all of Jenny's favorite snacks. Jenny was so happy to see her.

"""


text = """Have you heard about the new AI language model called ChatGPT? Developed by OpenAI, this model is making waves in the AI community with its advanced conversational abilities. And the best part? It could potentially be monetized!

According to an article on Search Engine Journal, ChatGPT could be used in a number of ways to generate revenue. For example, businesses could use the model to improve customer service by allowing it to handle repetitive or basic customer queries. This would free up human customer service representatives to focus on more complex inquiries.

Another way that ChatGPT could be monetized is by allowing developers to access its API for use in their own applications. This would give businesses access to the powerful conversational abilities of ChatGPT, allowing them to enhance the user experience for their customers.

But that's not all! ChatGPT could also be used for content creation, such as generating articles or social media posts. This could help businesses save time and resources, while still delivering high-quality content to their audience.

It's amazing to think about the endless possibilities that ChatGPT could offer. And with its advanced AI capabilities, it's clear that the future of AI is looking brighter than ever. So, what do you think about the potential monetization of ChatGPT? Let us know in the comments!"""










def get_duration(filename):
    sound = AudioSegment.from_file(filename,format="mp3")
    return sound.duration_seconds


def text_to_speech(text,i):
    # Create gTTS object
    tts = gTTS(text, lang=language)

    # Save the audio file
    tts.save("output"+str(i)+".mp3")





def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Please summarize each paragraph into a small list of simple words describing the theme the atmosphere to picture the paragraph: " + text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summarized_text = response["choices"][0]["text"].strip()

    # Split the summarized text into a list of words
    summarized_words = summarized_text.split()
    return summarized_words

def summarize_text_by_paragraph(text):
    # Split the text into paragraphs
    paragraphs = text.split("\n")

    # Summarize each paragraph
    summarized_paragraphs = []
    i=1
    for paragraph in paragraphs:
        if len(paragraph)!=0:
            print(paragraph)
            print("output"+str(i)+".mp3 loaded")
            text_to_speech(paragraph,i)
            duration=get_duration("output"+str(i)+".mp3")
            summarized_paragraphs.append([summarize_text(paragraph),duration])


            i=i+1
        
    return summarized_paragraphs




def get_video_url(words, duration):
    # construct the API request URL
    query = "+".join(words)
    # API request URL
    orientation= "landscape"
    if horizontal==False:
            orientation= "portrait" 

    api_url = f"https://api.pexels.com/v1/videos/search?query={query}&duration={duration}&orientation={orientation}&per_page=1&page=1"

    # make the API request
    response = requests.get(api_url, headers={"Authorization": API_KEY})

    # parse the API response
    data = json.loads(response.text)

    # return the video URL
    return data["videos"][0]["video_files"][0]["link"]


def get_video(url, duration, words, i):
    my_video_file = VideoFileClip(url).subclip(0, duration)

    video_url = get_video_url(words, duration)
 
    if my_video_file.duration > duration:
        my_video_file = VideoFileClip(video_url).subclip(0, duration)
    elif my_video_file.duration < duration: 
        # find a new video 
        video_url2 = get_video_url(words, duration - my_video_file.duration)

        # combine two videos 
        my_video_file2 = VideoFileClip(video_url2).subclip(0, duration - my_video_file.duration)
        my_video_file = mp.concatenate_videoclips([my_video_file, my_video_file2])

    #soundtrack
    if voice == True:

        if os.path.isfile("output" + str(i) + ".mp3"):
            soundtrack = AudioFileClip("output" + str(i) + ".mp3")
            my_video_file = my_video_file.set_audio(soundtrack)
        else:
            print("ERROR: 'output" + str(i) + ".mp3' not found")


    # Finally, save the video
    my_video_file.write_videofile("my_video"+str(i)+".mp4")


# Function to process a list of words with a given duration
def process_list_of_words(words):
    i=1
    for word,duration in words:
        # Get the video URL and download the video
        video_url = get_video_url(word, duration)
        get_video(video_url, duration, word, i)
        i=i+1
    merge_videos(i)
from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(i):
    filenames=[]
    video_clips = []
    for y in range(1,i):
        filenames.append("my_video"+str(y)+".mp4")
    for filename in filenames:
        clip = VideoFileClip(filename).resize(height=1080) # set the height to 1080
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=1920, height=1080) # set the width to 1920 and height to 1080
        clip = clip.set_fps(30) # set the frame rate to 30
        video_clips.append(clip)

    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile("merged_video.mp4")







'''
-----------------------------------------------------------
                    initialisation
----------------------------------------------------------
'''


# Take answers from the user


horizontal = bool
while horizontal != True and horizontal!= False:
    horizontal = input('Do you want the format of the video to be horizontal otherwise it will be vertical.Please enter Yes/No: ')
    if horizontal == "Yes" or horizontal == "Y" or horizontal == "y":
        horizontal = True
    elif horizontal == "No" or horizontal == "N":
        horizontal = False
    else:
        print("That is not a valid answer.")


voice = bool
while voice != True and voice!= False:
    voice = input('Do you want your video to have robot voiceover.Please enter Yes/No: ')
    if voice == "Yes" or voice == "Y" or voice == "y":
        voice = True
    elif voice == "No" or voice == "N":
    # Do something if user does not agree.
        voice = False
    else:
        print("That is not a valid answer.")


import tkinter

# create main window
root = tkinter.Tk()

text_label = tkinter.Label(root, text='Please enter a text with multiple paragraphs:')
text_label.pack()

text_input = tkinter.Text(root)
text_input.pack()

submit_button = tkinter.Button(root, text="Validate", command=lambda: validate_input(text_input))
submit_button.pack()

def validate_input(text_input):

    text_input=text_input.get("1.0","end-1c")
    root.destroy()
    summarized_text = summarize_text_by_paragraph(text_input)
    process_list_of_words(summarized_text)

root.mainloop()




