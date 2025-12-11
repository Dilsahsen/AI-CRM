from flask import Flask
from config import Config
from extensions import db, login_manager, mail
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.customers import customers_bp
from routes.sales import sales_bp
from flask import redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(sales_bp, url_prefix="/sales")

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))


    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)












