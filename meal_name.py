import openai
import streamlit as st
import logging

openai.api_key = st.secrets.openai_key

messages = [
    {
        "role": "system",
        "content": "Imagine the prompt as a short description or name of a meal or snack that a person might have eaten. Your goal is to convert the prompt into a set of items of food or name of a recipe that best represents what was typed in by the user.",
    },
    {"role": "user", "content": "A sandwich with steak and cheese"},
    {"role": "assistant", "content": "Cheesesteak, Cubano, Chopped Cheese"},
    {
        "role": "user",
        "content": "An indian dish with chicken marinated in a tomato gravy.",
    },
    {
        "role": "assistant",
        "content": "Chicken Tikka Masala, Butter Chicken, Jamaican Beef Stew",
    },
    {"role": "user", "content": "Rice, chicken, and beans"},
    {
        "role": "assistant",
        "content": "Burrito Casserole, Coconut Rice and Beans, Creamy Chicken Enchilada Soup",
    },
    {"role": "user", "content": "Red meat in wine sauce"},
    {
        "role": "assistant",
        "content": "Beef Bourguignon, Coq au Vin, Beef Stroganoff",
    },
    {"role": "user", "content": "An apple"},
    {
        "role": "assistant",
        "content": "Whole apple, apple slices, baked apple",
    },
]


def generate_meal_names(a_meal_name: str) -> str:
    messages.append({"role": "user", "content": a_meal_name})
    logging.info('Fetching completion from for "{}"'.format(a_meal_name))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content


generate_meal_names("Triple Chocolate Cake")
