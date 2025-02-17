import os
import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variables
openai_api_key = os.getenv("TOGETHER_API_KEY")  # Use the Together API key



# If API key is not found, stop execution
if not openai_api_key:
    st.error("API key not found. Please set it in the environment variables or .env file.")
    st.stop()

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys():  # Initialize chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize ChatOpenAI and ConversationChain
llm = ChatOpenAI(model="meta-llama/Llama-3-70B",  # Ensure this model is supported by Together API
                  openai_api_key=openai_api_key)

TOGETHER_API_KEY = "a23ae25589f1a136f1cb934dad3be1145b31b874a603b6011dcb1642633a2f95"
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Simple Chat Interface for LLMs by Build Fast with AI")

# User input and appending to the chat history
if prompt := st.chat_input("Your question"):  
    st.session_state.messages.append({"role": "user","content": prompt})

# Display the prior chat messages
for message in st.session_state.messages:  
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate response if last message is from user
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Generate response using LLM
            response = conversation.predict(input=prompt)
            st.write(response)
            
            # Append assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
