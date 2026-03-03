from datetime import datetime
from itertools import count

class Libro:
    def __init__(self, isbn, titulo, autor, ejemplares_totales):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.ejemplares_totales = ejemplares_totales
        self.ejemplares_disponibles = ejemplares_totales
        self.veces_prestado = 0


class Usuario:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre


class Biblioteca:
    def __init__(self):
        self.catalogo = {}  #key es isbn, devuelve libro
        self.usuarios = {}    #la key del diccionario es id_usuario, value devuelve el objeto
        self.prestamos = [] #lista que contiene tuplas dentro


    def registrar_libro(self, isbn, titulo, autor, ejemplares):
        if isbn in self.catalogo:
            print("El ISBN:{} ya existe en el sistem".format(isbn))
            return
        self.catalogo[isbn] = Libro(isbn, titulo, autor, ejemplares)
        print("El Libro ha sido registrado")

    def buscar_libro(self, texto):
        resultados = []
        for libro in self.catalogo.values():
            if texto.lower() in libro.titulo.lower() or texto.lower() in libro.autor.lower():
                resultados.append(libro)
        return resultados



    def registrar_usuario(self, id_usuario, nombre):
        if id_usuario in self.usuarios:
            print("Usuario ya existe.")
            return
        self.usuarios[id_usuario] = Usuario(id_usuario, nombre)
        print("Usuario registrado.")

    def prestar_libro(self, isbn, id_usuario):
        if isbn not in self.catalogo:
            print("Libro no existe.")
            return

        if id_usuario not in self.usuarios:
            print("Usuario no existe.")
            return

        libro = self.catalogo[isbn]

        
        if libro.ejemplares_disponibles <= 0:
            print("No hay ejemplares disponibles.")
            return

        
        for p in self.prestamos:
            if p[0] == isbn and p[1] == id_usuario:
                print(" El usuario ya tiene este libro.")
                return

        
        prestamos_usuario = [p for p in self.prestamos if p[1] == id_usuario]
        if len(prestamos_usuario) >= 3:
            print("El usuario alcanzó límite de 3 préstamos.")
            return

        fecha = datetime.now().strftime("%Y-%m-%d")
        self.prestamos.append((isbn, id_usuario, fecha))  # tupla
        libro.ejemplares_disponibles -= 1
        libro.veces_prestado += 1

        print("Préstamo registrado.")

    def devolver_libro(self, isbn, id_usuario):
        for prestamo in self.prestamos:
            if prestamo[0] == isbn and prestamo[1] == id_usuario:
                self.prestamos.remove(prestamo)
                self.catalogo[isbn].ejemplares_disponibles += 1
                print("El libro ha sido devuelto.")
                return
        print("No se encontró préstamo activo.")


    def top_3_libros(self):
        ordenados = sorted(
            self.catalogo.values(),
            key=lambda l: l.veces_prestado,
            reverse=True
        )
        print("\n TOP 3 LIBROS MÁS PRESTADOS")
        for libro in ordenados[:3]:
            print(f"{libro.titulo} - {libro.veces_prestado} préstamos")

    def listar_prestamos(self):
        print("\n PRÉSTAMOS ACTIVOS")
        for p in self.prestamos:
            print(f"ISBN: {p[0]} | Usuario: {p[1]} | Fecha: {p[2]}")

    def buscar_por_isbn(self, isbn):
        if isbn in self.catalogo:
            libro = self.catalogo[isbn]
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Disponibles: {libro.ejemplares_disponibles}")
        else:
            print("Libro no encontrado.")



def mostrar_menu():
    print("\n ***** Sistema de gestión para la Bilioteca *****\n")

    print("1. Registrar libro")
    print("2. Registrar usuario")
    print("3. Prestar un libro")
    print("4. Devolver un libro")
    print("5. Buscar un libro")
    print("6. Top 3 libros")
    print("7. Ver préstamos activos")
    print("8. Libros por ISBN")
    print("0. Salir")




biblioteca = Biblioteca()

while True:
    mostrar_menu()
    opcion = input("Seleccione opción: ")

    if opcion == "1":
        isbn = input("ISBN: ")
        titulo = input("Título: ")
        autor = input("Autor: ")
        ejemplares = int(input("Ejemplares: "))
        biblioteca.registrar_libro(isbn, titulo, autor, ejemplares)

    elif opcion == "2":
        id_usuario = input("ID Usuario: ")
        nombre = input("Nombre: ")
        biblioteca.registrar_usuario(id_usuario, nombre)

    elif opcion == "3":
        isbn = input("ISBN: ")
        id_usuario = input("ID Usuario: ")
        biblioteca.prestar_libro(isbn, id_usuario)

    elif opcion == "4":
        isbn = input("ISBN: ")
        id_usuario = input("ID Usuario: ")
        biblioteca.devolver_libro(isbn, id_usuario)

    elif opcion == "5":
        texto = input("Buscar por título o autor: ")
        resultados = biblioteca.buscar_libro(texto)
        for libro in resultados:
            print(f"{libro.titulo} - Disponibles: {libro.ejemplares_disponibles}")

    elif opcion == "6":
        biblioteca.top_3_libros()

    elif opcion == "7":
        biblioteca.listar_prestamos()

    elif opcion == "8":
        isbn = input("ISBN: ")
        biblioteca.buscar_por_isbn(isbn)

    elif opcion == "0":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida.")