from flask import Flask
from pathlib import Path


def create_app() -> Flask:
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'dev-secret-key'
	app.config['UPLOAD_FOLDER'] = str(Path('data/uploads').resolve())
	app.config['PROCESSED_FOLDER'] = str(Path('data/processed').resolve())
	app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

	from .routes import bp as main_bp
	app.register_blueprint(main_bp)

	Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
	Path(app.config['PROCESSED_FOLDER']).mkdir(parents=True, exist_ok=True)

	return app


