from app_.controllers.home_controller import home_blueprint
from app_.controllers.api_controller import api_blueprint

def register_routes(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(api_blueprint)
    
    