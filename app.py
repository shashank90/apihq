import threading
import time
import atexit
from flask import Flask

from backend.db.database import get_session, init_db
from backend.log.factory import Logger, init_logger
from backend.apis.auth.routes import auth_bp
from backend.apis.discovery.routes import discovery_bp
from backend.apis.validate.routes import validate_bp
from backend.apis.run.routes import run_bp
from backend.tester.connectors.zap.factory import ZAP
from backend.tester.connectors.zap.zap_handler import shutdown_zap, start_zap
from backend.utils.constants import WORK_DIR
from backend.utils.file_handler import remove_files
from backend.utils.file_cache_handler import init_cache
from backend.utils.init_folders import create_folders

logger = Logger(__name__)

app = Flask(__name__)


def setup_app():
    """
    Setup app, including db and api routes
    """

    app.config.from_object("config.ProdConfig")
    DATABASE_URI = app.config["DATABASE_URI"]
    with app.app_context():
        # Initialize database
        init_db(DATABASE_URI)

        # Register Blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(discovery_bp)
        app.register_blueprint(validate_bp)
        app.register_blueprint(run_bp)

    return app


def init_app():
    # Create folders
    create_folders()

    # Initialise logger
    init_logger()

    # Initialize file cache
    init_cache()

    # Initialize app
    setup_app()

    # Initialize zap
    start_zap()
    # start_flask_app()


init_app()


def shutdown_app():
    """
    Shutdown app
    """
    logger.info("Shutting down app...")

    logger.info("Terminating zap...")

    # Shutdown zap
    shutdown_zap()

    # Get threads from threadpool. Uncomment when threadpool handler ready
    # for thread in threads:
    #     thread.join()
    # print("Threads complete, ready to finish")


atexit.register(shutdown_app)


def start_flask_app():
    """
    Use this if using flask server directly. Or launch via gunicorn
    """
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
        app.register_blueprint(validate_bp)
        app.register_blueprint(run_bp)

    try:
        while True:
            # Keeping the main thread alive! So that when interrupt hits, child threads also exit gracefully
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Exiting App...")
        exit(0)
