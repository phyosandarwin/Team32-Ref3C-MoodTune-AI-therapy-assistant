import streamlit as st
import speech_recognition as sr
from st_audiorec import st_audiorec
from openai import OpenAI
import tempfile
import os

client = OpenAI(api_key=st.secrets['openai']["openai_api_key"])
st.set_page_config(page_title='MoodTune Chatbot', page_icon='🥰')
st.markdown("""
        <style>
        html, body, [class*="css"]  {
			font-weight:600;
		}
        h1{
            text-align: center;
        }
        div.row-widget.stRadio > div{
            flex-direction:row;
            border-radius:10px;
            padding:5px;
            background: #cbdbf5;
        }
        [data-testid=stSidebar] {
            background-color: #ADD8E6;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown('# :blue[MoodTune] Chatbot 🥰')
st.subheader(body='', divider='rainbow')

# Function to convert speech to text with automatic stop
def speech_to_text(audio_data, temp_filename):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio_data)
    except sr.UnknownValueError:
        text= "Could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results; {e}"
    finally:
        # Clean up temporary file
        if temp_filename:
            print(f"Cleaning up temporary file: {temp_filename}")
            os.unlink(temp_filename)
        else:
            text = "No audio input is received"
    return text

# Function to start recording with automatic stop
# Function to start recording audio
def start_recording_audio():
    wav_audio_data = st_audiorec()
    if wav_audio_data:
        global temp_filename
        # Write audio data to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(wav_audio_data)
            temp_filename = temp_file.name
        r = sr.Recognizer()
        with sr.AudioFile(temp_filename) as source:
            # Record the audio file
            audio_data = r.record(source)
        st.session_state['audio_data'] = audio_data

#################################################################################################
# Radio button to select input mode
input_mode = st.sidebar.radio("Select Input Mode", ["Text", "Voice"], key="input_mode")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if input_mode == "Voice":
    start_recording_audio()

# Display chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
                                 {"role": "assistant", "content": "Hello I am MoodTune, your personal therapist chatbot! On the sidebar, please select how you wish to input your feelings :)"}]

# Display chat messages from history within the last 24 hours
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(name=role, avatar=avatar):
        st.markdown(content)

# User input handling based on selected mode
if input_mode == "Text":
    if prompt := st.chat_input("Message MoodTune chatbot..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(name="user", avatar="👤"):
            st.markdown(prompt)
else:
    audio_data = st.session_state.get('audio_data')
    if audio_data:
        text = speech_to_text(audio_data, temp_filename)
        st.session_state.messages.append({"role": "user", "content": text})
        with st.chat_message(name="user", avatar="👤"):
            st.markdown(text)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar='🤖'):
        with st.spinner("Thinking..."):
            response_content = ""
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "user", "content": st.session_state.messages[-1]["content"]},  # Include only the latest user message
                ],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response_content += chunk.choices[0].delta.content
            st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})


