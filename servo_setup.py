import serial
import serial.tools.list_ports
import time

def list_ports():
    # Listar todos los puertos COM disponibles
    print("Puertos COM disponibles:")
    ports = list(serial.tools.list_ports.comports())
    for i, p in enumerate(ports):
        print(f"{i}: {p.device} - {p.description}")
    return ports

def connect_to_port(ports):
    # Si hay puertos disponibles, intentar conectarse al que selecciones
    if ports:
        # Permitir que el usuario seleccione un puerto si hay más de uno
        if len(ports) > 1:
            port_index = int(input(f"Selecciona el puerto (0-{len(ports) - 1}): "))
            port = ports[port_index].device
        else:
            port = ports[0].device
        
        print(f"\nIntentando conectar al puerto: {port}")
        try:
            ser = serial.Serial(port, baudrate=115200, timeout=1, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            print(f"Conexión exitosa al puerto {port}")
            return ser
        except serial.SerialException as e:
            print(f"\nError al abrir el puerto serial: {e}")
        except Exception as e:
            print(f"\nOcurrió un error inesperado: {e}")
    else:
        print("\nNo se encontraron puertos COM disponibles.")
    return None

def send_message(ser, message):
    # Envía el mensaje al ESP32
    ser.write(message.encode())
    
    # Espera la respuesta del ESP32
    time.sleep(0.1)
    response = ser.read_all().decode('utf-8')
    return response

def main():
    ports = list_ports()
    
    # Intentar conectar al puerto
    ser = connect_to_port(ports)
    
    if ser:
        print("\nConectado a la ESP32. Escribe tus comandos (escribe 'exit' para salir):")
        try:
            while True:
                # Leer el mensaje del usuario
                user_input = input("Tú > ")
                
                # Enviar el mensaje al ESP32
                if user_input.lower() == 'exit':
                    print("Cerrando conexión...")
                    break
                response = send_message(ser, user_input)
                
                # Mostrar la respuesta del ESP32
                print("ESP32 >", response)
        
        except KeyboardInterrupt:
            print("\nInterrupción por teclado. Cerrando...")
        finally:
            ser.close()
    print("\nFin del programa")

if __name__ == "__main__":
    main()
