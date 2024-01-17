
"""
Este programa es un simulador de movimiento de proyectiles que utiliza una interfaz gráfica (GUI) implementada con la biblioteca Tkinter.
Permite al usuario ingresar información sobre varios proyectiles, como la velocidad inicial, el ángulo de lanzamiento y la gravedad, y simula sus trayectorias.
El resultado se muestra gráficamente y se presenta en forma de texto en la interfaz.
A su vez los datos se guardan en un json.
"""
#Importamos las librerias necesarias para cálculos, para poder representar las gráficas y para poder hacer la interfaz.
import math
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import tkinter as tk
import json

class Projectile:
    def __init__(self, initial_velocity, launch_angle, gravity):
        self.initial_velocity = initial_velocity
        self.launch_angle = math.radians(launch_angle)
        self.gravity = gravity

class ProjectileSimulatorGUI:# Constructor de la clase. Se ejecuta al crear una instancia de la clase.
    def __init__(self, root):
        self.root = root# Almacena la referencia al objeto Tk (la ventana principal)
        self.root.title("Projectile Motion Simulator")# Establece el título de la ventana.
        self.unit_system_var = StringVar() # Variables de control para almacenar valores introducidos por el usuario.
        self.num_projectiles_var = StringVar()
        self.results_text_var = StringVar()
        self.create_widgets()# Método para crear los widgets en la interfaz.

    def create_widgets(self):# Método para crear y colocar los widgets en la interfaz.
        # Etiqueta y cuadro de entrada para el sistema de unidades (SI o US). y el resto son botones para la interfaz
        Label(self.root, text="Choose unit system (SI or US):").grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.unit_system_var).grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Enter the number of projectiles:").grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.num_projectiles_var).grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Simulate", command=self.simulate_projectiles).grid(row=2, column=0, columnspan=2, pady=20)

        Label(self.root, text="Results:").grid(row=3, column=0, columnspan=2, pady=10)
        Label(self.root, textvariable=self.results_text_var).grid(row=4, column=0, columnspan=2, pady=10)

    def simulate_projectiles(self):
        unit_system = self.unit_system_var.get().upper()
        num_projectiles = int(self.num_projectiles_var.get())

        projectiles = []
        results_list = []
        all_results = []  # List para guardar los dato de los proyectiles 
# Bucle para solicitar información sobre cada proyectil y realizar la simulación.

        for i in range(num_projectiles):
            # Solicitar información al usuario para cada proyectil.
            try:
                initial_velocity = float(input(f"Enter initial velocity ({get_velocity_unit(unit_system)}): "))
                launch_angle = float(input("Enter launch angle in degrees: "))
                gravity = float(input(f"Enter gravitational acceleration ({get_gravity_unit(unit_system)}): "))
                # Crear un objeto Projectile con la información proporcionada y agregarlo a la lista de proyectiles.
                projectiles.append(Projectile(initial_velocity, launch_angle, gravity))
            except ValueError:
                # Manejar errores si el usuario ingresa valores no numéricos.
                messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
                return
# Bucle para iterar sobre cada proyectil, realizar la simulación y recopilar resultados.
        for i, projectile in enumerate(projectiles, start=1):
            x_points, y_points, time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)
# Graficar la trayectoria en el gráfico.
            plt.plot(x_points, y_points, label=f"Projectile {i}")

            results_text = (
                f"Projectile {i} - Time of Flight: {time_of_flight} {get_time_unit(unit_system)}, "
                f"Max Height: {max_height} {get_length_unit(unit_system)}, Range: {range_val} {get_length_unit(unit_system)}"
            )

            results_list.append(results_text)

            # Agregar los resultados a la lista 'all_results'.
            all_results.append({
                "Projectile": i,
                "Time of Flight": time_of_flight,
                "Max Height": max_height,
                "Range": range_val
            })

        # Guardalos en un json
        with open("projectile_results.json", "w") as json_file:
            json.dump(all_results, json_file, indent=2)

        self.results_text_var.set("\n".join(results_list))

        plt.title("Projectile Motion")
        plt.xlabel(f"Horizontal Distance ({get_length_unit(unit_system)})")
        plt.ylabel(f"Vertical Distance ({get_length_unit(unit_system)})")
        plt.legend()

        plt.show()

        self.show_additional_info(projectiles, unit_system)
# Método para calcular la trayectoria de un proyectil dado.
    def calculate_trajectory(self, projectile):
        # Calcular el tiempo de vuelo, altura máxima y alcance horizontal del proyectil.
        time_of_flight = (2 * projectile.initial_velocity * math.sin(projectile.launch_angle)) / projectile.gravity
        max_height = (projectile.initial_velocity**2 * (math.sin(projectile.launch_angle))**2) / (2 * projectile.gravity)
        range_val = (projectile.initial_velocity**2 * math.sin(2 * projectile.launch_angle)) / projectile.gravity
# Crear puntos de tiempo para la simulación.
        time_points = [i * 0.1 for i in range(int(time_of_flight * 10) + 1)]
        # Calcular las coordenadas x e y en función del tiempo.
        x_points = [projectile.initial_velocity * math.cos(projectile.launch_angle) * t for t in time_points]
        y_points = [
            projectile.initial_velocity * math.sin(projectile.launch_angle) * t - 0.5 * projectile.gravity * t**2
            for t in time_points
        ]

        return x_points, y_points, time_of_flight, max_height, range_val
# Método para mostrar información adicional sobre cada proyectil en una nueva ventana.
    def show_additional_info(self, projectiles, unit_system):
        info_window = tk.Toplevel(self.root)
        info_window.title("Projectile Information")
# Iterar sobre cada proyectil y mostrar información detallada.
        for i, projectile in enumerate(projectiles, start=1):
            time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)[2:]

            info_label = Label(info_window, text=(
                f"Projectile {i} Information:\n"
                f"Time of Flight: {time_of_flight} {get_time_unit(unit_system)}\n"
                f"Max Height: {max_height} {get_length_unit(unit_system)}\n"
                f"Range: {range_val} {get_length_unit(unit_system)}"
            ))
            info_label.pack(pady=10)
# Funciones auxiliares para obtener unidades según el sistema seleccionado.
def get_velocity_unit(unit_system):
    return "m/s" if unit_system == "SI" else "ft/s"

def get_gravity_unit(unit_system):
    return "m/s^2" if unit_system == "SI" else "ft/s^2"

def get_time_unit(unit_system):
    return "s" if unit_system == "SI" else "s"

def get_length_unit(unit_system):
    return "m" if unit_system == "SI" else "ft"
# Punto de entrada principal del programa.
if __name__ == "__main__":
    root = Tk()
    app = ProjectileSimulatorGUI(root)
    root.mainloop()
