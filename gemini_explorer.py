import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

myproject = "sample-gemini"
vertexai.init(project = myproject)


config = generative_models.GenerationConfig(
    temperature=0.4
)

#Load model and also set with config
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
# Start a chat session
chat = model.start_chat()

# Helper function to display any streamlit messages
def llm_function(chat, query, user_name):
    # Logic to generate response based on query and user's name
    query = st.chat_message("user").content
    personalized_query = f"Hello {user_name}! {query}"
    response = chat.send_message(personalized_query)
    output = f"Hello {user_name}, {response.candidates[0].content.parts[0].text}"
    
    # Display the model's response in the chat
    with st.chat_message("model"):
        st.markdown(output)
    
    # Append the user's query and the model's response to the chat history
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": output})

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display and load to chat history
for index, message in enumerate(st.session_state.messages): 
    content = Content( 
        role = message["role"], 
        parts = [Part.from_text(message["content"])] 
    ) 
    if index > 0: 
        with st.chat_message(message["role"]): 
            st.markdown(message["content"])

# Check if there are no messages in the chat history and send the initial prompt
if len(st.session_state.messages) == 0:
    user_name = st.text_input("What is your name?")
    initial_prompt = "I am ReX, an assistant powered by Google Gemini. You can use emojis to be interactive!!"
    llm_function(chat, initial_prompt, user_name)

# Capture user input
query = st.chat_input("Ask ReX a question")

# Process the user's query
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query, user_name)

# If query asks for name
if query == "What is your name?" or "What are you?":
    response = f"Hello {user_name}!" + initial_prompt
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query, user_name)
    
    