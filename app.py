import os
import json
from flask import Flask, render_template, request, redirect, url_for
from script_telo import scrapear_telos

app = Flask(__name__)

@app.route("/scrapear")
def scrapear():
    scrapear_telos()
    
    return redirect(url_for('index'))

# Determine the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'hoteles.json')

def load_hotels():
    """Loads hotel data from the JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo de datos '{DATA_FILE}' no fue encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo de datos '{DATA_FILE}' no es un JSON válido.")
        return []

@app.route('/', methods=['GET'])
def index():
    all_hotels = load_hotels()
    filtered_hotels = all_hotels

    # Get filter criteria from query parameters
    nombre_query = request.args.get('nombre', '').lower()
    barrio_query = request.args.get('barrio', '').lower()
    precio_query = request.args.get('precio', '')
    

    # Apply filters
    if nombre_query:
        filtered_hotels = [
            hotel for hotel in filtered_hotels 
            if nombre_query in hotel.get('nombre', '').lower()
        ]

    if barrio_query:
        filtered_hotels = [
            hotel for hotel in filtered_hotels 
            if barrio_query in hotel.get('barrio', '').lower()
        ]

    if precio_query:
        try:
            precio_val = int(precio_query)
            filtered_hotels = [
                hotel for hotel in filtered_hotels 
                if hotel.get('precio_nivel') == precio_val
            ]
        except ValueError:
            pass # Ignore if price is not a valid number


    return render_template('index.html', hoteles=filtered_hotels)

if __name__ == '__main__':
    # This part is for local development, Netlify will use the handler
    app.run(debug=True)