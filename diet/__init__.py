import os 
 
from flask import Flask

def create_app(test_config = None):
    """ App creator for Flask """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='lul',
        DATABASE = os.path.join(app.instance_path, 'diet.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return 'hello'
    
    from . import db

    # Kinda like in embedded c programming
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.blueprint)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint = 'index')
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run('0.0.0.0')