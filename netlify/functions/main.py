import serverless_wsgi
import sys
import os

# Add the parent directory (project root) to the Python path
# This allows Netlify functions to import 'app' from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import app # Import your Flask app instance

def handler(event, context):
    """
    This function is the entry point for Netlify Functions.
    It uses serverless-wsgi to adapt the Flask app for a serverless environment.
    """
    return serverless_wsgi.handle_request(app, event, context)