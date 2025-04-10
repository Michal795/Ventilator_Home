from machine import Pin, PWM
from time import sleep
import dht

inside = dht.DHT22(Pin(22))
outside = dht.DHT22(Pin(21))
spinac = machine.Pin(18)
pwm_spinac = machine.PWM(spinac)
pwm_spinac.freq(50)
pwm_spinac.duty_u16(0)

hystereza_temp = 4
hystereza_hum = 5
hodnota_temp = 0
hodnota_hum = 0
norma_hum = 80


def spinac_temp(temp_inside, temp_outside, hystereza, pred_stav):
    spinac_hodnota = pred_stav
    if (temp_inside + (hystereza/2)) < temp_outside:
        spinac_hodnota = 0
        pwm_value = 0
    elif (temp_inside - (hystereza/2)) > temp_outside:
        spinac_hodnota = 1
        pwm_value = 1024
    else:
        if pred_stav == 0:
            pwm_value = ((temp_outside - (temp_inside - (hystereza/2))) / hystereza)**2 * 1024
        elif pred_stav == 1:
            pwm_value = 1024 - (((temp_outside - (temp_inside - (hystereza/2))) / hystereza)**2 * 1024)
    return spinac_hodnota, int(round(pwm_value, 0))


def spinac_hum(hystereza, humidity, pred_stav, norma):
    spinac_hodnota = pred_stav
    if (norma - (hystereza/2)) > humidity:
        spinac_hodnota = 1
    elif (norma + (hystereza/2)) < humidity:
        spinac_hodnota = 0
    return spinac_hodnota


while True:
    inside.measure()
    outside.measure()
    temp_inside = float(inside.temperature())
    temp_outside = float(outside.temperature())
    hum_outside = float(outside.humidity())
    '''
    for i in range(25):
        temp_outside = i
        hodnota_temp, pwm_hodnota = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
    for i in range(25, -1, -1):
        temp_outside = i
        hodnota_temp, pwm_hodnota = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
    '''
    print("Inside temp:", temp_inside)
    print("Outside temp:", temp_outside)
    print("Outside humidity:", hum_outside)
    hodnota_temp, pwm_hodnota = spinac_temp(temp_inside, temp_outside, hystereza_temp, hodnota_temp)
    hodnota_hum = spinac_hum(hystereza_hum, hum_outside, hodnota_hum, norma_hum)
    
    if hodnota_hum == 1:
        pwm_spinac.duty_u16(pwm_hodnota)
    else:
        pwm_spinac.duty_u16(0)
        
    print(f"Hodnota temp: {hodnota_temp}\nHodnota hum: {hodnota_hum}")
    print(f"spinac: {pwm_hodnota}")
    
    ###print('Temperature: %3.1f C' %temp_inside)
    ###print('Humidity: %3.1f %%' %hum_outside)
    #hodnota = spinac_def(temp_inside, temp_outside, hystereza)