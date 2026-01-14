import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import logging
# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "wellness-app-secret-key-2024")

# Vercel uses proxies, so we need ProxyFix to handle HTTPS correctly
# This ensures url_for generates https:// links and cookies are handled properly
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Configure session
# Standard Flask sessions use signed cookies.
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True for HTTPS (Vercel)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Import and register routes after app is configured
from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
