import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import requests
from PIL import Image

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

client = OpenAI()

# check OpenAI API key availability
if not OPENAI_API_KEY:
    st.error("Missing OpenAI API Key. Please set it in the .env file.")
    st.stop()
OpenAI.api_key = OPENAI_API_KEY

# Define selectable options
dict_list = {
    "genre": ["Mythology", "Sci-fi", "Fantasy", "Mystery", "Romance", "Horror"],
    "tone": ["Light-Hearted", "Serious/Dramatic", "Romantic", "Mysterious", "Cynical/Ironic", "Uplifting/Inspirational", "Satirical"],
    "mood": ["Joyful", "Melancholic/Sad", "Solemn", "Tense", "Eerie/Creepy", "Hopeful", "Whimsical"],
    "pov": ["Third-Person Limited", "First-Person", "Third-Person Omniscient"]
}

#function to generate story
def generate_story(scenario):
    prompt = f"""
    You are a story teller.
    Generate a short story (max 500 words) based on the following context:
    {scenario}
    """
    
    try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a creative storyteller."},
                        {"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=1
            )
            return completion["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"Error generating story: {e}")
        return

#fucntion to generate key events
def generate_key_events(story):
    prompt = f"""
    STORY: {story}
    give simple and small key events seperated by ","
    """

    try:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=1
                )
                return completion["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"Error generating key events: {e}")
        return

#function to generate key event visuals
def txt2img(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    if not HUGGINGFACE_API_KEY:
        st.error("Missing Hugging Face API Key. Please set it in the .env file.")
        return None
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        return Image.open(response.content)
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

#function to generate audio
def gen_audio(story):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": "Bearer {API_KEY}"}
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    audio_bytes = query({
        "inputs": story,
    })
    
    return audio_bytes

#Character info
def character_info(num_characters):
    character_data = [{'Name': '','Sex': '','Age': ''},
                      {'Name': '','Sex': '','Age': ''},
                      {'Name': '','Sex': '','Age': ''},
                      {'Name': '','Sex': '','Age': ''},
                      {'Name': '','Sex': '','Age': ''}]

    for i in range(num_characters):
        chara_name = st.text_input(f"Character {i + 1} Name:", max_chars=25, key=f"char_name_{i}")
        chara_sex = st.selectbox(f"{chara_name}'s Sex:", ["Male", "Female", "Other"], key=f"char_sex_{i}")
        chara_age = st.number_input(f"{chara_name}'s Age:", 1,value=1,step=1,key=f"char_age_{i}")
        
        character_data[i]['Name'] = chara_name
        character_data[i]['Sex'] = chara_sex
        character_data[i]['Age'] = chara_age
        

    return character_data

def main():
    st.title("StoryForge")
    genre = st.selectbox("Genre:", dict_list['genre'])
    no_of_characters = st.number_input("Number of Characters:",0,5,0,1)
    character_info_data = character_info(no_of_characters)
    major_events_data = st.text_input("Enter the major events(seperate them by commas): ")
    tone = st.selectbox("Tone:", dict_list['tone'])
    mood = st.selectbox("Mood:", dict_list['mood'])
    pov = st.selectbox("POV:", dict_list['pov'])
    readers_age = st.number_input("Reader's Age:",1,value=1,step=1)
    
    scenario = f"""Generate a {genre} story with the following characteristics:
    Genre: {genre}.
    Number of Main Characters: {no_of_characters}.
    Character Details: 
    Character 1: Name - {character_info_data[0]['Name']}, Sex - {character_info_data[0]['Sex']}, Age - {character_info_data[0]['Age']}
    Character 2 (if applicable): Name - {character_info_data[1]['Name']}, Sex - {character_info_data[1]['Sex']}, Age - {character_info_data[1]['Age']}
    Character 3 (if applicable): Name - {character_info_data[2]['Name']}, Sex - {character_info_data[2]['Sex']}, Age - {character_info_data[2]['Age']}
    Character 4 (if applicable): Name - {character_info_data[3]['Name']}, Sex - {character_info_data[3]['Sex']}, Age - {character_info_data[3]['Age']}
    Character 5 (if applicable): Name - {character_info_data[4]['Name']}, Sex - {character_info_data[4]['Sex']}, Age - {character_info_data[4]['Age']}
    Event Names: {major_events_data}
    Tone: {tone}.
    Mood: {mood}.
    Point of View (POV): {pov}.
    Reader's Age: {readers_age}.
    Please generate a story that aligns with these parameters. Thank you."""
    
    if st.button("Generate Story"):
        story = generate_story(scenario)
        st.write(story)
        
        audio_bytes = gen_audio(story)
        st.audio(audio_bytes,format="audio/wav")

        Key_Events = generate_key_events(story)
        split_result = Key_Events.split(', ')
        print(split_result)
        trimmed_list = [s.replace('\n', '') for s in split_result]

        img_bytes = [txt2img(item) for item in trimmed_list]
        for img_byte in img_bytes:
            st.image(img_byte)

        if st.button("Generate Image"):
            img = txt2img(scenario)
            if img:
                st.image(img)

if __name__ == '__main__':
    main()
