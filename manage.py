#!/usr/bin/env python
import os
from app import create_app, db
from flask.ext.script import Manager, Shell
from app.models import ScrapeCount, User
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug = True
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, ScrapeCount=ScrapeCount, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    pass

application = manager

if __name__ == '__main__':
    application.run()
