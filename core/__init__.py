#      PiCure - Meat dry ageing and curing
#      Copyright (C) <2021>  <Markus Hupfauer>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask

from core.API.loggerio import loggerio
from core.API.state_control import control
from core.Backend.Scheduler import scheduler
from core.DB import db_handler


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.root_path, "DB/picure.sqlite"),
        SCHEDULER_JOBSTORES={
            "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
        },
        SCHEDULER_API_ENABLED=False,
    )

    db_handler.register_db(app)
    app.register_blueprint(control)
    app.register_blueprint(loggerio)
    scheduler.init_app(app)

    with app.app_context():
        from core.Backend.Scheduler import logging_tasks

        scheduler.start()

    return app
