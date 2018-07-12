import os
import json

from flask import current_app


class Webpack(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Mutate the application passed in as explained here:
        http://flask.pocoo.org/docs/0.10/extensiondev/

        :param app: Flask application
        :return: None
        """

        # Setup a few sane defaults.
        app.config.setdefault('WEBPACK_MANIFEST_PATH',
                              '/tmp/themostridiculousimpossiblepathtonotexist')

        self._set_asset_paths(app)

        # We only want to refresh the webpack stats in development mode,
        # not everyone sets this setting, so let's assume it's production.
        print('XXX APP INITED')
        if app.config.get('DEBUG', False):
            print('XXXX ATTEMPTING TO REFRESH STATS')
            app.before_request(self._refresh_webpack_stats)

        if hasattr(app, 'add_template_global'):
            app.add_template_global(self.javascript_tag)
            app.add_template_global(self.stylesheet_tag)
            app.add_template_global(self.asset_url_for)
        else:
            # Flask < 0.10
            ctx = {
                'javascript_tag': self.javascript_tag,
                'stylesheet_tag': self.stylesheet_tag,
                'asset_url_for': self.asset_url_for
            }
            app.context_processor(lambda: ctx)

    def _set_asset_paths(self, app):
        """
        Read in the manifest json file which acts as a manifest for assets.
        This allows us to get the asset path as well as hashed names.

        :param app: Flask application
        :return: None
        """
        webpack_stats = app.config['WEBPACK_MANIFEST_PATH']
        print('XXX IN _SET_ASSET_PATHS')

        try:
            with app.open_resource(webpack_stats, 'r') as stats_json:
                self.assets = json.load(stats_json)
                self.assets_url = app.config['WEBPACK_ASSETS_URL']
                print('XXX NEW ASSETS: {}'.format(self.assets))
        except IOError:
            raise RuntimeError(
                "Flask-Webpack requires 'WEBPACK_MANIFEST_PATH' to be set and "
                "it must point to a valid json file.")
        except KeyError:
            raise RuntimeError(
                "Flask-Webpack requires 'WEBPACK_ASSETS_URL' to be set")
        except Exception as e:
            raise e

    def _refresh_webpack_stats(self):
        """
        Refresh the webpack stats so we get the latest version. It's a good
        idea to only use this in development mode.

        :return: None
        """
        print('XXX TRYING TO SET ASSET_PATHS')
        self._set_asset_paths(current_app)

    def javascript_tag(self, *args):
        """
        Convenience tag to output 1 or more javascript tags.

        :param args: 1 or more javascript file names
        :return: Script tag(s) containing the asset
        """
        tags = []

        for arg in args:
            asset_path = self.asset_url_for('{0}.js'.format(arg))
            if asset_path:
                tags.append('<script src="{0}"></script>'.format(asset_path))

        return '\n'.join(tags)

    def stylesheet_tag(self, *args):
        """
        Convenience tag to output 1 or more stylesheet tags.

        :param args: 1 or more stylesheet file names
        :return: Link tag(s) containing the asset
        """
        tags = []

        for arg in args:
            asset_path = self.asset_url_for('{0}.css'.format(arg))
            if asset_path:
                tags.append(
                    '<link rel="stylesheet" href="{0}">'.format(asset_path))

        return '\n'.join(tags)

    def asset_url_for(self, asset):
        """
        Lookup the hashed asset path of a file name unless it starts with
        something that resembles a web address, then take it as is.

        :param asset: A logical path to an asset
        :type asset: str
        :return: Asset path or None if not found
        """
        if '//' in asset:
            return asset

        if asset not in self.assets:
            return None

        if not self.assets_url:
            raise RuntimeError(
                "Flask-Webpack requires 'WEBPACK_ASSETS_URL' to be set")

        return os.path.join(self.assets_url, self.assets[asset])
