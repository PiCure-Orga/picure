/*
 *     PiCure - Meat dry ageing and curing
 *     Copyright (C) <2021>  <Markus Hupfauer>
 *
 *     This program is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     This program is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

DROP TABLE IF EXISTS latest_30_days;
DROP TABLE IF EXISTS latest_10_minutes;
DROP TABLE IF EXISTS cure_program;
DROP TABLE IF EXISTS cure_program_action_tasks;
DROP TABLE IF EXISTS cure_program_actions;
DROP TABLE IF EXISTS cure_program_step;
DROP TABLE IF EXISTS cure_program_step_targets;


CREATE TABLE latest_10_minutes(
    id INTEGER,
    timestamp INTEGER,
    sensor TEXT,
    value DECIMAL(4,2),
    PRIMARY KEY (id)
);
CREATE TABLE latest_30_days(
    id INTEGER,
    timestamp INTEGER,
    sensor TEXT,
    value DECIMAL(4,2),
    PRIMARY KEY (id)
);
CREATE TABLE cure_program(
    id INTEGER,
    name TEXT,
    comments TEXT,
    PRIMARY KEY (id)
);
CREATE TABLE cure_program_step(
    id INTEGER,
    cure_program_id INTEGER,
    duration int NOT NULL,
    name TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (cure_program_id) REFERENCES cure_program(id)
);
CREATE TABLE cure_program_step_targets(
    id INTEGER,
    cure_program_step_id INTEGER,
    sensor TEXT NOT NULL,
    target_value DECIMAL(4,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (cure_program_step_id) REFERENCES cure_program_step(id)
);
CREATE TABLE cure_program_actions(
    id INTEGER,
    cure_program_id INTEGER,
    sensor TEXT NOT NULL,
    eval TEXT NOT NULL,
    derivation DECIMAL(4,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (cure_program_id) REFERENCES cure_program(id)
);
CREATE TABLE cure_program_action_tasks(
    id INTEGER,
    cure_program_action_id INTEGER,
    hardware TEXT NOT NULL,
    task_enum INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (cure_program_action_id) REFERENCES cure_program_actions(id)
);