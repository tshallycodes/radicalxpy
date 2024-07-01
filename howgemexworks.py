import vertexai # for building machine learning models by Google cloud
import streamlit as st # STreamlit is a framework for web app models and is name st
from vertexai.preview import generative_models #generative_models is a class for manipulating Gemini models.
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession 
#GenerativeModel is for setting model and also setting configurations of the model / Part is a section of the content of a candidate or possible response / Content is the content inside the candidate / ChatSession is for sening and receiving input and output from the generative model.

myproject = "sample-gemini"
vertexai.init(project = myproject)

# How to set the response randomness of the generative model
config = generative_models.GenerationConfig(
    temperature=0.4
)

#Load model and also set with config
model = GenerativeModel(
    "gemini-pro", #selecting a model
    generation_config = config #the configuration of the model
)
# Start a chat session so messages caane sent and received
chat = model.start_chat()

# Helper function to send and display any streamlit messages
def llm_function(chat: ChatSession, query): #chat: ChatSession to turn chat variable to a ChatSession class, query for user input
    response = chat.send_message(query) #Sends user input(query) to the generative model using the send_message method
    output = response.candidates[0].content.parts[0].text #candidates are possible responses and [0] means pick the first possible response / text is for bringing the text in the part.

    with st.chat_message("model"): #with is used to open, retrieve and set "model" as the source of content to be displayed
        st.markdown(output) #markdown is content formarting

    st.session_state.messages.append( #session_state is the current chat session / messages is the sent and received inout and output / append is to add to the session or save data of the session
        {
            "role": "user", # role is to specific whether it is the user or the generative model that created a message 
            "content": query # content is the message written by the role.
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

st.title("Gemini Explorer") # To name the application

#Initialising chat history
if "messages" not in st.session_state: #Checks if any messages or message attributes in the session.
    st.session_state.messages = [] # This line is to set the value as empty( which it always is at the start of a session)make the message attribute an appendable attribute 

#Display and load to chat history
for index, message in enumerate(st.session_state.messages): #index is the numbering / enumarate(is used to add a counter)
    content = Content(  #content contains Content(for storing an displaying values), here it displays role and a part of the text form of the content of the role (either query or output)
        role = message["role"], 
        parts = [Part.from_text(message["content"])]
    )
    if index != 0:
       with st.chat_message(message["role"]): #This will load every message present in the session 
                st.markdown(message["content"]) #and streamlit will markdown the content of the role
if len(st.session_state.messages) == 0: #This displays "No messages to display" when the with statement does not find any messages(role and content) in the session.
    st.write("No messages to display")

#For capture user input
query = st.chat_input("Gemini Explorer") # This is use to collect user inpout using the streamlit method "chat_input"

if query:  
    with st.chat_message("user"): #This turns the user input(query) into a chat message with role (user) and performs markdown
        st.markdown(query)
    llm_function(chat, query) # This is to processs the user's input and make the model generate a response.