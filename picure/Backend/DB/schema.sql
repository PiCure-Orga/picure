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
DROP TABLE IF EXISTS program;
DROP TABLE IF EXISTS step;
DROP TABLE IF EXISTS target;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS program_run;
DROP TABLE IF EXISTS event_log;
DROP TABLE IF EXISTS step_log;


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
CREATE TABLE program(
    id INTEGER,
    name TEXT,
    comments TEXT,
    PRIMARY KEY (id)
);
CREATE TABLE event(
    id INTEGER,
    program_id INTEGER,
    name TEXT,
    sensor TEXT,
    eval TEXT,
    derivation DECIMAL(4,2),
    PRIMARY KEY (id),
    FOREIGN KEY (program_id) REFERENCES program(id) ON DELETE CASCADE
);
CREATE TABLE task(
    id INTEGER,
    event_id INTEGER,
    name TEXT,
    hardware TEXT,
    action INTEGER,
    duration INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);
CREATE TABLE step(
    id INTEGER,
    program_id INTEGER,
    duration INTEGER,
    step_order INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (program_id) REFERENCES program(id) ON DELETE CASCADE
);
CREATE TABLE target(
    id INTEGER,
    step_id INTEGER,
    sensor TEXT,
    value DECIMAL(4,2),
    PRIMARY KEY (id),
    FOREIGN KEY (step_id) REFERENCES step(id) ON DELETE CASCADE
);
CREATE TABLE program_run(
    id INTEGER,
    program_id INTEGER,
    enabled INTEGER,
    paused INTEGER,
    start_timestamp INTEGER,
    pause_timestamp INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (program_id) REFERENCES program(id) ON DELETE CASCADE
);
CREATE TABLE event_log(
    id INTEGER,
    program_run_id INTEGER,
    timestamp INTEGER,
    event_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (program_run_id) REFERENCES program_run(id) ON DELETE CASCADE ,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);
CREATE TABLE step_log(
    id INTEGER,
    program_run_id INTEGER,
    timestamp INTEGER,
    step_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (program_run_id) REFERENCES program_run(id) ON DELETE CASCADE ,
    FOREIGN KEY (step_id) REFERENCES step(id) ON DELETE CASCADE
);