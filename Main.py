import tkinter as tk
from tkinter import ttk, messagebox
from Modelo import Candidata, Jurado, Concurso

class ReinaIndependenciaApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Eleccion Reina de Independencia 2025")
        self.ventana.geometry("700x400")

        self.concurso = Concurso("Reina de Independencia Quetzaltenango 2025")
        self.concurso.cargar_datos()
        
        self.crear_menu()

        tk.Label(
            self.ventana,
            text="Sistema de Gestion - Eleccion Reina de Independencia 2025",
            font=("Arial", 14, "bold"),
            justify="center"
        ).pack(pady=50)

        self.ventana.mainloop()

    def crear_menu(self):
        barra_menu = tk.Menu(self.ventana)
        
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Registrar Candidata", command=self.registrar_candidata)
        menu_opciones.add_command(label="Registrar Jurado", command=self.registrar_jurado)
        menu_opciones.add_command(label="Registrar Calificacion", command=self.registrar_calificacion)
        menu_opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.ventana.quit)
        barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Guardar Datos", command=self.guardar_datos)
        menu_archivo.add_command(label="Cargar Datos", command=self.cargar_datos)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        self.ventana.config(menu=barra_menu)

    def registrar_candidata(self):
        ventana_registro = tk.Toplevel(self.ventana)
        ventana_registro.title("Registrar Nueva Candidata")
        ventana_registro.geometry("400x300")
        ventana_registro.grab_set()

        frame_form = tk.Frame(ventana_registro, padx=10, pady=10)
        frame_form.pack(expand=True, fill="both")

        tk.Label(frame_form, text="Codigo:").grid(row=0, column=0, sticky="w", pady=5)
        entry_codigo = tk.Entry(frame_form, width=40)
        entry_codigo.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Nombre Completo:").grid(row=1, column=0, sticky="w", pady=5)
        entry_nombre = tk.Entry(frame_form, width=40)
        entry_nombre.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Edad:").grid(row=2, column=0, sticky="w", pady=5)
        entry_edad = tk.Entry(frame_form, width=40)
        entry_edad.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Institucion:").grid(row=3, column=0, sticky="w", pady=5)
        entry_institucion = tk.Entry(frame_form, width=40)
        entry_institucion.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Municipio:").grid(row=4, column=0, sticky="w", pady=5)
        entry_municipio = tk.Entry(frame_form, width=40)
        entry_municipio.grid(row=4, column=1, sticky="ew", pady=5)
        
        frame_form.columnconfigure(1, weight=1)

        def guardar():
            codigo = entry_codigo.get()
            nombre = entry_nombre.get()
            edad_str = entry_edad.get()
            institucion = entry_institucion.get()
            municipio = entry_municipio.get()

            if not all([codigo, nombre, edad_str, institucion, municipio]):
                messagebox.showwarning("Datos Incompletos", "Todos los campos son obligatorios.", parent=ventana_registro)
                return
            
            try:
                edad = int(edad_str)
            except ValueError:
                messagebox.showerror("Error de Formato", "La edad debe ser un numero.", parent=ventana_registro)
                return

            nueva_candidata = Candidata(codigo, nombre, edad, institucion, municipio)
            if self.concurso.agregar_candidata(nueva_candidata):
                messagebox.showinfo("Exito", f"Candidata '{nombre}' registrada.", parent=ventana_registro)
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", f"El codigo de candidata '{codigo}' ya esta en uso.", parent=ventana_registro)

        tk.Button(ventana_registro, text="Guardar Candidata", command=guardar).pack(pady=20)

    def registrar_jurado(self):
        ventana_jurado = tk.Toplevel(self.ventana)
        ventana_jurado.title("Registrar Nuevo Jurado")
        ventana_jurado.geometry("400x150")
        ventana_jurado.grab_set()

        frame_form = tk.Frame(ventana_jurado, padx=10, pady=10)
        frame_form.pack(expand=True, fill="both")

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombre = tk.Entry(frame_form, width=40)
        entry_nombre.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Especialidad:").grid(row=1, column=0, sticky="w", pady=5)
        entry_especialidad = tk.Entry(frame_form, width=40)
        entry_especialidad.grid(row=1, column=1, sticky="ew", pady=5)

        frame_form.columnconfigure(1, weight=1)

        def guardar():
            nombre = entry_nombre.get()
            especialidad = entry_especialidad.get()

            if not nombre or not especialidad:
                messagebox.showwarning("Datos Incompletos", "Todos los campos son obligatorios.", parent=ventana_jurado)
                return

            nuevo_jurado = Jurado(nombre, especialidad)
            if self.concurso.agregar_jurado(nuevo_jurado):
                messagebox.showinfo("Exito", f"Jurado '{nombre}' registrado.", parent=ventana_jurado)
                ventana_jurado.destroy()
            else:
                messagebox.showerror("Error", f"El jurado '{nombre}' ya esta registrado.", parent=ventana_jurado)

        tk.Button(ventana_jurado, text="Guardar Jurado", command=guardar).pack(pady=10)

    def registrar_calificacion(self):
        codigos_candidatas = list(self.concurso.candidatas.keys())
        nombres_jurados = list(self.concurso.jurados.keys())

        if not codigos_candidatas or not nombres_jurados:
            messagebox.showinfo("Faltan Datos", "Debe haber al menos una candidata y un jurado registrados.")
            return

        ventana_calificar = tk.Toplevel(self.ventana)
        ventana_calificar.title("Registrar Calificacion")
        ventana_calificar.geometry("400x300")
        ventana_calificar.grab_set()

        frame_form = tk.Frame(ventana_calificar, padx=10, pady=10)
        frame_form.pack(expand=True, fill="both")

        tk.Label(frame_form, text="Candidata:").grid(row=0, column=0, sticky="w", pady=5)
        combo_candidatas = ttk.Combobox(frame_form, values=codigos_candidatas, state="readonly")
        combo_candidatas.grid(row=0, column=1, sticky="ew", pady=5)
        if codigos_candidatas:
            combo_candidatas.current(0)

        tk.Label(frame_form, text="Jurado:").grid(row=1, column=0, sticky="w", pady=5)
        combo_jurados = ttk.Combobox(frame_form, values=nombres_jurados, state="readonly")
        combo_jurados.grid(row=1, column=1, sticky="ew", pady=5)
        if nombres_jurados:
            combo_jurados.current(0)

        tk.Label(frame_form, text="Cultura General:").grid(row=2, column=0, sticky="w", pady=5)
        entry_cultura = tk.Entry(frame_form)
        entry_cultura.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Proyeccion Escenica:").grid(row=3, column=0, sticky="w", pady=5)
        entry_proyeccion = tk.Entry(frame_form)
        entry_proyeccion.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(frame_form, text="Entrevista:").grid(row=4, column=0, sticky="w", pady=5)
        entry_entrevista = tk.Entry(frame_form)
        entry_entrevista.grid(row=4, column=1, sticky="ew", pady=5)

        def guardar():
            codigo_candidata = combo_candidatas.get()
            nombre_jurado = combo_jurados.get()
            cultura_str = entry_cultura.get()
            proyeccion_str = entry_proyeccion.get()
            entrevista_str = entry_entrevista.get()

            if not all([codigo_candidata, nombre_jurado, cultura_str, proyeccion_str, entrevista_str]):
                messagebox.showwarning("Datos Incompletos", "Todos los campos son obligatorios.", parent=ventana_calificar)
                return

            try:
                cultura = float(cultura_str)
                proyeccion = float(proyeccion_str)
                entrevista = float(entrevista_str)

                if not (0 <= cultura <= 10 and 0 <= proyeccion <= 10 and 0 <= entrevista <= 10):
                    messagebox.showerror("Puntaje Invalido", "Las calificaciones deben estar entre 0 y 10.", parent=ventana_calificar)
                    return

            except ValueError:
                messagebox.showerror("Error de Formato", "Las calificaciones deben ser numeros.", parent=ventana_calificar)
                return

            candidata = self.concurso.candidatas.get(codigo_candidata)
            jurado = self.concurso.jurados.get(nombre_jurado)

            if candidata and jurado:
                calificacion = jurado.calificar(cultura, proyeccion, entrevista)
                candidata.agregar_calificacion(calificacion)
                messagebox.showinfo("Exito", f"Calificacion para '{candidata.nombre}' registrada.", parent=ventana_calificar)
                ventana_calificar.destroy()

        tk.Button(ventana_calificar, text="Guardar Calificacion", command=guardar).pack(pady=20)

    def ver_ranking(self):
        lista_ordenada = self.concurso.ranking()

        if not lista_ordenada:
            messagebox.showinfo("Sin Datos", "No hay candidatas para mostrar en el ranking.")
            return

        ventana_ranking = tk.Toplevel(self.ventana)
        ventana_ranking.title("Ranking de Candidatas")
        ventana_ranking.geometry("500x500")
        ventana_ranking.grab_set()

        texto_ranking = tk.Text(ventana_ranking, wrap="word", font=("Courier New", 10))
        texto_ranking.pack(expand=True, fill="both", padx=10, pady=10)

        for i, candidata in enumerate(lista_ordenada):
            lugar = i + 1
            info = f"{lugar}º Lugar: {candidata.nombre} (Codigo: {candidata.codigo})\n"
            info += f"   Puntaje Final: {candidata.get_puntaje_final():.2f}\n"
            info += "-" * 45 + "\n"
            texto_ranking.insert(tk.END, info)

        texto_ranking.config(state="disabled")


    def guardar_datos(self):
        if self.concurso.guardar_datos():
            messagebox.showinfo("Guardado", "Los datos se han guardado con exito.")
        else:
            messagebox.showerror("Error", "No se pudieron guardar los datos.")

    def cargar_datos(self):
        if messagebox.askokcancel("Confirmar Carga", "Esto reemplazara los datos actuales. Deseas continuar?"):
            if self.concurso.cargar_datos():
                messagebox.showinfo("Cargado", "Los datos se han cargado con exito.")
            else:
                messagebox.showerror("Error", "No se pudieron cargar los datos.")

if __name__ == "__main__":
    ReinaIndependenciaApp()