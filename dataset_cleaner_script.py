import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('cleaned_parsed_dataset.csv')
df['New_Ingredients'] = df['New_Ingredients'].apply(ast.literal_eval)

user_input = ['chicken', 'salt', 'water','garlic']

# Fit the TF-IDF vectorizer on the entire dataset
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
ingredients_matrix = tfidf_vectorizer.fit_transform(df['New_Ingredients'].apply(lambda x: ' '.join(x)))

# Use apply with a lambda function to check if at least one ingredient matches
matching_rows = df[df['New_Ingredients'].apply(lambda x: any(ingredient in user_input for ingredient in x))]

if matching_rows.empty:
    print('No matching recipes found')
else:
    matching_rows['New_ingredients_str'] = matching_rows['New_Ingredients'].apply(lambda x: ' '.join(x))
    
    # Transform the user input using the fitted vectorizer
    user_input_vector = tfidf_vectorizer.transform([' '.join(user_input)])
    
    matching_rows['similarity_score'] = cosine_similarity(user_input_vector, tfidf_vectorizer.transform(matching_rows['New_ingredients_str']))[0]
    top_matches = matching_rows.sort_values(by='similarity_score', ascending=False)
    result = top_matches.to_dict(orient='records')
    print(result[0:10])

