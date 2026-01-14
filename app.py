import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "wellness-app-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure session
# Standard Flask sessions use signed cookies, which is ideal for serverless environments like Vercel.
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # For HTTPS on Vercel
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Import and register routes after app is configured
from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
