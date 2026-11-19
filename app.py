import streamlit as st
from agent import agent

st.title("Agentic AI Assistant")

st.write("Search and Weather AI Agent")

user_input = st.text_input(
    "What would you like to know?",
    placeholder="e.g. Find the capital of Ghana and tell me its weather",
)

if st.button("Ask") and user_input:
    with st.spinner("Checking..."):
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    st.write(response["messages"][-1].text)
