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

from flask import Blueprint, render_template
from picure.Backend.hardware_controller import get_hardware_states
from picure.Backend.Program.controler import get_dict_of_programs

index = Blueprint("index", __name__, template_folder="templates")


@index.route("/")
def get_main_page():
    return render_template("index.html", states=get_hardware_states().items())


@index.route("/program")
def get_program_page():
    return render_template("program.html", program=get_dict_of_programs().values())


@index.route("/program/<int:id>")
def edit_program(id):
    return render_template("edit_program.html")
