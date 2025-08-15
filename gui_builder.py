import customtkinter as ctk

class GUIBuilder:
    """
    Construtor da interface do usuário.
    Cria todos os widgets e os posiciona na janela principal.
    """
    @staticmethod
    def build(app, controller):
        """Constrói a interface para a aplicação."""
        GUIBuilder._create_control_panel_widgets(app, controller)
        GUIBuilder._create_main_panel_widgets(app, controller)

    @staticmethod
    def _create_control_panel_widgets(app, controller):
        """Cria os widgets do painel de controle esquerdo."""
        app.frame_controles = ctk.CTkFrame(app, fg_color=controller.COLOR_FRAME, width=280)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        label_title = ctk.CTkLabel(app.frame_controles, text="Editor de Sprites", font=ctk.CTkFont(size=20, weight="bold"))
        label_title.pack(pady=(20, 20), padx=20)

        ctk.CTkButton(app.frame_controles, text="Escolher Imagem", height=35, command=controller.handle_choose_image, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(app.frame_controles, text="Escolher Pasta de Saída", height=35, command=controller.handle_choose_folder, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")

        frame_opcoes = ctk.CTkFrame(app.frame_controles, fg_color="transparent")
        frame_opcoes.pack(pady=20, padx=20, fill="x")
        frame_opcoes.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame_opcoes, text="Tamanho do bloco (px):").grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky="w")
        ctk.CTkLabel(frame_opcoes, text="Fator de escala:").grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="w")

        ctk.CTkEntry(frame_opcoes, textvariable=controller.bloco_px_var).grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")

        scale_factor_widget = ctk.CTkComboBox(frame_opcoes, values=["1", "2", "4", "8", "16", "32"], button_color=controller.COLOR_PRIMARY_BUTTON)
        scale_factor_widget.set("4")
        scale_factor_widget.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
        controller.scale_factor_var = scale_factor_widget

        ctk.CTkButton(app.frame_controles, text="Abrir Pasta de Saída", command=controller.handle_open_folder_exit, fg_color="transparent", border_width=1, border_color=controller.COLOR_SECONDARY_HOVER).pack(side="bottom", pady=20, padx=20, fill="x")
        
    @staticmethod
    def _create_main_panel_widgets(app, controller):
        """Cria os widgets do painel principal direito."""
        app.main_frame = ctk.CTkFrame(app, fg_color="transparent")
        app.main_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.main_frame.grid_columnconfigure(0, weight=1)
        app.main_frame.grid_rowconfigure(0, weight=0)
        app.main_frame.grid_rowconfigure(1, weight=0)
        app.main_frame.grid_rowconfigure(2, weight=0)
        app.main_frame.grid_rowconfigure(3, weight=1)

        controller.btn_execute = ctk.CTkButton(app.main_frame, text="✨ Dividir Imagens", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_split_image, fg_color=controller.COLOR_PRIMARY_BUTTON, hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.btn_execute.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="ew")

        ctk.CTkButton(app.main_frame, text="🎨 Criar Paleta de Cores", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_create_palette_button, fg_color=controller.COLOR_PRIMARY_BUTTON2, hover_color=controller.COLOR_PRIMARY_HOVER).grid(row=1, column=0, padx=0, pady=(2), sticky="ew")

        ctk.CTkButton(app.main_frame, text="↪️ Converter formato", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=lambda: controller.handle_create_palette_button(), fg_color=controller.COLOR_PRIMARY_BUTTON2, hover_color=controller.COLOR_PRIMARY_HOVER).grid(row=2, column=0, padx=0, pady=(2), sticky="ew")

        controller.tabview = ctk.CTkTabview(app.main_frame, fg_color=controller.COLOR_FRAME, segmented_button_selected_color=controller.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.tabview.grid(row=3, column=0, columnspan=2, sticky="nsew")
        controller.tabview.add("Log de Atividades")
        controller.tabview.add("Preview com Grid")
        controller.tabview.add("Gerador de Paleta de Cores")

        controller.preview_label = ctk.CTkLabel(controller.tabview.tab("Preview com Grid"), text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.preview_label.pack(padx=0, pady=0, expand=True, fill="both")

        controller.log_textbox = ctk.CTkTextbox(controller.tabview.tab("Log de Atividades"), text_color=controller.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        controller.log_textbox.pack(padx=0, pady=0, expand=True, fill="both")

        palette_tab_frame = ctk.CTkFrame(controller.tabview.tab("Gerador de Paleta de Cores"), fg_color="transparent")
        palette_tab_frame.pack(padx=20, pady=2, expand=True, fill="both")
        palette_tab_frame.grid_rowconfigure(0, weight=0)
        palette_tab_frame.grid_rowconfigure(1, weight=1)
        palette_tab_frame.grid_columnconfigure(0, weight=1)

        controller.palette_preview_label = ctk.CTkLabel(palette_tab_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.palette_preview_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(2))

        controller.palette_frame = ctk.CTkFrame(palette_tab_frame, fg_color="transparent")
        controller.palette_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=2)
        controller.palette_frame.grid_columnconfigure(0, weight=1)
        controller.palette_frame.grid_rowconfigure(0, weight=1)

        controller.status_label = ctk.CTkLabel(app.main_frame, text="", text_color=controller.COLOR_SUCCESS)
        controller.status_label.grid(row=4, column=0, columnspan=1, padx=5, pady=(10, 0), sticky="sw")
        controller.progressbar = ctk.CTkProgressBar(app.main_frame, fg_color=controller.COLOR_FRAME, progress_color=controller.COLOR_PRIMARY_BUTTON)
        controller.progressbar.set(0)