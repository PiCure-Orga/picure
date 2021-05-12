import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask

from core.API.state_control import control
from core.Backend.Scheduler import scheduler
from core.DB import db_handler


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'DB/picure.sqlite'),
        SCHEDULER_JOBSTORES={"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")},
        SCHEDULER_API_ENABLED=False
    )

    db_handler.register_db(app)
    app.register_blueprint(control)
    scheduler.init_app(app)

    with app.app_context():
        from core.Backend.Scheduler import logging_tasks
        scheduler.start()

    return app
