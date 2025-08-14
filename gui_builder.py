import customtkinter as ctk
from PIL import Image


class GUIBuilder:
    """
    Construtor da interface do usuário.
    Cria todos os widgets e os posiciona na janela principal.
    """
    @staticmethod
    def build(app):
        """Constrói a interface para a aplicação """
        GUIBuilder._create_control_panel_widgets(app)
        GUIBuilder._create_main_panel_widgets(app)


    @staticmethod
    def _create_control_panel_widgets(app):
        """Cria os widgets do painel de controle esquerdo."""
        app.frame_controles = ctk.CTkFrame(app, fg_color=app.COLOR_FRAME, width=280)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        app.icon = None
        label_title = ctk.CTkLabel(app.frame_controles, text="Editor de Sprites", font=ctk.CTkFont(size=20, weight="bold"))
        label_title.pack(pady=(20, 20), padx=20)

        ctk.CTkButton(app.frame_controles, text="Escolher Imagem", height=35, command=app._handle_choose_image, fg_color=app.COLOR_SECONDARY_BUTTON, hover_color=app.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(app.frame_controles, text="Escolher Pasta de Saída", height=35, command=app._handle_choose_folder, fg_color=app.COLOR_SECONDARY_BUTTON, hover_color=app.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")

        frame_opcoes = ctk.CTkFrame(app.frame_controles, fg_color="transparent")
        frame_opcoes.pack(pady=20, padx=20, fill="x")
        frame_opcoes.grid_columnconfigure((0, 1), weight=1)

        block_label = ctk.CTkLabel(frame_opcoes, text="Tamanho do bloco (px):")
        block_label.grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky="w")

        label_scale = ctk.CTkLabel(frame_opcoes, text="Fator de escala:")
        label_scale.grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="w")

        app.entry_block_size = ctk.CTkEntry(frame_opcoes, textvariable=app.bloco_px_var)
        app.entry_block_size.grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")

        app.scale_factor_ = ctk.CTkComboBox(frame_opcoes, values=["1", "2", "4", "8", "16", "32"], button_color=app.COLOR_PRIMARY_BUTTON)
        app.scale_factor_.set("4")
        app.scale_factor_.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")

        ctk.CTkButton(app.frame_controles, text="Abrir Pasta de Saída", command=app._handle_open_folder_exit, fg_color="transparent", border_width=1, border_color=app.COLOR_SECONDARY_HOVER).pack(side="bottom", pady=20, padx=20, fill="x")

    @staticmethod
    def _create_main_panel_widgets(app):
        """Cria os widgets do painel principal direito."""
        app.main_frame = ctk.CTkFrame(app, fg_color="transparent")
        app.main_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.main_frame.grid_columnconfigure(0, weight=1)
        app.main_frame.grid_rowconfigure(2, weight=1)
        
        # Os botões agora estão um abaixo do outro.
        app.btn_execute = ctk.CTkButton(app.main_frame, text="✨ Dividir Imagens", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=app._handle_split_image, fg_color=app.COLOR_PRIMARY_BUTTON, hover_color=app.COLOR_PRIMARY_HOVER)
        app.btn_execute.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="ew")

        ctk.CTkButton(app.main_frame, text="🎨 Criar Paleta de Cores", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=app._handle_create_palette_button, fg_color=app.COLOR_PRIMARY_BUTTON2, hover_color=app.COLOR_PRIMARY_HOVER).grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")
        
        # Cria a tabview antes de adicionar as abas
        app.tabview = ctk.CTkTabview(app.main_frame, fg_color=app.COLOR_FRAME, segmented_button_selected_color=app.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=app.COLOR_PRIMARY_HOVER)
        app.tabview.grid(row=2, column=0, columnspan=2, sticky="nsew")
        app.tabview.add("Log de Atividades")
        app.tabview.add("Preview com Grid")
        app.tabview.add("Gerador de Paleta de Cores")

        # Aba de Preview com Grid
        app.preview_label = ctk.CTkLabel(app.tabview.tab("Preview com Grid"), text="Selecione uma imagem para ver o preview", text_color=app.COLOR_TEXT)
        app.preview_label.pack(padx=20, pady=20, expand=True, fill="both")

        # Aba de Log de Atividades
        app.log_textbox = ctk.CTkTextbox(app.tabview.tab("Log de Atividades"), text_color=app.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        app.log_textbox.pack(padx=20, pady=20, expand=True, fill="both")

        # Aba de Gerador de Paleta de Cores
        palette_tab_frame = ctk.CTkFrame(app.tabview.tab("Gerador de Paleta de Cores"), fg_color="transparent")
        palette_tab_frame.pack(padx=20, pady=20, expand=True, fill="both")
        palette_tab_frame.grid_rowconfigure(0, weight=0)  # Preview
        palette_tab_frame.grid_rowconfigure(1, weight=1)  # Lista de cores
        palette_tab_frame.grid_columnconfigure(0, weight=1)

        # Preview da imagem na aba de paleta
        app.palette_preview_label = ctk.CTkLabel(palette_tab_frame, text="Preview da imagem", text_color=app.COLOR_TEXT)
        app.palette_preview_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(0, 10))

        # Frame para a paleta de cores
        app.palette_frame = ctk.CTkFrame(palette_tab_frame, fg_color="transparent")
        app.palette_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        app.palette_frame.grid_columnconfigure(0, weight=1)

        
        app.status_label = ctk.CTkLabel(app.main_frame, text="", text_color=app.COLOR_SUCCESS)
        app.status_label.grid(row=3, column=0, columnspan=1, padx=5, pady=(10, 0), sticky="sw")
        app.progressbar = ctk.CTkProgressBar(app.main_frame, fg_color=app.COLOR_FRAME, progress_color=app.COLOR_PRIMARY_BUTTON)
        app.progressbar.set(0)
