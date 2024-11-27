import tkinter as tk
from tkinter import messagebox, ttk
import re
import os

# Función para cargar archivos de log desde todas las carpetas de logs comunes
def cargar_archivos():
    carpetas = ["/var/log", "C:\\xampp\\apache\\logs", "C:\\Program Files\\Apache Group\\Apache2\\logs"]  # Rutas comunes a revisar
    archivos_log = []

    for carpeta in carpetas:
        if os.path.exists(carpeta):
            archivos_log += [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.log')]

    if archivos_log:
        combo_archivos['values'] = archivos_log
        combo_archivos.current(0)  # Seleccionar el primer archivo por defecto
        messagebox.showinfo("Cargar Archivos", f"Archivos cargados de: {', '.join(carpetas)}")
    else:
        messagebox.showwarning("Advertencia", "No se encontraron archivos .log en las carpetas especificadas.")

# Función para cargar el archivo seleccionado del dropdown
def cargar_archivo_seleccionado(event):
    ruta_archivo = combo_archivos.get()
    if ruta_archivo:
        with open(ruta_archivo, "r") as file:
            log_text.delete(1.0, tk.END)  # Limpiar el visor antes de cargar el nuevo archivo
            log_text.insert(tk.END, file.read())
        messagebox.showinfo("Cargar Archivo", f"Archivo cargado: {ruta_archivo}")

# Función para realizar la búsqueda en el archivo de log
def buscar_logs():
    criterio = entry_buscar.get()
    if not criterio:
        messagebox.showwarning("Advertencia", "Debe ingresar un criterio de búsqueda.")
        return
    
    contenido = log_text.get(1.0, tk.END)
    patron = re.compile(criterio, re.IGNORECASE)
    resultados = patron.findall(contenido)
    
    resultado_text.delete(1.0, tk.END)
    
    if resultados:
        for resultado in resultados:
            resultado_text.insert(tk.END, resultado + '\n')
    else:
        messagebox.showinfo("Resultados", "No se encontraron coincidencias.")

# Función para cambiar la resolución
def configurar_resolucion():
    def aplicar_resolucion():
        seleccion = combo_resolucion.get()
        if seleccion:
            ancho, alto = map(int, seleccion.split("x"))
            root.geometry(f"{ancho}x{alto}")
            messagebox.showinfo("Resolución", f"Resolución cambiada a: {seleccion}")
        ventana_configuracion.destroy()

    ventana_configuracion = tk.Toplevel(root)
    ventana_configuracion.title("Configuración de Resolución")
    ventana_configuracion.geometry("500x300")

    label_resolucion = tk.Label(ventana_configuracion, text="Seleccionar Resolución:")
    label_resolucion.pack(pady=10)

    opciones_resolucion = ["900x600", "1024x768", "1280x720", "1920x1080"]
    combo_resolucion = ttk.Combobox(ventana_configuracion, values=opciones_resolucion, state="readonly")
    combo_resolucion.current(0)
    combo_resolucion.pack(pady=5)

    btn_aplicar = ttk.Button(ventana_configuracion, text="Aplicar", command=aplicar_resolucion)
    btn_aplicar.pack(pady=10)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Visor/Buscador de Logs")
root.geometry("900x600")
root.config(bg="#f0f0f0")

font_header = ("Helvetica", 14, "bold")
font_body = ("Helvetica", 12)

# Frame superior para cargar archivo y realizar búsquedas
frame_superior = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10)
frame_superior.pack(fill="x")

# Botón para cargar archivos de log
btn_cargar = ttk.Button(frame_superior, text="Cargar Logs", command=cargar_archivos)
btn_cargar.grid(row=0, column=0, padx=10, pady=5)

# Dropdown para seleccionar archivo
combo_archivos = ttk.Combobox(frame_superior, state="readonly", width=50)
combo_archivos.bind("<<ComboboxSelected>>", cargar_archivo_seleccionado)
combo_archivos.grid(row=0, column=1, padx=10, pady=5)

# Etiqueta para el campo de búsqueda
label_buscar = tk.Label(frame_superior, text="Buscar en logs:", font=font_body, bg="#e0e0e0")
label_buscar.grid(row=0, column=2, padx=10, pady=5)

# Campo para ingresar el criterio de búsqueda
entry_buscar = ttk.Entry(frame_superior, width=50)
entry_buscar.grid(row=0, column=3, padx=10, pady=5)

# Botón para buscar
btn_buscar = ttk.Button(frame_superior, text="Buscar", command=buscar_logs)
btn_buscar.grid(row=0, column=4, padx=10, pady=5)

# Botón de configuración en la esquina superior derecha
btn_configurar = ttk.Button(frame_superior, text="Configuración", command=configurar_resolucion)
btn_configurar.grid(row=0, column=5, padx=10, pady=5, sticky="e")

# Divisor para separar secciones
ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

# Frame central para mostrar los logs cargados
frame_logs = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame_logs.pack(fill="both", expand=True)

# Etiqueta para el visor de logs
label_logs = tk.Label(frame_logs, text="Logs cargados:", font=font_header, bg="#f0f0f0")
label_logs.pack(anchor="w")

# Área de texto para mostrar los logs cargados
log_text = tk.Text(frame_logs, height=15, width=100, font=font_body, bg="#ffffff", relief="sunken", borderwidth=2)
log_text.pack(fill="both", expand=True, padx=10, pady=5)

# Divisor para separar secciones
ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

# Frame inferior para mostrar los resultados
frame_resultados = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame_resultados.pack(fill="both", expand=True)

# Etiqueta para los resultados de búsqueda
label_resultados = tk.Label(frame_resultados, text="Resultados de búsqueda:", font=font_header, bg="#f0f0f0")
label_resultados.pack(anchor="w")

# Área de texto para mostrar los resultados de la búsqueda
resultado_text = tk.Text(frame_resultados, height=10, width=100, font=font_body, bg="#e8f4f8", relief="sunken", borderwidth=2)
resultado_text.pack(fill="both", expand=True, padx=10, pady=5)

# Ejecutar la ventana
root.mainloop()
