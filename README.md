# Meal Nutrition Helper

## Description
A [streamlit](https://docs.streamlit.io/) chatbot that allows you to enter a meal name or short description and then returns the basic nutritional information for that meal such as calories, fat, carbs, and protein.

## How It Works
There are four stages to the chatbot:
1. On startup we parse a small list of foundation foods from the https://fdc.nal.usda.gov/download-datasets.html website. We extract the food name, calories, fat, carbs, and protein from the dataset for each entry.
2. We generate embeddings for each description of a foundation food. These are stored in [chroma-db](https://docs.trychroma.com/) which is a small in-memory embedding database for quick retrieval.
3. When a user enters a meal description we use an LLM few-shot prompt to expand the description into a list of possible prepared foods and dishes. Transformer based query expansion is a powerful technique for AI based information retrieval.
4. We then take the expanded search terms and chain them into a new prompt template - also using a few-shot learning method - that tries to reason about the common and most prominent ingredients across the set of meals.
5. We do a K-nearest-neighors vector embedding search against chroma-db to find the closest matching foundation foods by the semantic similarity of their descriptions to the ingredients and return the nutritional information for the top k results.
6. Lastly we aggregate the nutritional information across the top 5 results and return the total calories, fat, carbs, and protein for the meal.

## Environment Setup
