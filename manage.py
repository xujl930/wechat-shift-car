# -*- coding:utf8 -*-
import os
from app import create_app, db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    from app.models.model import User, QrCode
    return dict(app=app, db=db, User=User, QrCode=QrCode)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="127.0.0.1", port=8000, use_debugger=True))


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

@manager.command
def command():
    """ 定义自己的命令"""
    pass


if __name__ == '__main__':
    manager.run()
    # app.run(host='127.0.0.1', port=8000, debug=1)