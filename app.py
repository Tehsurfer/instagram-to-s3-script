from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from airtable_csv import AirtableCSVManager

app = Flask(__name__)
CORS(app)

load_dotenv('.env.local')

# Ensure required environment variables are set
if not os.getenv('BASE_ID') or not os.getenv('TABLE_NAME') or not os.getenv('API_KEY'):
    load_dotenv('.env')
if not os.getenv('BASE_ID') or not os.getenv('TABLE_NAME') or not os.getenv('API_KEY'):
    raise ValueError("Missing required environment variables: BASE_ID, TABLE_NAME, API_KEY")

ENVIRONMENT_MODE = os.getenv('ENVIRONMENT', 'Production')

exporter = AirtableCSVManager(
    base_id=os.getenv('BASE_ID'),
    table_name=os.getenv('TABLE_NAME'),
    api_key=os.getenv('API_KEY')
)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == '__main__':
    exporter.update_csv_from_airtable()
    
    app.run(debug=True)