import tkinter as tk
from tkinter import messagebox
import random


class JuegoPenales:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("⚽ Juego de Fútbol - Tanda de Penales")
        self.ventana.geometry("850x650")
        self.ventana.resizable(False, False)

        # Variables del juego
        self.goles_jugador = 0
        self.goles_cpu = 0
        self.ronda = 1
        self.turno = "jugador"
        self.nombre = "Jugador"

        self.crear_inicio()

    def limpiar(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    # -----------------------------
    # PANTALLA DE INICIO
    # -----------------------------
    def crear_inicio(self):
        self.limpiar()

        titulo = tk.Label(
            self.ventana,
            text="⚽ JUEGO DE FÚTBOL ⚽",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=50)

        subtitulo = tk.Label(
            self.ventana,
            text="TANDA DE PENALES",
            font=("Arial", 20, "bold")
        )
        subtitulo.pack(pady=10)

        tk.Label(
            self.ventana,
            text="Ingrese su nombre:",
            font=("Arial", 14)
        ).pack(pady=20)

        self.entrada_nombre = tk.Entry(
            self.ventana,
            font=("Arial", 16),
            justify="center",
            width=25
        )
        self.entrada_nombre.pack()

        boton = tk.Button(
            self.ventana,
            text="INICIAR PARTIDO",
            font=("Arial", 16, "bold"),
            width=20,
            height=2,
            command=self.iniciar
        )
        boton.pack(pady=40)

        tk.Label(
            self.ventana,
            text="Python + Tkinter",
            font=("Arial", 10)
        ).pack(side="bottom", pady=20)

    # -----------------------------
    # INICIAR JUEGO
    # -----------------------------
    def iniciar(self):
        nombre = self.entrada_nombre.get().strip()

        if nombre:
            self.nombre = nombre

        self.goles_jugador = 0
        self.goles_cpu = 0
        self.ronda = 1
        self.turno = "jugador"

        self.crear_juego()

    # -----------------------------
    # PANTALLA PRINCIPAL
    # -----------------------------
    def crear_juego(self):
        self.limpiar()

        titulo = tk.Label(
            self.ventana,
            text="⚽ TANDA DE PENALES",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=15)

        # Marcador
        self.lbl_marcador = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 18, "bold")
        )
        self.lbl_marcador.pack()

        self.lbl_ronda = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 14)
        )
        self.lbl_ronda.pack(pady=5)

        # Cancha
        self.canvas = tk.Canvas(
            self.ventana,
            width=650,
            height=300,
            bg="#3b9b45"
        )
        self.canvas.pack(pady=15)

        # Arco
        self.canvas.create_rectangle(
            175, 40, 475, 180,
            outline="white",
            width=5
        )

        # Línea horizontal
        self.canvas.create_line(
            175, 180, 475, 180,
            fill="white",
            width=4
        )

        # Arquero
        self.arquero = self.canvas.create_oval(
            305, 100, 345, 150,
            fill="blue"
        )

        # Pelota
        self.pelota = self.canvas.create_oval(
            310, 230, 340, 260,
            fill="white",
            outline="black",
            width=2
        )

        self.lbl_mensaje = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 16, "bold")
        )
        self.lbl_mensaje.pack(pady=10)

        # Botones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="⬅ IZQUIERDA",
            font=("Arial", 12, "bold"),
            width=15,
            command=lambda: self.jugar("izquierda")
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_botones,
            text="⬆ CENTRO",
            font=("Arial", 12, "bold"),
            width=15,
            command=lambda: self.jugar("centro")
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            frame_botones,
            text="DERECHA ➡",
            font=("Arial", 12, "bold"),
            width=15,
            command=lambda: self.jugar("derecha")
        ).grid(row=0, column=2, padx=10)

        self.actualizar()

    # -----------------------------
    # ACTUALIZAR INFORMACIÓN
    # -----------------------------
    def actualizar(self):
        self.lbl_marcador.config(
            text=f"{self.nombre}  {self.goles_jugador}  -  "
                 f"{self.goles_cpu}  CPU"
        )

        self.lbl_ronda.config(
            text=f"Ronda: {self.ronda}"
        )

        if self.turno == "jugador":
            self.lbl_mensaje.config(
                text="Tu turno: selecciona dónde patear"
            )
        else:
            self.lbl_mensaje.config(
                text="Tu turno de arquero: selecciona dónde lanzarte"
            )

    # -----------------------------
    # JUGADA
    # -----------------------------
    def jugar(self, direccion_jugador):

        if self.turno == "jugador":
            direccion_cpu = random.choice(
                ["izquierda", "centro", "derecha"]
            )

            self.animar(
                direccion_jugador,
                direccion_cpu
            )

            if direccion_jugador == direccion_cpu:
                resultado = "¡ATAJÓ EL ARQUERO!"
            else:
                resultado = "⚽ ¡GOOOOOOL!"
                self.goles_jugador += 1

            self.lbl_mensaje.config(
                text=resultado
            )

            self.turno = "cpu"

            self.ventana.after(
                1300,
                self.actualizar
            )

        else:
            tiro_cpu = random.choice(
                ["izquierda", "centro", "derecha"]
            )

            self.animar(
                tiro_cpu,
                direccion_jugador
            )

            if tiro_cpu == direccion_jugador:
                resultado = "🧤 ¡ATAJASTE EL PENAL!"
            else:
                resultado = "⚽ ¡GOL DE LA CPU!"
                self.goles_cpu += 1

            self.lbl_mensaje.config(
                text=resultado
            )

            self.turno = "jugador"

            self.ronda += 1

            if self.ronda > 5:
                self.ventana.after(
                    1500,
                    self.verificar_final
                )
            else:
                self.ventana.after(
                    1300,
                    self.actualizar
                )

        self.lbl_marcador.config(
            text=f"{self.nombre}  {self.goles_jugador}  -  "
                 f"{self.goles_cpu}  CPU"
        )

    # -----------------------------
    # ANIMACIÓN
    # -----------------------------
    def animar(self, tiro, arquero):
        posiciones = {
            "izquierda": 210,
            "centro": 310,
            "derecha": 410
        }

        # Pelota
        x = posiciones[tiro]

        self.canvas.coords(
            self.pelota,
            x,
            110,
            x + 30,
            140
        )

        # Arquero
        x_arq = posiciones[arquero]

        self.canvas.coords(
            self.arquero,
            x_arq,
            100,
            x_arq + 40,
            150
        )

        self.ventana.after(
            1000,
            self.resetear_cancha
        )

    def resetear_cancha(self):

        self.canvas.coords(
            self.pelota,
            310,
            230,
            340,
            260
        )

        self.canvas.coords(
            self.arquero,
            305,
            100,
            345,
            150
        )

    # -----------------------------
    # RESULTADO FINAL
    # -----------------------------
    def verificar_final(self):

        if self.goles_jugador > self.goles_cpu:

            mensaje = (
                f"🏆 ¡FELICITACIONES {self.nombre}!\n\n"
                f"Ganaste {self.goles_jugador} - "
                f"{self.goles_cpu}"
            )

        elif self.goles_cpu > self.goles_jugador:

            mensaje = (
                f"😢 La CPU ganó\n\n"
                f"Resultado: {self.goles_jugador} - "
                f"{self.goles_cpu}"
            )

        else:

            mensaje = (
                "🤝 EMPATE\n\n"
                f"Resultado: {self.goles_jugador} - "
                f"{self.goles_cpu}"
            )

        messagebox.showinfo(
            "Resultado Final",
            mensaje
        )

        self.crear_inicio()


# -----------------------------
# EJECUCIÓN DEL PROGRAMA
# -----------------------------
ventana = tk.Tk()

juego = JuegoPenales(ventana)

ventana.mainloop()