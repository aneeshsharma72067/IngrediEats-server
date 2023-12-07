from flask import Flask, request
from flask_cors import CORS
import dataset

app = Flask(__name__)
CORS(app)

@app.route('/api/recipes')
def getAllRecipes():
    return {
        'message':dataset.getRecipes()
    }

@app.route('/api/ingredients')
def allIngredients():
    return {
        'ingredients':dataset.getAllIngredients()
    } 

@app.route('/api/similar-recipes')
def getSimilarRecipes():
    user_input = request.args.get('ingredients')
    if not user_input:
        return {'error': 'Empty user input'}
    user_input = user_input.split('-')
    return {
        'similar_recipes':dataset.similarRecipes(user_input)
    }

if __name__ == '__main__':
    app.run(debug=True)