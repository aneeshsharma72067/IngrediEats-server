from flask import Flask, request
from flask_cors import CORS
import dataset

app = Flask(__name__)
CORS(app)

@app.route('/api/recipes')
def home():
    return {
        'message':dataset.getRecipeNames()
    }

if __name__ == '__main__':
    app.run(debug=True)