from flask import Flask
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.finance_routes import finance_bp
from routes.commute_routes import commute_bp
from routes.calendar_routes import calendar_bp
from routes.tasks_routes import tasks_bp 
from auth.auth import requires_auth
import logging


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s"  # Include timestamps and log levels
)


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(finance_bp, url_prefix='/finance')
    app.register_blueprint(commute_bp, url_prefix='/commute')
    app.register_blueprint(calendar_bp)
    app.register_blueprint(tasks_bp) 


    return app

if __name__ == "__main__":
    logging.debug("🔄 Initializing Flask app...")
    app = create_app()
    logging.debug("🔄 Configuring CORS...")
    app.app_context().push()
    logging.debug("🚀 Starting Flask app...")
    app.run(host="10.250.102.152", port=5000, debug=True)
