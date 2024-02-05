import streamlit as st
import datetime
import random
import csv
import pandas as pd
from openai import OpenAI
from googlesearch import search
from googleapiclient.discovery import build
client = OpenAI(api_key=st.secrets['openai']["openai_api_key"])
st.set_page_config(page_title='MoodTune Journal', page_icon='🥰', layout="wide")

st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');
        html, body, [class*="css"]  {
			font-family: 'Poppins', sans-serif;
		}
        h1{
            text-align: center;
        }
        [data-testid="stForm"] {
            background: #abdedb;
        }
        [data-testid=stSidebar] {
            background-color: #ADD8E6;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown('# :blue[MoodTune] Journal 🥰')

emotions = ["Anger", "Confused", "Disappointed", "Embarrassed", "Excited", "Fearful", 
            "Grateful", "Guilty", "Happy", "Insecure", "Jealous", "Proud", "Sad", 
            "Stressed", "Surprised"]
#list of google and youtube prompts for each emotion
prompts = {
    'Anger': {
        'Google': ['anger management techniques', 'how to calm down when angry', 'anger quotes'],
        'YouTube': ['anger management TED talk', 'calming music', 'inspirational videos for anger']
    },
    'Confused': {
        'Google': ['how to overcome confusion', 'clearing a confused mind', 'tips for clarity of thought'],
        'YouTube': ['explaining complex concepts', 'mind-clearing meditation', 'videos on understanding confusion']
    },
    'Disappointed': {
        'Google': ['coping with disappointment', 'motivational quotes after disappointment', 'bouncing back from letdowns'],
        'YouTube': ['overcoming setbacks video', 'uplifting music playlist', 'inspiring speeches']
    },
    'Embarrassed': {
        'Google': ['dealing with embarrassment', 'how to overcome embarrassment', 'coping with public embarrassment'],
        'YouTube': ['funny moments compilation', 'embarrassing stories shared', 'comedians handling embarrassment']
    },
    'Excited': {
        'Google': ['how to sustain excitement', 'capturing and embracing excitement', 'ideas for celebrating excitement'],
        'YouTube': ['high-energy workout videos', 'celebration moments compilation', 'uplifting music for excitement']
    },
    'Fearful': {
        'Google': ['overcoming fear', 'facing fears bravely', 'coping strategies for fear'],
        'YouTube': ['inspiring stories of overcoming fear', 'guided meditation for fear', 'motivational videos on conquering fear']
    },
    'Grateful': {
        'Google': ['cultivating gratitude', 'expressing gratitude daily', 'benefits of a grateful mindset'],
        'YouTube': ['gratitude journaling tutorial', 'inspiring gratitude stories', 'music for a thankful heart']
    },
    'Guilty': {
        'Google': ['coping with guilt', 'forgiving oneself', 'overcoming guilty feelings'],
        'YouTube': ['self-forgiveness guided meditation', 'personal stories of redemption', 'advice on dealing with guilt']
    },
    'Happy': {
        'Google': ['how to maintain happiness', 'scientifically proven ways to be happy', 'daily habits for lasting happiness'],
        'YouTube': ['uplifting moments compilation', 'happy dance videos', 'music for a joyful mood']
    },
    'Insecure': {
        'Google': ['building self-confidence', 'overcoming insecurities', 'tips for boosting self-esteem'],
        'YouTube': ['self-love affirmations', 'body-positive videos', 'personal growth talks']
    },
    'Jealous': {
        'Google': ['coping with jealousy', 'turning jealousy into motivation', 'strategies for overcoming envy'],
        'YouTube': ['stories of overcoming jealousy', 'mindfulness practices for jealousy', 'comedy sketches on jealousy']
    },
    'Proud': {
        'Google': ['cultivating a sense of pride', 'acknowledging achievements', 'benefits of feeling proud'],
        'YouTube': ['celebrating accomplishments video', 'inspiring success stories', 'music for feeling proud']
    },
    'Sad': {
        'Google': ['coping with sadness', 'lifting spirits during sadness', 'expressing and processing sadness'],
        'YouTube': ['comforting music playlist', 'motivational talks for overcoming sadness', 'inspirational stories of resilience']
    },
    'Stressed': {
        'Google': ['stress management techniques', 'relaxation methods during stress', 'tips for reducing stress levels'],
        'YouTube': ['stress-relief yoga videos', 'guided meditation for stress relief', 'calming nature scenes']
    },
    'Surprised': {
        'Google': ['embracing surprises', 'how to handle unexpected events', 'the science behind being surprised'],
        'YouTube': ['reaction to surprising news videos', 'unboxing and reaction videos', 'music for a surprised mood']
    }
}

def form_callback(data1, data2, data3, data4):
    header = ['Date', 'Emotion', 'Reason for emotion', 'Other Thoughts']
    with open('journal_entries.csv', 'a+', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerow([data1, data2, data3, data4])

# Encouraging message function
def generate_encouraging_message(emotion, text):
    prompt = f"I feel {emotion} because {text}. Provide me with an empathetic encouragement in 20 words." 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def search_youtube(query):
    youtube_api_key = st.secrets['youtube']["youtube_api_key"]
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    # Set up the search request
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=3  # Adjust based on your preference
    )

    # Execute the request
    response = request.execute()

    # Extract relevant information from the response
    video_results = [(item['snippet']['title'], f'https://www.youtube.com/watch?v={item["id"]["videoId"]}') for item in response['items']]

    return video_results


# Streamlit app
def main():
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
    # Streamlit form
        with st.form(key="My Journal", clear_on_submit=True):
            date = st.date_input("Date of entry", value= None,format="DD/MM/YYYY")
            selected_emotion = st.selectbox('How are you feeling?', options=emotions)
            context_text = st.text_area('What is making you feel this way?', max_chars=50)
            other_thoughts = st.text_area('Other Thoughts', max_chars=50)
            submitted = st.form_submit_button("Submit",type='secondary')

    with col2:
        if submitted:
            # Handle form submission
            form_callback(date,selected_emotion,context_text,other_thoughts)

            with st.container(border=True):
                st.subheader("Message: ", divider="rainbow")
                # Generate encouraging message
                encouraging_message = generate_encouraging_message(selected_emotion, context_text)
                st.markdown(encouraging_message)
                
                # google search enquiry
                with st.expander("You can visit these recommended Google sites!"):
                    google_prompt = random.choice(prompts[selected_emotion]['Google'])
                    google_search_results = list(search(google_prompt, num_results=3))
                    for i, result in enumerate(google_search_results, start=1):
                        st.write(f"{i}. {result}")

                # youtube search enquiry
                with st.expander("You can visit these recommended Youtube videos!"):
                    youtube_prompt = random.choice(prompts[selected_emotion]['YouTube'])
                    youtube_search_results = search_youtube(youtube_prompt)
                    for i, (title, video_url) in enumerate(youtube_search_results, start=1):
                        st.markdown(f"{i}. [{title}]({video_url})")
                



# Run the Streamlit app
if __name__ == "__main__":
    main()