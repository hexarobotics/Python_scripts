import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import font, ttk

def list_ports():
    ports = list(serial.tools.list_ports.comports())
    return [p.device for p in ports]

def connect_to_port():
    selected_port = port_combobox.get()
    if selected_port:
        try:
            global ser  # Hacer la variable ser global para usarla en otras funciones
            ser = serial.Serial(selected_port, baudrate=115200, timeout=1)
            print(f"Conexión exitosa al puerto {selected_port}")
            status_label.config(text=f"Conectado a {selected_port}", fg="green")
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
            status_label.config(text=f"Error: {e}", fg="red")

def send_message(ser, message):
    ser.write(message.encode())
    time.sleep(0.2)
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
window.geometry("400x400")
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

# Botón para actualizar coordenadas a la derecha de Y, un poco más arriba
update_button = tk.Button(frame, text="Actualizar", command=update_coordinates, bg="#2196F3", fg="white", font=button_font, width=10)
update_button.grid(row=1, column=4, padx=(10, 0))

# Selector de puerto
tk.Label(window, text="Selecciona el puerto COM:", bg="#2E2E2E", fg="#FFFFFF", font=label_font).pack(pady=10)
port_combobox = ttk.Combobox(window, values=list_ports(), width=20)
port_combobox.pack(pady=5)

# Botón para conectar al puerto
connect_button = tk.Button(window, text="Conectar", command=connect_to_port, bg="#2196F3", fg="white", font=button_font)
connect_button.pack(pady=10)

# Etiqueta para mostrar el estado de conexión
status_label = tk.Label(window, text="Desconectado", bg="#2E2E2E", fg="red", font=label_font)
status_label.pack(pady=5)

ser = None  # Inicializar la variable ser

# Loop principal de la interfaz
window.mainloop()
