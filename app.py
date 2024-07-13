from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()  # loading all the environment variables

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question, image=None):
    predefined_responses = {
        "who are you": "I am a Chatbot created by SOUVIK.",
        "describe yourself": "I am an AI-powered chatbot created by SOUVIK to assist with various tasks and provide information.",
        "tell me about yourself": "I am a chatbot developed by SUN, designed to help you with queries and provide useful information.",
        "who is anirban tung": "Anirban is an Indian boy, known as GAMLA",
        "who is md ayan sk": "Ayan is an Indian boy, who always ride bike over 100 km/h speed.😁"
    }
    
    question_lower = question.lower()
    
    if question_lower in predefined_responses:
        return predefined_responses[question_lower]
    else:
        if image:
            response = model.generate_content([question, image])
        else:
            response = model.generate_content(question)
        return response.text

# Function to handle vision mode
def vision_mode():
    st.session_state.show_vision_mode = True
    
    input_text = st.text_input("Input Prompt:", key="vision_input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Tell me about the image"):
            with st.spinner("Generating response..."):
                response = get_gemini_response(input_text, image=image)
            st.subheader("Response")
            st.write(response)
    
    # Button to switch back to normal mode
    if st.button("Back to Chat", on_click=switch_to_normal_mode):
        st.session_state.show_vision_mode = False

# Function to switch back to normal mode
def switch_to_normal_mode():
    st.session_state.show_vision_mode = False

# Initialize Streamlit app
st.set_page_config(page_title="ChatBOT", page_icon=":robot_face:", layout="wide")

# Custom CSS and SVG Background
st.markdown("""
    <style>
            .stApp {
            color: white;
            background-color: #1a237e; /* Dark blue background color */
            background-image: linear-gradient(43deg, #000000 0%, #1a237e 30%, #6a1b9a 70%, #000000 100%); /* Initial gradient */
        }
        
        .times-new-roman-heading {
            font-family: 'Times New Roman', Times, serif;
            text-align: center;
            font-size: 64px;
            background: linear-gradient(175deg, #0072ff, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            padding: 10px 0;
            animation: color-animation 5s infinite alternate; /* Animation applied */
        }

        @keyframes color-animation {
            0% {
                color: #0072ff; /* Start color (blue) */
            }
            50% {
                color: #ffffff; /* Middle color (white) */
            }
            100% {
                color: #0072ff; /* End color (blue) */
            }
        }
        .chat-container {
            background-color: rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin: 20px 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .chat-box {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .user-msg, .bot-msg {
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            word-wrap: break-word;
            color: black;
            background-color: white;
        }

        .user-msg {
            align-self: flex-end;
            border-radius: 15px 15px 0 15px;
        }

        .bot-msg {
            align-self: flex-start;
            border-radius: 15px 15px 15px 0;
        }

        .stButton>button {
            background: none;
            color: white;
            border: 1px solid white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 25px;
            margin: 5px;
            transition: background 0.3s, color 0.3s;
        }

        .stButton>button:hover {
            background: white;
            color: black;
        }

        .submit-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 5px;
        }

        .submit-btn:hover {
            background-color: #45a049;
        }

        .clear-btn {
            background-color: #f44336;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 5px;
        }

        .clear-btn:hover {
            background-color: #e53935;
        }

        .header {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
        }

        .footer {
            text-align: center;
            margin-top: 75px;
            font-size: 15px;
            color: white;
        }

        .footer a {
            color: white;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        .chat-input-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            background-color: #f44336;
            color: white;
        }

        .chat-input-container .stTextInput>div>input {
            height: 40px;
            width: 400px;
            border-radius: 25px;
            background-color: #f44336;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='times-new-roman-heading'>Orion AI</h1>", unsafe_allow_html=True)

def handle_input():
    question = st.session_state.input
    if not question.strip():
        st.error("Empty message. Please write a question.")
        return
    
    with st.spinner("Generating response..."):
        response = get_gemini_response(question)
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    st.session_state.chat_history.append({"user": question, "bot": response})
    st.session_state.input = ""

def clear_history():
    if "chat_history" in st.session_state:
        del st.session_state.chat_history

# Center-aligned text input box
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
st.text_input("Ask me anything:", key="input", on_change=handle_input, placeholder="Type your question here...", help=" Type your question here ")

st.markdown("</div>", unsafe_allow_html=True)

# Create columns with minimal gap
col1, col2 = st.columns([1, 6])
with col1:
    st.button("Ask the question", on_click=handle_input)
with col2:
    st.button("Clear Chat", on_click=clear_history)

# Display chat history if exists
if "chat_history" in st.session_state:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        st.markdown(f"""
            <div class='chat-box'>
                <div class='user-msg'>{chat['user']}</div>
                <div class='bot-msg'>{chat['bot']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer with Instagram link
st.markdown("<div class='footer'>Developed by SOUVIK <a href='https://www.instagram.com/sun007_/' target='_blank'><img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' style='width: 20px; vertical-align: middle; margin-left: 5px;' /></a></div>", unsafe_allow_html=True)


