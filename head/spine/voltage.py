def get_battery_voltage():
    n = 5
    avg_adc_val = 0
    for i in range(n):
        with open('/sys/devices/ocp.3/helper.15/AIN1') as f:
            adc_val = float(f.read())
            avg_adc_val += adc_val / n
    r1 = 10000.0
    r2 = 2200.0
    vout = 1.8 * adc_val / 1799.0
    vbat = vout / (r2/(r1+r2))
    return vbat
