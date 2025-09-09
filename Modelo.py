class Calificacion:
    def __init__(self, cultura, proyeccion, entrevista):
        self.cultura = float(cultura)
        self.proyeccion = float(proyeccion)
        self.entrevista = float(entrevista)

    def promedio(self):
        return (self.cultura + self.proyeccion + self.entrevista) / 3

class Candidata:
    def __init__(self, codigo, nombre, edad, institucion, municipio):
        self.codigo = codigo
        self.nombre = nombre
        self.edad = edad
        self.institucion = institucion
        self.municipio = municipio
        self.calificaciones = []
        self.puntaje_final = 0.0

    def agregar_calificacion(self, calificacion):
        self.calificaciones.append(calificacion)
        self.calcular_puntaje_final()

    def calcular_puntaje_final(self):
        if not self.calificaciones:
            self.puntaje_final = 0.0
            return

        total = 0
        for calif in self.calificaciones:
            total = total + calif.promedio()

        self.puntaje_final = total / len(self.calificaciones)

    def get_puntaje_final(self):
        return self.puntaje_final

class Jurado:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad

    def calificar(self, cultura, proyeccion, entrevista):
        return Calificacion(cultura, proyeccion, entrevista)

class Concurso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.candidatas = {}
        self.jurados = {}

    def agregar_candidata(self, candidata):
        if candidata.codigo in self.candidatas:
            return False
        self.candidatas[candidata.codigo] = candidata
        return True

    def agregar_jurado(self, jurado):
        if jurado.nombre in self.jurados:
            return False
        self.jurados[jurado.nombre] = jurado
        return True

    def ranking(self):
        lista_ordenada = sorted(self.candidatas.values(), key=lambda c: c.get_puntaje_final(), reverse=True)
        return lista_ordenada

    def guardar_datos(self):
        try:
            with open("candidatas.txt", "w") as f:
                for c in self.candidatas.values():
                    linea = f"{c.codigo}|{c.nombre}|{c.edad}|{c.institucion}|{c.municipio}\n"
                    f.write(linea)

            with open("jurados.txt", "w") as f:
                for j in self.jurados.values():
                    linea = f"{j.nombre}|{j.especialidad}\n"
                    f.write(linea)

            with open("calificaciones.txt", "w") as f:
                for c in self.candidatas.values():
                    for calif in c.calificaciones:
                        linea = f"{c.codigo}|{calif.cultura}|{calif.proyeccion}|{calif.entrevista}\n"
                        f.write(linea)
            return True
        except:
            return False

    def cargar_datos(self):
        try:
            try:
                with open("candidatas.txt", "r") as f:
                    self.candidatas.clear()
                    for linea in f:
                        partes = linea.strip().split("|")
                        if len(partes) == 5:
                            c = Candidata(partes[0], partes[1], int(partes[2]), partes[3], partes[4])
                            self.agregar_candidata(c)
            except FileNotFoundError:
                pass

            try:
                with open("jurados.txt", "r") as f:
                    self.jurados.clear()
                    for linea in f:
                        partes = linea.strip().split("|")
                        if len(partes) == 2:
                            j = Jurado(partes[0], partes[1])
                            self.agregar_jurado(j)
            except FileNotFoundError:
                pass

            try:
                with open("calificaciones.txt", "r") as f:
                    for linea in f:
                        partes = linea.strip().split("|")
                        if len(partes) == 4:
                            codigo_candidata, cultura, proyeccion, entrevista = partes
                            candidata = self.candidatas.get(codigo_candidata)
                            if candidata:
                                calif = Calificacion(cultura, proyeccion, entrevista)
                                candidata.agregar_calificacion(calif)
            except FileNotFoundError:
                pass

            return True
        except:
            return False