import chromadb
import logging
from src.foundation_food_parser import parse_foundation_ingredients_nutrition_df

chroma_client = chromadb.Client()

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
    results = collection.query(
        query_texts=["Mozzarella Cheese, Ground Beef, Flour"], n_results=2
    )
    print(results)


build_vector_store_index()
