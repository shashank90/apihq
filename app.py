import threading
import time

from flask import Flask
from db import tester

from db.database import init_db
from log.factory import Logger, init_logger
from apis.auth.routes import auth_bp
from apis.discovery.routes import discovery_bp
from apis.audit.routes import audit_bp
from apis.scan.routes import scan_bp
from utils.constants import WORK_DIR
from utils.file_handler import remove_files

logger = Logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    # app.secret_key = "secret key"
    logger.info("Starting Flask App server...")
    t = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    t.setDaemon(True)
    t.start()

    with app.app_context():
        # Initialize database
        init_db()

        # Register Blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(discovery_bp)
        app.register_blueprint(audit_bp)
        app.register_blueprint(scan_bp)

    try:
        while True:
            # Keeping the main thread alive! So that when interrupt hits, child threads also exit gracefully
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Exiting App...")
        exit(0)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     get_session().remove()


if __name__ == "__main__":
    # Initialise logger
    init_logger()
    # Initialize app
    create_app()

    # tester.test()
