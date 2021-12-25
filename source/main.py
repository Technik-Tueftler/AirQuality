from bme68x import BME68X
import bme68xConstants as cst
import bsecConstants as bsec
from time import sleep
import db

print("Start sensor 1 - Keller Arbeitszimmer")
bme = BME68X(cst.BME68X_I2C_ADDR_HIGH, 1)
bme.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)


def get_data(sensor):
    data = {}
    try:
        data = sensor.get_bsec_data()
    except Exception as e:
        print(e)
        return None
    if data is None or data == {}:
        sleep(0.1)
        print("Fehler 1")
        return None
    else:
        sleep(3)
        return data


try:
    while True:
        bsec_data = get_data(bme)
        while bsec_data is None:
            bsec_data = get_data(bme)
        print(bsec_data)
        db.add_new_measurement(1, **bsec_data)
        sleep(897)
except KeyboardInterrupt:
    print("\nBeenden durch Tastatur")

print("Ende sensor 1 - Keller Arbeitszimmer")
