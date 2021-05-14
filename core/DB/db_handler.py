import os
import sqlite3
from flask import current_app, g
import pathlib


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        if not os.path.isfile(current_app.config["DATABASE"]):
            path = os.path.join(pathlib.Path(__file__).parent.absolute(), "schema.sql")
            db = get_db()
            db.cursor().executescript(open(path).read())
            db.commit()
            db.cursor().close()


def register_db(app):
    init_db(app)
    app.teardown_appcontext(close_db)
