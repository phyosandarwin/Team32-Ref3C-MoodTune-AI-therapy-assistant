import streamlit as st
import speech_recognition as sr
from openai import OpenAI

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
def speech_to_text_with_auto_stop():
    text = ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        st.write("Say something...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(mic, duration=1)

        # Start listening with a timeout for automatic stop
        audio = recognizer.listen(mic, timeout=4)  # Set a timeout (e.g., 30 seconds)

    try:
        text = recognizer.recognize_google(audio)
        #st.write("You said:", text)
    except sr.UnknownValueError:
        st.write("Could not understand audio")
    except sr.RequestError as e:
        st.write(f"Could not request results; {e}")
    return text

# Function to start recording with automatic stop
def start_recording_auto_stop():
    st.session_state.recording_started = True
    # Process speech to text with automatic stop and store the result in the session state
    st.session_state['text'] = speech_to_text_with_auto_stop()
    # Automatic stop recording by setting the flag to False
    st.session_state.recording_started = False

# Function to stop recording
def stop_recording():
    # Here, you might want to add any clean-up or stop logic if necessary
    st.session_state.recording_started = False

# Radio button to select input mode
input_mode = st.sidebar.radio("Select Input Mode", ["Text", "Voice"], key="input_mode")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if input_mode == "Voice":
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False
    
    # Display a centered start button
    start_button = st.button("Start Recording", on_click=start_recording_auto_stop, type="primary")

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
    if st.session_state.get('text', ''):
        st.session_state.messages.append({"role": "user", "content": st.session_state['text']})
        with st.chat_message(name="user", avatar="👤"):
            st.markdown(st.session_state['text'])

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


