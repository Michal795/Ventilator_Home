import machine, onewire, ds18x20, time
from machine import Pin

def teplomer(pin_port, poradove_c, kompenzacia):
    ds_pin = machine.Pin(pin_port)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    ds_sensor.convert_temp()
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms, f"\nOn pin{pin_port}")
    teplota = ds_sensor.read_temp(roms[poradove_c])
    return (teplota + kompenzacia)

def spinac(temp_inside, temp_outside, hystereza):
    if (temp_outside - (hystereza/2)) > temp_inside:
        my_value = 0
    elif (temp_outside + (hystereza/2)) < temp_inside:
        my_value = 1
    return my_value

hystereza = 5
value_moja = 0

spinac = machine.Pin(18, Pin.OUT)
sensor1_waterproof = bytearray(b'(\xffQ\xcb\xc1\x17\x04\xa6')
sensor2_normal = bytearray(b'(\xff\xc6uQ\x17\x04\xec')

while True:
    #current_date = datetime.datetime.now().month
    temp_outside = teplomer(22, 0, -0.5)
    temp_inside = teplomer(22, 1, 0)
    print("Inside:", temp_inside)
    print("Outside:", temp_outside)
    value_moja = spinac(temp_inside, temp_outside, hystereza)
    spinac.value(value_moja)
