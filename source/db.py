#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, ForeignKey, TIMESTAMP, func, and_, or_
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, relationship, query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import tetueSrc

read_successful, cfg = tetueSrc.get_configuration("database")
Base = declarative_base()
engine = create_engine(
    f'mariadb+mariadbconnector://{cfg["user"]}:{cfg["password"]}@{cfg["host"]}:{cfg["port"]}/{cfg["database"]}')


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    floor = Column(Integer, nullable=False, default=0)
    name = Column(String(100), nullable=False)
    measurements = relationship('Measurement', backref='room')


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    sample_nr = Column(Integer, nullable=False, default=0)
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("NOW()"))
    iaq = Column(Float, nullable=False, default=0)
    iaq_accuracy = Column(Integer, nullable=False, default=0)
    static_iaq = Column(Float, nullable=False, default=0)
    static_iaq_accuracy = Column(Integer, nullable=False, default=0)
    co2_equivalent = Column(Float, nullable=False, default=0)
    co2_accuracy = Column(Integer, nullable=False, default=0)
    breath_voc_equivalent = Column(Float, nullable=False, default=0)
    breath_voc_accuracy = Column(Integer, nullable=False, default=0)
    raw_temperature = Column(Float, nullable=False, default=0)
    raw_pressure = Column(Float, nullable=False, default=0)
    raw_humidity = Column(Float, nullable=False, default=0)
    raw_gas = Column(Float, nullable=False, default=0)
    stabilization_status = Column(Float, nullable=False, default=0)
    run_in_status = Column(Float, nullable=False, default=0)
    temperature = Column(Float, nullable=False, default=0)
    humidity = Column(Float, nullable=False, default=0)
    comp_gas_value = Column(Float, nullable=False, default=0)
    comp_gas_accuracy = Column(Integer, nullable=False, default=0)
    gas_percentage = Column(Float, nullable=False, default=0)
    gas_percentage_accuracy = Column(Integer, nullable=False, default=0)


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
session = session()


def commit(function):
    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)
        session.commit()
        return return_value
    return wrapper


#@commit
def add_new_measurement(**kwargs):
    new_measurement = Measurement(room_id=kwargs["room_id"],
                                  sample_nr=kwargs["sample_nr"],
                                  iaq=kwargs["iaq"],
                                  iaq_accuracy=kwargs["iaq_accuracy"],
                                  static_iaq=kwargs["static_iaq"],
                                  static_iaq_accuracy=kwargs["static_iaq_accuracy"],
                                  co2_equivalent=kwargs["co2_equivalent"],
                                  co2_accuracy=kwargs["co2_accuracy"],
                                  breath_voc_equivalent=kwargs["breath_voc_equivalent"],
                                  breath_voc_accuracy=kwargs["breath_voc_accuracy"],
                                  raw_temperature=kwargs["raw_temperature"],
                                  raw_pressure=kwargs["raw_pressure"],
                                  raw_humidity=kwargs["raw_humidity"],
                                  raw_gas=kwargs["raw_gas"],
                                  stabilization_status=kwargs["stabilization_status"],
                                  run_in_status=kwargs["run_in_status"],
                                  temperature=kwargs["temperature"],
                                  humidity=kwargs["humidity"],
                                  comp_gas_value=kwargs["comp_gas_value"],
                                  comp_gas_accuracy=kwargs["comp_gas_accuracy"],
                                  gas_percentage=kwargs["gas_percentage"],
                                  gas_percentage_accuracy=kwargs["gas_percentage_accuracy"]
                                  )
    session.add(new_measurement)


def main():
    measurement = {'sample_nr': 1, 'timestamp': 5448467805395, 'iaq': 25.0, 'iaq_accuracy': 0, 'static_iaq': 25.0, 'static_iaq_accuracy': 0, 'co2_equivalent': 500.0, 'co2_accuracy': 0, 'breath_voc_equivalent': 0.4999999403953552, 'breath_voc_accuracy': 0, 'raw_temperature': 22.507539749145508, 'raw_pressure': 100748.109375, 'raw_humidity': 64.39527130126953, 'raw_gas': 704.9998779296875, 'stabilization_status': 0, 'run_in_status': 0, 'temperature': 22.507539749145508, 'humidity': 64.39527130126953, 'comp_gas_value': 3.679572105407715, 'comp_gas_accuracy': 0, 'gas_percentage': 0.0, 'gas_percentage_accuracy': 0}
    add_new_measurement(**measurement)
    pass


if __name__ == "__main__":
    main()
