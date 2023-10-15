from typing import List
import openai
import streamlit as st
import logging
import json

openai.api_key = st.secrets.openai_key

messages = [
    {
        "role": "system",
        "content": "Imagine the prompt as a list of dishes that could be prepared. Your job is to guess the common and most prominent ingredients across the set of meals. Return the answer as a JSON array of strings sorted by prominence of the ingredient. ",
    },
    {
        "role": "user",
        "content": "Chicken Tikka Masala, Butter Chicken, Jamaican Beef Stew",
    },
    {"role": "assistant", "content": '["chicken", "beef", "masala", "butter"]'},
    {"role": "user", "content": "Cheesesteak, Cubano, Chopped Cheese"},
    {"role": "assistant", "content": '["cheese", "steak", "ham", "pork", "bread"]'},
    {"role": "user", "content": "Beef Bourguignon, Coq au Vin, Beef Stroganoff"},
    {"role": "assistant", "content": '["beef", "wine", "onion", "mushroom", "cream"]'},
]


def parse_json_string(json_str: str) -> List[str]:
    """Convert a JSON-formatted string to a Python list of strings"""
    try:
        # Parse the JSON-formatted string and convert it to a Python list
        parsed_list = json.loads(json_str)

        # Check if the parsed result is a list of strings
        if isinstance(parsed_list, list) and all(
            isinstance(item, str) for item in parsed_list
        ):
            return parsed_list
        else:
            raise ValueError("Input is not a valid list of strings in JSON format.")
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format: " + str(e))


def generate_prominent_ingredients(meal_names: str) -> str:
    # Given a list of meal names, return the common and prominent ingredients
    # that can be used to compose the meal
    messages.append({"role": "user", "content": meal_names})
    logging.info(
        'Fetching common and prominent ingredients for meal names "{}"'.format(
            meal_names
        )
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content
