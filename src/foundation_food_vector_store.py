import chromadb
import logging
from src.foundation_food_parser import parse_foundation_ingredients_nutrition_df

chroma_client = None
collection = None
if not chroma_client:
    chroma_client = chromadb.Client()

if not collection:
    collection = chroma_client.create_collection(name="foundation_foods")


def build_vector_store_index():
    logging.info("Parsing foundation foods data into a dataframe")
    foundation_foods_df = parse_foundation_ingredients_nutrition_df()
    logging.info("Building vector store index")
    collection.add(
        documents=list(foundation_foods_df["description"]),
        metadatas=foundation_foods_df.to_dict(orient="records"),
        ids=list(foundation_foods_df["fdcId"]),
    )


def query_vector_store_index(an_ingredient: str, n_results: int = 1):
    print(f"Querying vector store index for {an_ingredient}")
    results = collection.query(query_texts=[an_ingredient], n_results=n_results)
    print(f"Most similar result: {results}")
    description = results["documents"][0][0]
    calories = results["metadatas"][0][0]["calories"]
    carbs = results["metadatas"][0][0]["carbs"]
    fat = results["metadatas"][0][0]["fat"]
    protein = results["metadatas"][0][0]["protein"]
    return {
        "Description": description,
        "Calories (kcal)": calories,
        "Carbs (g)": carbs,
        "Fat (g)": fat,
        "Protein (g)": protein,
    }


build_vector_store_index()
