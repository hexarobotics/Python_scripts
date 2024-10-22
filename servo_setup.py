import serial
import serial.tools.list_ports
import time
import tkinter as tk

def list_ports():
    # Listar todos los puertos COM disponibles
    ports = list(serial.tools.list_ports.comports())
    print("Puertos COM disponibles:", "\n".join(f"{i}: {p.device} - {p.description}" for i, p in enumerate(ports)))
    return ports

def connect_to_port(ports):
    # Conexión al puerto seleccionado
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

def send_coordinates():
    # Enviar coordenadas al ESP32
    coordinates = f"{x_var.get()},{y_var.get()},{z_var.get()}\n"  # Formato: x,y,z
    ser.write(coordinates.encode())
    print(f"Enviando: {coordinates.strip()}")  # Mostrar en consola

def increment_x():
    x_var.set(x_var.get() + 1)

def decrement_x():
    x_var.set(x_var.get() - 1)

def increment_y():
    y_var.set(y_var.get() + 1)

def decrement_y():
    y_var.set(y_var.get() - 1)

def increment_z():
    z_var.set(z_var.get() + 1)

def decrement_z():
    z_var.set(z_var.get() - 1)

# Configuración de la ventana principal
ports = list_ports()
ser = connect_to_port(ports)

if ser:
    root = tk.Tk()
    root.title("Control de Coordenadas")

    # Variables para las coordenadas
    x_var = tk.IntVar(value=0)
    y_var = tk.IntVar(value=0)
    z_var = tk.IntVar(value=0)

    # Campos de coordenadas
    tk.Label(root, text="Coordenadas").grid(row=0, columnspan=4)

    tk.Label(root, text="X:").grid(row=1, column=0)
    tk.Label(root, textvariable=x_var).grid(row=1, column=1)
    tk.Button(root, text="+", command=increment_x).grid(row=1, column=2)
    tk.Button(root, text="-", command=decrement_x).grid(row=1, column=3)

    tk.Label(root, text="Y:").grid(row=2, column=0)
    tk.Label(root, textvariable=y_var).grid(row=2, column=1)
    tk.Button(root, text="+", command=increment_y).grid(row=2, column=2)
    tk.Button(root, text="-", command=decrement_y).grid(row=2, column=3)

    tk.Label(root, text="Z:").grid(row=3, column=0)
    tk.Label(root, textvariable=z_var).grid(row=3, column=1)
    tk.Button(root, text="+", command=increment_z).grid(row=3, column=2)
    tk.Button(root, text="-", command=decrement_z).grid(row=3, column=3)

    tk.Button(root, text="Actualizar", command=send_coordinates).grid(row=4, columnspan=4)

    # Ciclo principal de la interfaz
    root.mainloop()

    # Cierre de conexión al finalizar
    ser.close()
else:
    print("No se pudo conectar al puerto serial.")
