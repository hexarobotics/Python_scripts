import serial
import time

# Configuración del puerto serial en Windows
# Asegúrate de cambiar 'COM3' por el puerto correcto de tu ESP32
ser = serial.Serial('COM3', baudrate=115200, timeout=1)

def send_message(message):
    # Envía el mensaje al ESP32
    ser.write(message.encode())
    
    # Espera la respuesta del ESP32
    time.sleep(0.1)
    response = ser.read_all().decode('utf-8')
    return response

def main():
    print("Conectado a la ESP32. Escribe tus comandos:")
    try:
        while True:
            # Leer el mensaje del usuario
            user_input = input("Tú > ")
            
            # Enviar el mensaje al ESP32
            if user_input.lower() == 'exit':
                print("Cerrando conexión...")
                break
            response = send_message(user_input)
            
            # Mostrar la respuesta del ESP32
            print("ESP32 >", response)
    
    except KeyboardInterrupt:
        print("Interrupción por teclado. Cerrando...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()