#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector as mc
import tetueSrc
import datetime
import pathlib

read_successful, cfg = tetueSrc.get_configuration("database")


def open_connection():
    connection = mc.connect(host=cfg["host"], user=cfg["user"], passwd=cfg["password"], db=cfg["database"])
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def add_new_measurement(room_id: int, **kwargs):
    try:
        connection, cursor = open_connection()
        query = "INSERT INTO measurements (room_id, sample_nr, iaq, iaq_accuracy, " \
                "static_iaq, static_iaq_accuracy, co2_equivalent, co2_accuracy, " \
                "breath_voc_equivalent, breath_voc_accuracy, raw_temperature, raw_pressure, " \
                "raw_humidity, raw_gas, stabilization_status, run_in_status, temperature, humidity, " \
                "comp_gas_value, comp_gas_accuracy, gas_percentage, gas_percentage_accuracy) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (room_id, kwargs["sample_nr"], kwargs["iaq"], kwargs["iaq_accuracy"], kwargs["static_iaq"],
               kwargs["static_iaq_accuracy"], kwargs["co2_equivalent"], kwargs["co2_accuracy"],
               kwargs["breath_voc_equivalent"], kwargs["breath_voc_accuracy"], kwargs["raw_temperature"],
               kwargs["raw_pressure"], kwargs["raw_humidity"], kwargs["raw_gas"], kwargs["stabilization_status"],
               kwargs["run_in_status"], kwargs["temperature"], kwargs["humidity"], kwargs["comp_gas_value"],
               kwargs["comp_gas_accuracy"], kwargs["gas_percentage"], kwargs["gas_percentage_accuracy"])
        cursor.execute(query, val)
        connection.commit()
        close_connection(connection, cursor)
    except mc.Error as err:
        f = open(pathlib.Path(tetueSrc.absolute_project_path, "files/backup_measurement.txt"), "a")
        f.write(f"{datetime.datetime.now()}\n")
        f.write(f"{err}\n")
        f.write(str(kwargs))
        f.write("\n")
        f.close()


def main():
    pass


if __name__ == "__main__":
    main()
