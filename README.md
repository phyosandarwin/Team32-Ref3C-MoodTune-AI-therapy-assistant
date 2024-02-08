# MoodTuneAI (Techfest 2024 Hackathon Product)
MoodTune AI Assistant is a Streamlit-built virtual companion designed to enhance emotional wellness through AI-driven conversations. It listens, analyzes emotions, and offers personalized suggestions to improve users’ moods, functioning through both text and voice inputs.

## Inspiration 💡
1. To address growing mental health concerns in Singapore
2. Growing demand for mental health and therapy services yet increasing costs for these services
3. To provide a more personalized, safe, easily accessible, non-judgemental space to share and record feelings/experiences

## What it does 🤔
The chatbot acts as a virtual listener, paying attention to the user’s messages and understanding the context. It responds with empathy and acknowledges the user’s emotions, validating their experiences.
The journaling feature allows the user to jot down their emotions and experiences on a day-to-day basis. The diary entry is analyzed and an encouraging text is provided by the system along with other suggestions and ways for user’s to improve their mood.
The dashboard keeps an account of the users’ diary entries allowing them to reflect and review their emotions and feelings over the past few days. 

## How we built it 👩‍💻
We built the web application by using Streamlit. With the use of GPT3.5 Turbo API, we carried out chatbot text generation and encouragement message generation tasks. We also used Youtube APIs and did Google Web Scraping to return recommendation sites and videos.

## Challenges we ran into 
The largest challenge we ran into was finding an available API to use for generation. We were looking for free options and tried using online models and GPT2, however the outputs were disappointing. We finally decided to sign up for GPT 3.5 and the generated responses and recommendations were finally satisfiable.
Thus the better the API, the better the responses were for our chatbot prototype. 

## Accomplishments that we're proud of 💪
We’re proud of creating a chatbot that actually generates a response that a therapist would and we are proud of being able to incorporate speech to text function into our chatbot. We are also very proud of being able to create a working web prototype and accomplish what we initially wanted to. 

## What we learnt 💭
We learnt many different tasks of generative AI, usage of APIs, especially the stark difference in quality of output between them.
We also learnt to leverage different component features of Streamlit. 

## What's next for MoodTune 🤷‍♀️
* With datasets trained on psychotherapy data, we could fine tune the model to be able to craft a specific therapist's response. 
* We could allow for users to rant through video and get responses for it directly. 
