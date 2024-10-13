from flask import Flask
from routes import routes

app = Flask(__name__)

# Register routes blueprint
app.register_blueprint(routes)


if __name__ == '__main__':
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
