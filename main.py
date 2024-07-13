from dotenv import load_dotenv
import streamlit as st
import os
# from PIL import Image
import google.generativeai as genai
import datetime
import urllib.parse

# Load environment variables
load_dotenv()  # loading all the environment variables

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question, image=None):
    predefined_responses = {
        "who are you": "I am a Chatbot created by SUN.",
        "describe yourself": "I am an AI-powered chatbot created by SUN to assist with various tasks and provide information.",
        "tell me about yourself": "I am a chatbot developed by SUN, designed to help you with queries and provide useful information.",
        "who is anirban tung": "Anirban is an Indian boy, known as GAMLA😁",
        "who is md ayan sk": "Ayan is an Indian boy, who always rides a bike over 100 km/h speed.😁",
        "who is srijan hudait": "Srijan Hudait is an Indian boy, who is known as Rising Star.😁",
        "who is arijit jana": "Arijit Jana is an Indian boy who fell in love with Susmita.😁"

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



# Initialize Streamlit app
st.set_page_config(page_title="DinoAI", page_icon=":robot_face:", layout="wide")

# Custom CSS for white background and black text
st.markdown("""
    <style>
        .stApp {
            background-color: white; /* Fallback color */
            background-image: linear-gradient(to bottom, white); /* Gradient from white to light grey */
        }

        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }

        .header-logo {
            width: 64px; /* Adjust the size as needed */
            margin-right: 10px;
        }

        .times-new-roman-heading {
            font-family: 'Times New Roman', Times, serif;
            text-align: center;
            font-size: 64px;
            background: black;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 10px 0;
            animation: color-animation 5s infinite alternate;
        }

        @keyframes color-animation {
            0% {
                color: #0072ff;
            }
            50% {
                color: #ffffff;
            }
            100% {
                color: #0072ff;
            }
        }

        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 20px 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 400px; /* Set a max height for the chat container */
            overflow-y: auto; /* Enable vertical scrolling */
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
            color: white;
            background-color: black;
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
            color: black;
            border: 1px solid black;
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
            background: black;
            color: white;
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
            color: black;
        }

        .footer a {
            color: black;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        .chat-input-container {
            display: flex;
            justify-content: center;
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 10px;
            background-color: white;
            z-index: 1000;
            border-top: 1px solid #ccc;
        }

        .chat-input-container .stTextInput>div>input {
            height: 40px;
            width: 400px;
            border-radius: 25px;
            background-color: white;
            color: black; /* Text color inside the input box */
        }

        .chat-input-container .stTextInput>div>input::placeholder {
            color: black; /* Placeholder text color */
        }

        /* Custom style to make the label black */
        .chat-input-container label {
            color: black; /* Label text color */
        }

        .chat-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='header-container'>
        <img src='https://cdn.pixabay.com/photo/2021/05/22/10/21/dinosaur-6273164_1280.png' class='header-logo'/>
        <h1 class='times-new-roman-heading'>DinoAI</h1>
    </div>
""", unsafe_allow_html=True)



# Embed Chrome Dino game at the top
st.markdown("""
    <style>
        .iframe-container {
            position: relative;
            width: 100%;
            height: 200px; /* Adjust the height as needed */
            overflow: hidden;
            background: #000; /* Optional: set a background color for the container */
        }

        .iframe-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            box-sizing: border-box;
        }
    </style>

    <div class="iframe-container">
        <iframe src="https://wayou.github.io/t-rex-runner/"></iframe>
    </div>
""", unsafe_allow_html=True)

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

# Center-aligned text input box
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
st.markdown("<p style='color: black;'>👽Ask me anything...</p>", unsafe_allow_html=True)
st.text_input("👇👇👇",key="input", on_change=handle_input, placeholder="Type your question here...", help=" Type your question here ")

st.markdown("</div>", unsafe_allow_html=True)

# Buttons below the input box
st.markdown("<div class='chat-buttons'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 6])
with col1:
    st.button("Ask the question", on_click=handle_input)
with col2:
    st.button("Clear Chat", on_click=clear_history)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar for additional functionalities
# Sidebar for additional functionalities
with st.sidebar:
    st.header("Google Search")
    search_query = st.text_input("Enter your query:")
    if st.button("Search"):
        if search_query:
            encoded_query = urllib.parse.quote(search_query)
            google_search_url = f"https://www.google.com/search?q={encoded_query}"
            st.markdown(f"[Open Google Search]({google_search_url})", unsafe_allow_html=True)
        else:
            st.warning("Please enter a query to search.")

    st.markdown("---")

    st.header("Age Calculator🥸")

    date1 = st.date_input("Select first date")
    date2 = st.date_input("Select second date")

    if st.button("Calculate Difference"):
        if date1 and date2:
            diff = abs((date2 - date1).days)
            years = diff // 365
            remaining_days = diff % 365
            months = remaining_days // 30
            days = remaining_days % 30
            st.write(f"Difference: {years} years, {months} months, {days} days")
            st.write(f"Difference: {(diff)//365} Years")
            st.write(f"Difference: {(diff)//30} months")            
            st.write(f"Difference: {diff} days")

    st.markdown("---")

   
# Header for Todo App
    # st.header("Todo App")

    # # Input to add a new task
    # todo_item = st.text_input("Add a new task:")

    # # Button to add a task
    # if st.button("Add Task"):
    #     if "tasks" not in st.session_state:
    #         st.session_state.tasks = []
    #     st.session_state.tasks.append({"task": todo_item, "completed": False})  # Store task with completed status

    # # Display tasks and manage them
    # if "tasks" in st.session_state:
    #     st.subheader("Tasks:")

    #     for index, task in enumerate(st.session_state.tasks):
    #         task_key = f"task-{index}"
    #         # Checkbox to mark task as completed
    #         task["completed"] = st.checkbox(task["task"], task["completed"], key=task_key)

    #     # Button to delete completed tasks
    #     if st.button("Delete Completed Tasks"):
    #         st.session_state.tasks = [task for task in st.session_state.tasks if not task["completed"]]

    # # Separator
    # st.markdown("---")

    # st.header("Other AI Tools")

    # # Button for Chat GPT
    # if st.button("Chat GPT", key="chat_gpt_btn"):
    #     st.markdown("[Chat GPT](https://openai.com/chatgpt/)")

    # # Button for Claude AI
    # if st.button("Claude AI", key="claude_ai_btn"):
    #     st.markdown("[Claude AI](https://claude.ai/new)")



# Header for the calculator
    st.header("Normal Calculator")

    # Function to perform basic arithmetic operations
    def calculator(num1, num2, operation):
        if operation == "Addition":
            return num1 + num2
        elif operation == "Subtraction":
            return num1 - num2
        elif operation == "Multiplication":
            return num1 * num2
        elif operation == "Division":
            if num2 != 0:
                return num1 / num2
            else:
                return "Error: Division by zero"

    # Input fields for numbers and operation choice
    num1 = st.number_input("Enter first number:")
    num2 = st.number_input("Enter second number:")
    operation = st.selectbox("Select operation:", ["Addition", "Subtraction", "Multiplication", "Division"])

    # Calculate button
    if st.button("Calculate"):
        result = calculator(num1, num2, operation)
        st.write(f"Result of {operation}: {result}")

# Header for the unit conversion calculator
  

# Header for the unit conversion calculator
    st.header("Unit Conversion Calculator")

    # Function to convert units
    def convert_units(value, from_unit, to_unit):
        if from_unit == "Meter" and to_unit == "Kilometer":
            return value / 1000
        elif from_unit == "Meter" and to_unit == "Centimeter":
            return value * 100
        elif from_unit == "Meter" and to_unit == "Feet":
            return value * 3.281
        elif from_unit == "Meter" and to_unit == "Inch":
            return value * 39.37
        elif from_unit == "Meter" and to_unit == "Millimeter":
            return value * 1000
        elif from_unit == "Kilometer" and to_unit == "Meter":
            return value * 1000
        elif from_unit == "Centimeter" and to_unit == "Meter":
            return value / 100
        elif from_unit == "Feet" and to_unit == "Meter":
            return value / 3.281
        elif from_unit == "Inch" and to_unit == "Meter":
            return value / 39.37
        elif from_unit == "Millimeter" and to_unit == "Meter":
            return value / 1000
        else:
            return "Conversion not supported"

    # Input fields for unit conversion
    value = st.number_input("Enter value to convert:")
    from_unit = st.selectbox("From unit:", ["Meter", "Kilometer", "Centimeter", "Feet", "Inch", "Millimeter"])
    to_unit = st.selectbox("To unit:", ["Meter", "Kilometer", "Centimeter", "Feet", "Inch", "Millimeter"])

    # Convert button
    if st.button("Convert"):
        converted_value = convert_units(value, from_unit, to_unit)
        if isinstance(converted_value, str):
            st.write(f"Conversion not supported")
        else:
            st.write(f"{value} {from_unit} = {converted_value} {to_unit}")





    import webbrowser

    # Function to open URLs
    def open_url(url):
        webbrowser.open(url, new=2)  # new=2 opens the URL in a new tab

    # Sidebar section for AI Tools and buttons
    st.sidebar.header("Other AI Tools")

    # Button for Chat GPT
    if st.sidebar.button("Chat GPT"):
        open_url("https://openai.com/chatgpt/")

    # Button for Claude AI
    if st.sidebar.button("Claude AI"):
        open_url("https://claude.ai/new")
    


           

# Footer with Instagram link
st.markdown("<div class='footer'>Developed by SUN <a href='https://www.instagram.com/sun007_/' target='_blank'><img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' style='width: 20px; vertical-align: middle; margin-left: 5px;' /></a></div>", unsafe_allow_html=True)