import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from src.meal_name_expander import generate_meal_names
from src.common_ingredient_finder import (
    generate_prominent_ingredients,
    parse_json_string,
)
from src.foundation_food_vector_store import query_vector_store_index
from llama_index.query_engine.pandas_query_engine import PandasQueryEngine

# openai.log = "debug"

st.set_page_config(
    page_title="Look up foods based on nutritional needs",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
openai.api_key = st.secrets.openai_key
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info(
    "Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)",
    icon="📃",
)
prompt = st.chat_input("Say something")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Provide a short description of the meal you just ate and I'll find the nutrition information for you.",
        }
    ]


# @st.cache_resource(show_spinner=False)
# def load_data():
#     with st.spinner(
#         text="Loading and indexing the food nutrients data. This should take less than a minute minutes."
#     ):


# index = load_data()

if prompt := st.chat_input(
    "Description of a meal or snack"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for first_message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(first_message["role"]):
        st.write(first_message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            similar_meal_names_response = generate_meal_names(prompt)
            print(f"similar_meal_names_response={similar_meal_names_response}")
            st.write("Okay i've found some dishes that seem similar:")
            similar_meal_names_md = ""
            for i in parse_json_string(similar_meal_names_response):
                similar_meal_names_md += "- " + i + "\n"
            st.markdown(similar_meal_names_md)
            prominent_ingredients = generate_prominent_ingredients(
                similar_meal_names_response
            )
            st.write("Okay here are some ingredients that seeem likely:")
            prominent_ingredients_md = ""
            prominent_ingredients_list = parse_json_string(prominent_ingredients)
            for i in prominent_ingredients_list:
                prominent_ingredients_md += "- " + i + "\n"
            st.markdown(prominent_ingredients_md)
            st.write("Finding nutrition info for these ingredients...")
            for an_ingredient in prominent_ingredients_list:
                query_vector_store_index(an_ingredient)
            # st.session_state.messages.append(first_message)  # Add response to message history