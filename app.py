from app_ import create_app
from app_.config.config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)