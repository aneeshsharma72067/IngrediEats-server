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


if __name__ == '__main__':
    app.run(debug=True)