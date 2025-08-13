import customtkinter as ctk
from PIL import Image


class GUIBuilder:
    @staticmethod
    def build(app):
        """Constrói a interface para a aplicação """
        GUIBuilder._create_control_panel_widgets(app)
        GUIBuilder._create_main_panel_widgets(app)


    @staticmethod
    def _create_control_panel_widgets(app):
        app.frame_controles = ctk.CTkFrame(app, fg_color=app.COLOR_FRAME, width=280)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        app.icon = None
        label_titulo = ctk.CTkLabel(app.frame_controles, text="Gerador de Paleta de Cores", font=ctk.CTkFont(size=20, weight="bold"))
        label_titulo.pack(pady=(20, 20), padx=20)


    @staticmethod
    def _create_main_panel_widgets(app):
        app.frame_principal = ctk.CTkFrame(app, fg_color=app.COLOR_FRAME)
        app.frame_principal.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.frame_principal.grid_columnconfigure(0, weight=1)
        app.frame_principal.grid_rowconfigure(0, weight=1)

