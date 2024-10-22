import serial
import serial.tools.list_ports
import time

def list_ports():
    ports = list(serial.tools.list_ports.comports())
    print("Puertos COM disponibles:", "\n".join(f"{i}: {p.device} - {p.description}" for i, p in enumerate(ports)))
    return ports

def connect_to_port(ports):
    if ports:
        port = ports[0].device if len(ports) == 1 else ports[int(input(f"Selecciona el puerto (0-{len(ports) - 1}): "))].device
        try:
            ser = serial.Serial(port, baudrate=115200, timeout=1)
            print(f"Conexión exitosa al puerto {port}")
            return ser
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
    else:
        print("No se encontraron puertos COM disponibles.")
    return None

def send_message(ser, message):
    ser.write(message.encode())
    time.sleep(0.2)
    return ser.read_all().decode('utf-8', errors='replace').strip()

def main():
    ser = connect_to_port(list_ports())
    if ser:
        print("Conectado a la ESP32. Escribe tus comandos (escribe 'exit' para salir):")
        try:
            while (user_input := input("Tú > ")) != 'exit':
                response = send_message(ser, user_input)
                print("ESP32 >", response)
        except KeyboardInterrupt:
            print("\nInterrupción por teclado. Cerrando...")
        finally:
            ser.close()
    print("\nFin del programa")

if __name__ == "__main__":
    main()
