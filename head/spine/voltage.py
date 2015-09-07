def get_battery_voltage():
    n = 5
    avg_adc_val = 0
    for i in range(n):
        with open('/sys/devices/ocp.3/helper.15/AIN5') as f:
            adc_val = float(f.read())
            avg_adc_val += adc_val / n
    r1 = 9990.0 + 255.0
    r2 = 2197.0
    offset = 14

    vadc = (adc_val + offset) / 1000

    #vout = 1.8 * adc_val / 1799.0
    vbat = (vadc) / (r2 / (r1 + r2))
    return vbat
