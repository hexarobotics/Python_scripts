import serial
import serial.tools.list_ports
import time

# Listar todos los puertos COM disponibles
print("Puertos COM disponibles:")
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

# Comentamos la línea original que causaba el error
# ser = serial.Serial('COM3', baudrate=115200, timeout=1)

# Intento de conexión con manejo de errores
try:
    # Intentamos conectar al primer puerto disponible (si existe alguno)
    if ports:
        port = ports[0].device
        print(f"\nIntentando conectar al puerto: {port}")
        ser = serial.Serial(port, baudrate=115200, timeout=1)
        print(f"Conexión exitosa al puerto {port}")
        
        # Aquí puedes agregar el resto de tu código para trabajar con el servo
        # Por ejemplo:
        # time.sleep(2)  # Espera 2 segundos
        # ser.write(b'algún comando')  # Envía un comando al servo
        
        ser.close()  # Cierra la conexión cuando hayas terminado
    else:
        print("\nNo se encontraron puertos COM disponibles.")
except serial.SerialException as e:
    print(f"\nError al abrir el puerto serial: {e}")
except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")

print("\nFin del programa")