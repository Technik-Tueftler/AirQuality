from bme68x import BME68X
import bme68xConstants as cnst
import bsecConstants as bsec
import time
from datetime import datetime, timedelta
import db

print("Start sensor 1 - Keller Arbeitszimmer")

"""temp_prof = [50, 50, 350, 350, 350, 140, 140, 350, 350, 350]
dur_prof = [9800, 9800, 140, 140, 19320, 9800, 9800, 140, 140, 19320]
print("Start Kalibrierung mit Heizprofil HP-331 - Dauer ca. 78,4 Sekunden")
# 567.774761, 272.294563
start_time = datetime.datetime.now()
sensor = BME68X(cnst.BME68X_I2C_ADDR_HIGH, 0)
print(sensor.get_data())
print(sensor.set_heatr_conf(cnst.BME68X_ENABLE, temp_prof, dur_prof, cnst.BME68X_SEQUENTIAL_MODE))
print(sensor.get_data())
print("Kalibrierung mit Heizprofil HP-331 abgeschlossen")
end_time = datetime.datetime.now()
print(f"Gesamtzeit für Kalibrierung: {(end_time-start_time).total_seconds()}")"""

print("Start zyklische Messung")
delta_push_to_database_time = timedelta(seconds=297)
last_push_to_database_time = datetime.now()

sensor = BME68X(cnst.BME68X_I2C_ADDR_HIGH, 0)
sensor.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)


def get_data(sensor):
    data = {}
    try:
        data = sensor.get_bsec_data()
    except Exception as e:
        print(e)
        return None
    if data is None or data == {}:
        time.sleep(0.1)
        return None
    else:
        time.sleep(3)
        return data


try:
    while True:
        bsec_data = get_data(sensor)
        while bsec_data is None:
            bsec_data = get_data(sensor)
        """print(f'Nr.: {bsec_data["sample_nr"]}'.center(140, "-"))
        print(bsec_data)
        db.add_new_measurement(1, **bsec_data)
        time.sleep(297)"""
        if (datetime.now() - last_push_to_database_time) >= delta_push_to_database_time:
            db.add_new_measurement(1, **bsec_data)
            last_push_to_database_time = datetime.now()
except KeyboardInterrupt:
    print("\nBeenden durch Tastatur")

print("Ende sensor 1 - Keller Arbeitszimmer")
