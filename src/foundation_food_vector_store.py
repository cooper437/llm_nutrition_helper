import chromadb
import logging
from src.foundation_food_parser import parse_foundation_ingredients_nutrition_df


class FoundationFoodsVectorStore:
    """A vector store for semantically searching foundation foods that may be used as ingredients in a meal"""

    def __init__(self):
        self.chroma_client = None
        self.collection = None

    def initialize_vector_db(self):
        print("Initializing vector db")
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(name="foundation_foods")

    def build_vector_store_index(self):
        """Builds a vector store index for the foundation foods data"""
        logging.info("Parsing foundation foods data into a dataframe")
        foundation_foods_df = parse_foundation_ingredients_nutrition_df()
        logging.info("Building vector store index")
        self.collection.add(
            documents=list(foundation_foods_df["description"]),
            metadatas=foundation_foods_df.to_dict(orient="records"),
            ids=list(foundation_foods_df["fdcId"]),
        )

    def query_vector_store_index(self, an_ingredient: str, n_results: int = 1):
        """Queries the vector store index for the most similar foundation food ingredient.
        Returns the most similar foundation food ingredient as a dictionary"""
        print(f"Querying vector store index for {an_ingredient}")
        results = self.collection.query(
            query_texts=[an_ingredient], n_results=n_results
        )
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
