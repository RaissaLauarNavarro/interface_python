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
        GUIBuilder._create_tab_view_widgets(app, controller)

    @staticmethod
    def _create_control_panel_widgets(app, controller):
        """Cria os widgets do painel de controle esquerdo, que são comuns a todas as abas."""
        app.frame_controles = ctk.CTkFrame(app, fg_color=controller.COLOR_FRAME, width=280)
        app.frame_controles.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        label_title = ctk.CTkLabel(app.frame_controles, text="Editor de Sprites", font=ctk.CTkFont(size=20, weight="bold"))
        label_title.pack(pady=(20, 20), padx=20)

        ctk.CTkButton(app.frame_controles, text="Escolher Imagem", height=35, command=controller.handle_choose_image, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(app.frame_controles, text="Escolher Pasta de Saída", height=35, command=controller.handle_choose_folder, fg_color=controller.COLOR_SECONDARY_BUTTON, hover_color=controller.COLOR_SECONDARY_HOVER).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(app.frame_controles, text="Abrir Pasta de Saída", command=controller.handle_open_folder_exit, fg_color="transparent", border_width=1, border_color=controller.COLOR_SECONDARY_HOVER).pack(side="bottom", pady=20, padx=20, fill="x")
    
    @staticmethod
    def _create_tab_view_widgets(app, controller):
        """Cria as abas e os widgets específicos para cada funcionalidade."""
        app.main_frame = ctk.CTkFrame(app, fg_color="transparent")
        app.main_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        app.main_frame.grid_columnconfigure(0, weight=1)
        app.main_frame.grid_rowconfigure(0, weight=1)

        # Cria a tabview antes de adicionar as abas
        controller.tabview = ctk.CTkTabview(app.main_frame, fg_color=controller.COLOR_FRAME, segmented_button_selected_color=controller.COLOR_PRIMARY_BUTTON, segmented_button_selected_hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.tabview.grid(row=0, column=0, sticky="nsew")
        
        # Adiciona e configura cada aba
        tab_split = controller.tabview.add("Divisor de Sprites")
        tab_palette = controller.tabview.add("Gerador de Paleta de Cores")
        tab_convert = controller.tabview.add("Conversor de Formato")
        tab_log = controller.tabview.add("Log de Atividades")
        
        # Widgets para a aba "Divisor de Sprites"
        GUIBuilder._create_split_tab_widgets(tab_split, controller)

        # Widgets para a aba "Gerador de Paleta"
        GUIBuilder._create_palette_tab_widgets(tab_palette, controller)

        # Widgets para a aba "Conversor de Formato"
        GUIBuilder._create_convert_tab_widgets(tab_convert, controller)

        # Widgets para a aba "Log de Atividades"
        GUIBuilder._create_log_tab_widgets(tab_log, controller)

        # Cria a barra de status e progresso na parte inferior do main_frame
        controller.progressbar = ctk.CTkProgressBar(app.main_frame, fg_color=controller.COLOR_FRAME, progress_color=controller.COLOR_PRIMARY_BUTTON)
        controller.progressbar.set(0)
        controller.progressbar.grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=5)
        
        controller.status_label = ctk.CTkLabel(app.main_frame, text="", text_color=controller.COLOR_SUCCESS)
        controller.status_label.grid(row=2, column=0, sticky="sw", padx=5)
        
        # Oculta a barra de progresso e a label de status inicialmente
        controller.progressbar.grid_remove()
        controller.status_label.grid_remove()

    @staticmethod
    def _create_split_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Divisor de Sprites."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Frame de preview com grid
        preview_frame = ctk.CTkFrame(tab, fg_color="transparent")
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        controller.preview_label = ctk.CTkLabel(preview_frame, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.preview_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Frame para os controles da aba
        controls_frame = ctk.CTkFrame(tab, fg_color="transparent")
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        controls_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(controls_frame, text="Tamanho do bloco (px):").grid(row=0, column=0, padx=(0, 5), pady=(0, 0), sticky="w")
        ctk.CTkLabel(controls_frame, text="Fator de escala:").grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="w")

        ctk.CTkEntry(controls_frame, textvariable=controller.bloco_px_var).grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")

        scale_factor_widget = ctk.CTkComboBox(controls_frame, values=["1", "2", "4", "8", "16", "32"], button_color=controller.COLOR_PRIMARY_BUTTON)
        scale_factor_widget.set(controller.scale_factor_var.get())
        scale_factor_widget.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
        # Conecta a variável do controller ao widget
        controller.scale_factor_var = scale_factor_widget
        
        controller.btn_execute = ctk.CTkButton(controls_frame, text="✨ Dividir Imagens", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_split_image, fg_color=controller.COLOR_PRIMARY_BUTTON, hover_color=controller.COLOR_PRIMARY_HOVER)
        controller.btn_execute.grid(row=2, column=0, columnspan=2, padx=0, pady=10, sticky="ew")

    @staticmethod
    def _create_palette_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Gerador de Paleta."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=0) # Preview
        tab.grid_rowconfigure(1, weight=1) # Paleta
        
        controller.palette_preview_label = ctk.CTkLabel(tab, text="Selecione uma imagem para ver o preview", text_color=controller.COLOR_TEXT)
        controller.palette_preview_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 5))
        
        controller.palette_frame = ctk.CTkFrame(tab, fg_color="transparent")
        controller.palette_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        controller.palette_frame.grid_columnconfigure(0, weight=1)
        controller.palette_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkButton(tab, text="🎨 Criar Paleta de Cores", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=controller.handle_create_palette_button, fg_color=controller.COLOR_PRIMARY_BUTTON2, hover_color=controller.COLOR_PRIMARY_HOVER).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
    @staticmethod
    def _create_convert_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Conversor de Formato."""
        # TODO: Adicionar widgets para a funcionalidade de conversão de formato.
        ctk.CTkLabel(tab, text="Funcionalidade de Conversor de Formato em breve!", font=ctk.CTkFont(size=16)).pack(padx=20, pady=20, expand=True)

    @staticmethod
    def _create_log_tab_widgets(tab, controller):
        """Cria e posiciona os widgets dentro da aba Log de Atividades."""
        controller.log_textbox = ctk.CTkTextbox(tab, text_color=controller.COLOR_TEXT, fg_color="transparent", activate_scrollbars=True)
        controller.log_textbox.pack(padx=0, pady=0, expand=True, fill="both")