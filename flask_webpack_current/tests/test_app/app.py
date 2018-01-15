from flask import Flask, render_template
from werkzeug.serving import run_simple

from flask_webpack_current import Webpack
webpack = Webpack()


def create_app(settings_override=None):
    """
    Create a test application.

    :param settings_override: Override settings
    :type settings_override: dict
    :return: Flask app
    """
    app = Flask(__name__)

    params = {
        'DEBUG': True,
        'WEBPACK_MANIFEST_PATH': 'build/public/manifest.json',
        'WEBPACK_ASSETS_URL': 'https://yourdomainname_or_asset_cdn.com/assets/'
    }

    app.config.update(params)

    if settings_override:
        app.config.update(settings_override)

    webpack.init_app(app)

    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)
