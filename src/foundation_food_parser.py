import pandas as pd
import json


def extract_calories(food_nutrients: list) -> int:
    calories_rows = list(filter(lambda d: d["nutrient"]["id"] == 2047, food_nutrients))
    if len(calories_rows) > 0:
        return calories_rows[0]["amount"]
    return 0


def extract_carbs(food_nutrients: list) -> int:
    carbs_rows = list(filter(lambda d: d["nutrient"]["id"] == 1005, food_nutrients))
    if len(carbs_rows) > 0:
        return carbs_rows[0]["amount"]
    return 0


def extract_fat(food_nutrients: list) -> int:
    fat_rows = list(filter(lambda d: d["nutrient"]["id"] == 1004, food_nutrients))
    if len(fat_rows) > 0:
        return fat_rows[0]["amount"]
    return 0


def extract_protein(food_nutrients: list) -> int:
    protein_rows = list(filter(lambda d: d["nutrient"]["id"] == 1003, food_nutrients))
    if len(protein_rows) > 0:
        return protein_rows[0]["amount"]
    return 0


def parse_foundation_ingredients_nutrition_df():
    # load data using Python JSON module
    with open("data/foundationDownload.json", "r") as f:
        data = json.loads(f.read())
        # Flatten data
        df = pd.json_normalize(data, record_path=["FoundationFoods"])
        df = df[
            [
                "description",
                "fdcId",
                "foodCategory.description",
                "foodNutrients",
            ]
        ]
        df["calories"] = df["foodNutrients"].apply(extract_calories)
        df["carbs"] = df["foodNutrients"].apply(extract_carbs)
        df["fat"] = df["foodNutrients"].apply(extract_fat)
        df["protein"] = df["foodNutrients"].apply(extract_protein)
        # Convert fdcId to string so it can be used as an id in the vector store
        df["fdcId"] = df["fdcId"].astype(str)
        df = df.drop("foodNutrients", axis=1)
        return df
