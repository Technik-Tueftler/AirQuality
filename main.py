#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bme68x import BME68X
import bme68xConstants as cst
import bsecConstants as bsec
from time import sleep


def main() -> None:
    print('\nTESTING FORCED MODE WITH BSEC')
    bme = BME68X(cst.BME68X_I2C_ADDR_HIGH, 1)
    bme.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)

    def get_data(sensor):
        data = {}
        try:
            data = sensor.get_bsec_data()
        except Exception as e:
            print(e)
            return None
        if data == None or data == {}:
            sleep(0.1)
            print("Fehler 1")
            return None
        else:
            sleep(3)
            return data

    bsec_data = get_data(bme)
    while bsec_data == None:
        bsec_data = get_data(bme)
    print(bsec_data)

    bsec_data = None
    while bsec_data == None:
        bsec_data = get_data(bme)
    print(bsec_data)


if __name__ == "__main__":
    main()
