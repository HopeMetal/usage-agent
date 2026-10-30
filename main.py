import streamlit as st
import langchain.messages as lcm
from src.agent import send_message
from src.agent import messages as agent_messages

def message_type_to_name(message) -> str:
    if isinstance(message, lcm.HumanMessage):
        return "human"
    if isinstance(message, lcm.AIMessage):
        return "assistant"
    if isinstance(message, lcm.ToolMessage):
        return "tool"

st.title("Code Assistant Usage Agent")

with st.chat_message("assistant"):
    st.write("Hello. This is the AI Coding Assistant Usage Agent. What can I do for you?")

for message in agent_messages:
    print(message)
    with st.chat_message(message_type_to_name(message)):
        st.write(message.content)

get_claude_data_button = st.button("Get Claude Data", type="primary")

if get_claude_data_button:
    with st.chat_message("assistant"):
        st.write("I will get your Claude usage data from your local machine.")
    send_message("Get my Claude usage data.")
    st.rerun()

prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    send_message(prompt)
    st.rerun()