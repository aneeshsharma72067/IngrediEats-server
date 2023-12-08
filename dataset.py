import pandas as pd
import numpy as np
import re
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Read data from a CSV file into a DataFrame
df = pd.read_csv('cleaned_parsed_dataset.csv')

# Extract relevant columns from the DataFrame
recipe_names = list(df['Title'])
recipe_image_names = list(df['Image_Name'])
recipe_id = list(df['Index'])
ingredients = list(df['New_Ingredients'])

tfidf_vectorizer = None
def initialize_tfidf_vectorizer():
    global tfidf_vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    return tfidf_vectorizer.fit_transform(df['New_Ingredients'].apply(lambda x:''.join(x)))

if tfidf_vectorizer is None:
    ingredients_matrix = initialize_tfidf_vectorizer()

def getRecipes():
  
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

    def clean_ingredient(ingredient):
     
        words_and_symbols_to_remove = ['new', 'old', 'fresh', 'freshly', 'sliced', 'diced', '/', '"', '\\', ',', ':', ';', 'or', 'and']
        pattern = '|'.join(r'\b{}\b'.format(re.escape(word)) for word in words_and_symbols_to_remove)
        cleaned_ingredient = re.sub(pattern, '', ingredient, flags=re.IGNORECASE)
        return cleaned_ingredient.strip().capitalize()

    ingredient_list = []
    for i in ingredients[0:100]:
        ing_list = eval(i)
        for ing in ing_list:
            cleaned_ing = clean_ingredient(ing)
            cleaned_ing = cleaned_ing.replace('"','').replace('/','').replace(',',' ').replace('-','').replace(' A ','').capitalize()
            if cleaned_ing != "":
                ingredient_list.append(cleaned_ing) 
    return sorted(list(set(ingredient_list)))


def similarRecipes(user_input):

    global tfidf_vectorizer
    global ingredients_matrix
    
    if tfidf_vectorizer is None:
        ingredients_matrix = initialize_tfidf_vectorizer()

    df['New_Ingredients'] = df['New_Ingredients'].apply(str).apply(ast.literal_eval)
    print(df['New_Ingredients'].iloc[1])
    matching_rows = df[df['New_Ingredients'].apply(lambda x: any(ingredient in user_input for ingredient in x))]

    if matching_rows.empty:
        return 'No recipe found'
    else:
        matching_rows['New_ingredients_str'] = matching_rows['New_Ingredients'].apply(lambda x: ' '.join(x))
        
        user_input_vector = tfidf_vectorizer.transform([' '.join(user_input)])
        
        matching_rows['similarity_score'] = cosine_similarity(user_input_vector, tfidf_vectorizer.transform(matching_rows['New_ingredients_str']))[0]
        top_matches = matching_rows.sort_values(by='similarity_score', ascending=False)
        top_matches['Cleaned_Ingredients'] = top_matches['Cleaned_Ingredients'].apply(eval)
        result = top_matches.to_dict(orient='records')[0:10]
        return result

