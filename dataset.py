import pandas as pd
import numpy as np
import re

df = pd.read_csv('recipe_dataset.csv')
recipe_names = list(df['Title'])
recipe_image_names = list(df['Image_Name'])
recipe_id = list(df['Index'])
ingredients = list(df['Ingredients'])

def getRecipeNames():
    return [{'id':recipe_id[i], 'recipe_name':recipe_names[i],'image_name':recipe_image_names[i], 'ingredients':eval(ingredients[i])} for i in range(0,50)]