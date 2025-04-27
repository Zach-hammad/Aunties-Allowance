from flask import Flask
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.finance_routes import finance_bp
from routes.commute_routes import commute_bp
from routes.calendar_routes import calendar_bp
from routes.tasks_routes import tasks_bp 



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
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
