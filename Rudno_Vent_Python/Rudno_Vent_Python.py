from machine import Pin
from time import sleep
import dht

inside = dht.DHT22(Pin(22))
outside = dht.DHT22(Pin(21))
spinac = machine.Pin(18, Pin.OUT)
hystereza_temp = 3
hystereza_hum = 5
hodnota_temp = 0
hodnota_hum = 0
norma_hum = 80


def spinac_temp(temp_inside, temp_outside, hystereza, pred_stav):
    spinac_hodnota = pred_stav
    if (temp_inside + (hystereza/2)) < temp_outside:
        spinac_hodnota = 0
    elif (temp_inside - (hystereza/2)) > temp_outside:
        spinac_hodnota = 1
    return  spinac_hodnota


def spinac_hum(hystereza, humidity, pred_stav, norma):
    spinac_hodnota = pred_stav
    if (norma - (hystereza/2)) > humidity:
        spinac_hodnota = 1
    elif (norma + (hystereza/2)) < humidity:
        spinac_hodnota = 0
    return spinac_hodnota


while True:
    sleep(1)
    inside.measure()
    outside.measure()
    temp_inside = float(inside.temperature())
    temp_outside = float(outside.temperature())
    hum_outside = float(outside.humidity())
    print("Inside temp:", temp_inside)
    print("Outside temp:", temp_outside)
    print("Outside humidity:", hum_outside)
    hodnota_temp = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
    hodnota_hum = spinac_hum(hystereza_hum, hum_outside, hodnota_hum, norma_hum)
    
    if hodnota_temp == 1 and hodnota_hum == 1:
        hodnota = 1
    else:
        hodnota = 0
        
    spinac.value(hodnota)
    print(f"Hodnota temp: {hodnota_temp}\nHodnota hum: {hodnota_hum}")
    print(f"spinac: {hodnota}")
    
    ###print('Temperature: %3.1f C' %temp_inside)
    ###print('Humidity: %3.1f %%' %hum_outside)
    #hodnota = spinac_def(temp_inside, temp_outside, hystereza)


