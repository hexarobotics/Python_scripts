import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import font

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
    time.sleep(0.1)
    return ser.read_all().decode('utf-8', errors='replace').strip()

def update_coordinates():
    x = x_var.get()
    y = y_var.get()
    z = z_var.get()
    command = f"{x},{y},{z}"
    response = send_message(ser, command)
    print("ESP32 >", response)

# Configuración de la ventana principal
window = tk.Tk()
window.title("Controlador de Servomotor")
window.geometry("400x300")
window.configure(bg="#2E2E2E")  # Color de fondo oscuro

# Estilo de la fuente
label_font = font.Font(family="Helvetica", size=12, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# Variables para las coordenadas
x_var = tk.IntVar(value=0)
y_var = tk.IntVar(value=0)
z_var = tk.IntVar(value=0)

# Etiquetas y campos para coordenadas
tk.Label(window, text="Coordenadas", bg="#2E2E2E", fg="#FFFFFF", font=label_font).pack(pady=10)

frame = tk.Frame(window, bg="#2E2E2E")
frame.pack(pady=10)

# Fila para X
tk.Label(frame, text="X:", bg="#2E2E2E", fg="#FFFFFF", font=label_font).grid(row=0, column=0)
tk.Entry(frame, textvariable=x_var, width=5).grid(row=0, column=1)
tk.Button(frame, text="+", command=lambda: x_var.set(x_var.get() + 1), bg="#4CAF50", fg="white", font=button_font, width=3).grid(row=0, column=2, padx=(5, 0))
tk.Button(frame, text="-", command=lambda: x_var.set(x_var.get() - 1), bg="#F44336", fg="white", font=button_font, width=3).grid(row=0, column=3, padx=(5, 0))

# Fila para Y
tk.Label(frame, text="Y:", bg="#2E2E2E", fg="#FFFFFF", font=label_font).grid(row=1, column=0)
tk.Entry(frame, textvariable=y_var, width=5).grid(row=1, column=1)
tk.Button(frame, text="+", command=lambda: y_var.set(y_var.get() + 1), bg="#4CAF50", fg="white", font=button_font, width=3).grid(row=1, column=2, padx=(5, 0))
tk.Button(frame, text="-", command=lambda: y_var.set(y_var.get() - 1), bg="#F44336", fg="white", font=button_font, width=3).grid(row=1, column=3, padx=(5, 0))

# Fila para Z
tk.Label(frame, text="Z:", bg="#2E2E2E", fg="#FFFFFF", font=label_font).grid(row=2, column=0)
tk.Entry(frame, textvariable=z_var, width=5).grid(row=2, column=1)
tk.Button(frame, text="+", command=lambda: z_var.set(z_var.get() + 1), bg="#4CAF50", fg="white", font=button_font, width=3).grid(row=2, column=2, padx=(5, 0))
tk.Button(frame, text="-", command=lambda: z_var.set(z_var.get() - 1), bg="#F44336", fg="white", font=button_font, width=3).grid(row=2, column=3, padx=(5, 0))

# Botón para actualizar las coordenadas
update_button = tk.Button(window, text="Actualizar Coordenadas", command=update_coordinates, bg="#2196F3", fg="white", font=button_font, width=20)
update_button.pack(pady=20)

ser = connect_to_port(list_ports())

# Loop principal de la interfaz
window.mainloop()
