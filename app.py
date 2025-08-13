import customtkinter
import os
import threading
from typing import Optional

from gui_builder import GUIBuilder


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # --- Paleta de Cores Personalizada ---
        self.COLOR_BACKGROUND: str = "#1e1e1e"
        self.COLOR_FRAME: str = "#2d2d30"
        self.COLOR_TEXT: str = "#E3E3E3"
        self.COLOR_PRIMARY_BUTTON: str = "#e74af5"
        self.COLOR_PRIMARY_HOVER: str = "#7c0b80"
        self.COLOR_SECONDARY_BUTTON: str = "#404040"
        self.COLOR_SECONDARY_HOVER: str = "#505050"
        self.COLOR_GRID: str = "#4dff4d"
        self.COLOR_SUCCESS: str = "#4dff4d"
        self.COLOR_ERROR: str = "#ed8484"

        # --- Variáveis de estado ---
        self.imagem_path: str = ""

        # --- Configuração da Janela ---
        self._setup_window()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Criação dos Widgets usando o construtor da GUI ---
        GUIBuilder.build(self)


    def _setup_window(self) -> None:
        """Configura as propriedades da janela principal."""
        self.title("Gerador de Paleta de Cores")
        self.geometry("850x650")
        self.minsize(800, 600)
        self._set_appearance_mode("dark")
        self.configure(fg_color=self.COLOR_BACKGROUND)


if __name__ == "__main__":
    app = App()
    app.mainloop()
