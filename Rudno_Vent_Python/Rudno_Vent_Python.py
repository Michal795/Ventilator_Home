import machine, onewire, ds18x20, time
from machine import Pin

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
spinac = machine.Pin(18, Pin.OUT)
hystereza_temp = 3
hodnota_temp = 0


def spinac_temp(temp_inside, temp_outside, hystereza, pred_stav): #leto - vonku musi byt chladnejsie, ako vnutri
    spinac_hodnota = pred_stav
    if (temp_inside + (hystereza/2)) < temp_outside:
        spinac_hodnota = 0
    elif (temp_inside - (hystereza/2)) > temp_outside:
        spinac_hodnota = 1
    return  spinac_hodnota


while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    temp_inside = ds_sensor.read_temp(bytearray(b'(R\xb6\xbc\x00\x00\x00\x0e'))
    temp_outside = ds_sensor.read_temp(bytearray(b'(\xd7\xbe\xbc\x00\x00\x001'))
    print("Inside temp:", temp_inside)
    print("Outside temp:", temp_outside)
    hodnota_temp = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
    spinac.value(hodnota_temp)
    print(f"Hodnota temp: {hodnota_temp}")
    time.sleep(1)

# vonku = bytearray(b'(\xd7\xbe\xbc\x00\x00\x001')
# vnutri = bytearray(b'(R\xb6\xbc\x00\x00\x00\x0e')