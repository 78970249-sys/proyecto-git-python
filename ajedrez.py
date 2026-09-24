import tkinter as tk
from tkinter import messagebox
import chess


class JuegoAjedrez:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("♟ Juego de Ajedrez en Python")
        self.ventana.geometry("760x850")
        self.ventana.resizable(False, False)

        self.tablero = chess.Board()
        self.casilla_seleccionada = None

        self.colores = {
            "claro": "#F0D9B5",
            "oscuro": "#B58863",
            "seleccion": "#F6F669"
        }

        self.piezas = {
            "P": "♙",
            "N": "♘",
            "B": "♗",
            "R": "♖",
            "Q": "♕",
            "K": "♔",
            "p": "♟",
            "n": "♞",
            "b": "♝",
            "r": "♜",
            "q": "♛",
            "k": "♚"
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="♟ JUEGO DE AJEDREZ ♟",
            font=("Arial", 26, "bold")
        )
        titulo.pack(pady=15)

        self.lbl_turno = tk.Label(
            self.ventana,
            text="Turno: Blancas",
            font=("Arial", 16, "bold")
        )
        self.lbl_turno.pack(pady=5)

        self.lbl_estado = tk.Label(
            self.ventana,
            text="Selecciona una pieza para comenzar",
            font=("Arial", 12)
        )
        self.lbl_estado.pack(pady=5)

        self.frame_tablero = tk.Frame(self.ventana)
        self.frame_tablero.pack(pady=15)

        self.botones = {}

        for fila in range(8):
            for columna in range(8):
                boton = tk.Button(
                    self.frame_tablero,
                    font=("Arial", 30),
                    width=2,
                    height=1,
                    command=lambda f=fila, c=columna:
                    self.seleccionar_casilla(f, c)
                )

                boton.grid(
                    row=fila,
                    column=columna,
                    ipadx=7,
                    ipady=7
                )

                self.botones[(fila, columna)] = boton

        frame_controles = tk.Frame(self.ventana)
        frame_controles.pack(pady=10)

        tk.Button(
            frame_controles,
            text="🔄 NUEVA PARTIDA",
            font=("Arial", 13, "bold"),
            width=18,
            command=self.nueva_partida
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_controles,
            text="🏳 RENDIRSE",
            font=("Arial", 13, "bold"),
            width=18,
            command=self.rendirse
        ).grid(row=0, column=1, padx=10)

        self.actualizar_tablero()

    def obtener_square(self, fila, columna):
        """
        Convierte las coordenadas de la interfaz
        a una casilla de python-chess.
        """

        fila_chess = 7 - fila

        return chess.square(
            columna,
            fila_chess
        )

    def actualizar_tablero(self):
        for fila in range(8):
            for columna in range(8):

                square = self.obtener_square(
                    fila,
                    columna
                )

                pieza = self.tablero.piece_at(square)

                boton = self.botones[(fila, columna)]

                color = (
                    self.colores["claro"]
                    if (fila + columna) % 2 == 0
                    else self.colores["oscuro"]
                )

                boton.config(
                    bg=color,
                    activebackground=color
                )

                if pieza:
                    simbolo = self.piezas[
                        pieza.symbol()
                    ]

                    boton.config(text=simbolo)

                else:
                    boton.config(text="")

        if self.casilla_seleccionada is not None:

            fila, columna = self.casilla_seleccionada

            self.botones[
                (fila, columna)
            ].config(
                bg=self.colores["seleccion"]
            )

        turno = (
            "Blancas"
            if self.tablero.turn == chess.WHITE
            else "Negras"
        )

        self.lbl_turno.config(
            text=f"Turno: {turno}"
        )

        self.verificar_estado()

    def seleccionar_casilla(self, fila, columna):

        square = self.obtener_square(
            fila,
            columna
        )

        pieza = self.tablero.piece_at(square)

        # Primer clic
        if self.casilla_seleccionada is None:

            if pieza is None:
                self.lbl_estado.config(
                    text="Selecciona una pieza."
                )
                return

            if pieza.color != self.tablero.turn:
                self.lbl_estado.config(
                    text="Esa pieza no corresponde al turno actual."
                )
                return

            self.casilla_seleccionada = (
                fila,
                columna
            )

            self.lbl_estado.config(
                text="Ahora selecciona la casilla de destino."
            )

            self.actualizar_tablero()
            return

        # Segundo clic
        fila_origen, columna_origen = (
            self.casilla_seleccionada
        )

        origen = self.obtener_square(
            fila_origen,
            columna_origen
        )

        destino = square

        movimiento = chess.Move(
            origen,
            destino
        )

        # Promoción automática a reina
        pieza_origen = self.tablero.piece_at(
            origen
        )

        if (
            pieza_origen
            and pieza_origen.piece_type
            == chess.PAWN
        ):
            rank_destino = chess.square_rank(
                destino
            )

            if rank_destino in (0, 7):
                movimiento = chess.Move(
                    origen,
                    destino,
                    promotion=chess.QUEEN
                )

        if movimiento in self.tablero.legal_moves:

            self.tablero.push(movimiento)

            self.lbl_estado.config(
                text="Movimiento realizado correctamente."
            )

        else:

            self.lbl_estado.config(
                text="Movimiento no permitido."
            )

        self.casilla_seleccionada = None

        self.actualizar_tablero()

    def verificar_estado(self):

        if self.tablero.is_checkmate():

            ganador = (
                "Negras"
                if self.tablero.turn
                == chess.WHITE
                else "Blancas"
            )

            messagebox.showinfo(
                "Jaque Mate",
                f"♚ JAQUE MATE ♚\n\n"
                f"Ganaron las {ganador}."
            )

            self.lbl_estado.config(
                text=f"Jaque mate. Ganaron las {ganador}."
            )

            return

        if self.tablero.is_stalemate():

            messagebox.showinfo(
                "Empate",
                "La partida terminó en tablas."
            )

            self.lbl_estado.config(
                text="Partida terminada en tablas."
            )

            return

        if self.tablero.is_insufficient_material():

            messagebox.showinfo(
                "Empate",
                "Empate por material insuficiente."
            )

            return

        if self.tablero.is_check():

            self.lbl_estado.config(
                text="⚠ ¡JAQUE!"
            )

    def nueva_partida(self):

        respuesta = messagebox.askyesno(
            "Nueva partida",
            "¿Deseas iniciar una nueva partida?"
        )

        if respuesta:

            self.tablero.reset()

            self.casilla_seleccionada = None

            self.lbl_estado.config(
                text="Nueva partida iniciada."
            )

            self.actualizar_tablero()

    def rendirse(self):

        ganador = (
            "Negras"
            if self.tablero.turn == chess.WHITE
            else "Blancas"
        )

        messagebox.showinfo(
            "Fin de la partida",
            f"El jugador se rindió.\n\n"
            f"Ganaron las {ganador}."
        )

        self.nueva_partida()


# ==============================
# EJECUCIÓN
# ==============================

ventana = tk.Tk()

juego = JuegoAjedrez(ventana)

ventana.mainloop()