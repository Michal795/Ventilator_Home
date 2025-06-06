import machine, onewire, ds18x20, time, _thread
from machine import Pin

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
spinac = machine.Pin(18, Pin.OUT)
hystereza_temp = 3
hodnota_temp = 0
teploty = []
pocitadlo = 0
obdobie = "leto"
priemer_teplot = 0

def measure_every_8_hours():
    global pocitadlo, priemer_teplot, obdobie
    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        temp_outside = ds_sensor.read_temp(bytearray(b'(\xd7\xbe\xbc\x00\x00\x001'))
        teploty.append(temp_outside)
        pocitadlo += 1
        if pocitadlo >= 3:
            priemer_teplot = (teploty[0] + teploty[1] + teploty[2])/3
            if priemer_teplot > 12:
                obdobie = "leto"
            else:
                obdobie = "zima"
            teploty.clear()
        time.sleep(8 * 3600)


def spinac_temp(temp_inside, temp_outside, hystereza, pred_stav): # aj leto, aj zima
    spinac_hodnota = pred_stav
    if (temp_inside + (hystereza/2)) < temp_outside:
        spinac_hodnota = 0
    elif (temp_inside - (hystereza/2)) > temp_outside:
        spinac_hodnota = 1
    return  spinac_hodnota



def main_program():
    global hodnota_temp
    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        temp_inside = ds_sensor.read_temp(bytearray(b'(R\xb6\xbc\x00\x00\x00\x0e'))
        temp_outside = ds_sensor.read_temp(bytearray(b'(\xd7\xbe\xbc\x00\x00\x001'))
        print("Inside temp:", temp_inside)
        print("Outside temp:", temp_outside)
        if obdobie == "leto":
            hodnota_temp = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
        else:
            hodnota_temp = spinac_temp(temp_outside, temp_inside, hystereza_temp, hodnota_temp)
        spinac.value(hodnota_temp)
        print(f"Hodnota temp: {hodnota_temp}")
        time.sleep(1)

_thread.start_new_thread(measure_every_8_hours, ())
main_program()

# vonku = bytearray(b'(\xd7\xbe\xbc\x00\x00\x001')
# vnutri = bytearray(b'(R\xb6\xbc\x00\x00\x00\x0e')