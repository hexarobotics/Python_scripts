import serial
import serial.tools.list_ports
import tkinter as tk

# Conexión al puerto serial (ajusta según sea necesario)
def connect_to_port():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        ser = serial.Serial(ports[0].device, baudrate=115200, timeout=1)
        return ser
    return None

# Enviar coordenadas al ESP32
def send_coordinates():
    coordinates = f"{x_var.get()},{y_var.get()},{z_var.get()}\n"  # Formato: x,y,z
    ser.write(coordinates.encode())
    print(f"Enviando: {coordinates.strip()}")  # Mostrar en consola

# Incrementar/decrementar coordenadas
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
ser = connect_to_port()
if ser:
    root = tk.Tk()
    root.title("Control de Coordenadas")

    # Variables para las coordenadas
    x_var = tk.IntVar(value=-155)
    y_var = tk.IntVar(value=0)
    z_var = tk.IntVar(value=-70)

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

    root.mainloop()
else:
    print("No se pudo conectar al puerto serial.")
