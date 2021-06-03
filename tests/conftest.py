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
import pathlib

import pytest
from picure import create_app


@pytest.fixture()
def app():
    db_path = os.path.join(
        pathlib.Path(__file__).resolve().parent.parent,
        "picure/Backend/DB/picure.sqlite",
    )
    if os.path.isfile(db_path):
        os.remove(db_path)

    return create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def program(app):
    insert_path = os.path.join(
        pathlib.Path(__file__).resolve().parent, "program_db_inserts"
    )

    with app.app_context():
        files = [f for f in os.listdir(insert_path) if f.endswith(".sql")]
        files.sort()

        for file in files:
            from picure.Backend.DB.db_handler import get_db

            file_path = os.path.join(insert_path, file)

            get_db().cursor().executescript(open(file_path).read())
            get_db().commit()
            get_db().cursor().close()

        from picure.Backend.Program.controler import get_current_program

        return get_current_program()
