import machine, onewire, ds18x20, time
from machine import Pin

hystereza = 5

spinac = machine.Pin(18, Pin.OUT)

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

sensor1_waterproof = bytearray(b'(\xffQ\xcb\xc1\x17\x04\xa6')
sensor2_normal = bytearray(b'(\xff\xc6uQ\x17\x04\xec')

spinac.value(1)
time.sleep(1)
spinac.value(0)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    temp_outside = ds_sensor.read_temp(sensor1_waterproof)
    temp_inside = ds_sensor.read_temp(sensor2_normal)
    print(temp_inside, "inside")
    print(temp_outside, "outside")
    if (temp_outside - (hystereza/2)) > temp_inside:
        on_off = "off"
    elif (temp_outside + (hystereza/2)) <= temp_inside:
        on_off = "on"
    print(on_off)
    