import Adafruit_DHT
import time 
sensor = Adafruit_DHT.DHT11
pin = 4

def temperature(): 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
	    return 'La temperatura es de {0:0.1f} grados centigrados, con una humedad de: {1:0.1f} porciento'.format(temperature, humidity)
    else:
	    return 'No pude obtener la temperatura de mi sensor, vuelvelo a intentar por favor!'




