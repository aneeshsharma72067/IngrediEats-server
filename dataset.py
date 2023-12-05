import pandas as pd
import numpy as np
import re

# Read data from a CSV file into a DataFrame
df = pd.read_csv('parsed_recipe_dataset.csv')

# Extract relevant columns from the DataFrame
recipe_names = list(df['Title'])
recipe_image_names = list(df['Image_Name'])
recipe_id = list(df['Index'])
ingredients = list(df['New_Ingredients'])

def getRecipes():
    """
    Get a list of recipes with cleaned ingredients.

    Returns:
    list: A list of dictionaries, each containing recipe information.
    """
    recipe_list = []
    print(f' recipe ID length : {len(recipe_id)}')
    for i in range(0, 1000):
        ingredient_list = [ing.capitalize() for ing in eval(ingredients[i])]
        recipe_list.append({
            'id': recipe_id[i],
            'recipe_name': recipe_names[i],
            'image_name': recipe_image_names[i],
            'ingredients': ingredient_list
        })
    print(f' recipe length : {len(recipe_list)}')
    return recipe_list

def getAllIngredients():
    """
    Get a list of cleaned ingredients.

    Returns:
    list: A list of cleaned and unique ingredients.
    """
    def clean_ingredient(ingredient):
        """
        Clean an ingredient by removing specified words.

        Args:
        ingredient (str): The ingredient to be cleaned.

        Returns:
        str: The cleaned ingredient.
        """
        words_and_symbols_to_remove = ['new', 'old', 'fresh', 'freshly', 'sliced', 'diced', '/', '"', '\\', ',', ':', ';', 'or', 'and']
        pattern = '|'.join(r'\b{}\b'.format(re.escape(word)) for word in words_and_symbols_to_remove)
        cleaned_ingredient = re.sub(pattern, '', ingredient, flags=re.IGNORECASE)
        return cleaned_ingredient.strip().capitalize()

    ingredient_list = []
    for i in ingredients[0:1000]:
        ing_list = eval(i)
        for ing in ing_list:
            cleaned_ing = clean_ingredient(ing)
            cleaned_ing = cleaned_ing.replace('"','').replace('/','').replace(',',' ').replace('-','').replace(' A ','').capitalize()
            if cleaned_ing != "":
                ingredient_list.append(cleaned_ing) 
    return sorted(list(set(ingredient_list)))
