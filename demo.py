# A bare bones UI for the Open AI Chat Completion used in ChatGPT
# Created by Adam Tomkins

import openai
import streamlit as st
import yaml
import json
import datetime
import requests

# Set up Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "primer" not in st.session_state:
    st.session_state["primer"] = "You are a friendly and helpful assistant."
if "context_length" not in st.session_state:
    st.session_state["context_length"] = 10

def main():
    # Initialization your state messages

    st.sidebar.header("Settings")

    with st.sidebar:
        # Allow the user to set their prompt
        st.session_state.primer = st.text_area(
            "System Prompt",
            "You are a friendly and helpful assistant.",
        )
        # st.session_state.context_length = st.slider(
        #     "Context Message Length", min_value=1, max_value=50, value=10, step=1
        # )

        # Allow Users to reset the memory
        save_col, clear_col = st.columns(2)
        with save_col:
            if st.button("Save Chat"):
                with open("history/chat-{}.json".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), "w") as f:
                    json.dump(st.session_state.messages, f)
        with clear_col:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.info("Chat Memory Cleared")
        
    # A place to draw the chat history
    history = st.container()

    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            # Create an on the fly message stack
            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages
            )

            # Call the OpenAI API
            if openai.api_type == "openai":
                r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            elif openai.api_type == "azure":
                # Use curl instead of the python SDK
                url = f'{openai.api_base}/openai/deployments/{st.session_state.engine}/chat/completions?api-version=2023-03-15-preview'
                payload = {
                    "model": st.session_state.engine,
                    "messages": messages,
                }

                headers = {
                    "Content-Type": "application/json",
                    "api-key": f"{openai.api_key}"
                }
                r = requests.post(url, json=payload, headers=headers).json()
                # r = openai.ChatCompletion.create(engine=st.session_state.engine, messages=messages)
            else:
                raise ValueError("Invalid API Type")
            tokens = r["usage"]["total_tokens"]
            # cost = round((tokens / 1000) * 0.02, 3)
            st.info(f"Message uses {tokens} tokens.")

            # with st.expander("Result"):
            #     st.info("Your Output Response")
            #     st.write(r)

            st.session_state.messages.append(
                {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
            )

    with history:
        for i, message in enumerate(st.session_state.messages):
            c1, c2 = st.columns([2, 10])
            with c1:
                st.write(message["role"])
            with c2:
                # Lets italisize the messages that are sent in the state
                if (
                    len(st.session_state.messages) - i
                    < st.session_state.context_length + 1
                ):
                    st.markdown(f'_{message["content"]}_')
                else:
                    st.markdown(f'{message["content"]}')

def save_settings():
    with open("config.yml", "w") as f:
        yaml.dump({
            "api_type": st.session_state.api_type,
            "api_key": st.session_state.api_key,
            "api_base": st.session_state.api_base,
            "api_version": st.session_state.api_version,
            "engine": st.session_state.engine,
            "model": st.session_state.model
        }, f)
        
def load_settings():
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
        st.session_state.api_type = config["api_type"]
        st.session_state.api_key = config["api_key"]
        st.session_state.api_base = config["api_base"]
        st.session_state.api_version = config["api_version"]
        st.session_state.engine = config["engine"]
        st.session_state.model = config["model"]
         
with st.sidebar:
    # if "api_type" not in st.session_state:
    #     st.session_state.api_type = "Azure"
    load_settings()
    # display settings
    with st.expander("Settings"):
        st.selectbox("API Type", ["openai", "azure"], key="api_type", index=0, on_change=save_settings)
        
        if st.session_state.api_type == "azure":
            st.selectbox("engine", ["chatgpt", "chatgpt-4"], key="engine", index=0, on_change=save_settings)
            st.session_state.api_key = st.text_input("API Key", st.session_state.api_key)
            st.session_state.api_base = st.text_input("API Base", st.session_state.api_base)
            st.session_state.api_version = st.text_input("API Version", st.session_state.api_version)
        elif st.session_state.api_type == "openai":
            st.session_state.api_key = st.text_input("API Key", st.session_state.api_key)
            st.selectbox("model", ["gpt-4", "gpt-3.5-turbo"], key="model", index=0, on_change=save_settings)
            # key = st.text_input("Your {} Key".format(st.session_state.api_type))
    
st.title("{} GPT".format(st.session_state.api_type.capitalize()))
# ("API Type", ["OpenAI", "Azure"], value="OpenAI")

if "api_key" not in st.session_state:
    st.info("Please check `config.yml`.")
else:
    openai.api_type = st.session_state.api_type
    openai.api_key = st.session_state.api_key
    openai.api_base = st.session_state.api_base
    openai.api_version = st.session_state.api_version
    save_settings()
    main()

# create footer
st.sidebar.header("About")
st.sidebar.info(
    """
    Created by Adam Tomkins. Source Code: https://github.com/AdamRTomkins/StreamlitChatGPT
    """
)
