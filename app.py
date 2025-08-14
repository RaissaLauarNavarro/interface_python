import customtkinter as ctk
import os
import threading
from typing import Optional
from PIL import Image, ImageOps

# Importa as classes e funções dos outros arquivos
from gui_builder import GUIBuilder
from image_processor import process_and_save_blocks
from utils import update_log, open_output_folder, select_image_path, select_output_folder
from color_palette_generator import get_color_palette, rgb_to_hex

# --- Classe principal da Aplicação ---
class App(ctk.CTk):
    """
    Aplicativo principal "Editor de Sprites".
    Gerencia a janela, o estado e a interação entre a GUI e a lógica de processamento.
    """
    def __init__(self) -> None:
        super().__init__()

        # --- Paleta de Cores Personalizada ---
        self.COLOR_BACKGROUND: str = "#1e1e1e"
        self.COLOR_FRAME: str = "#2d2d30"
        self.COLOR_TEXT: str = "#E3E3E3"
        self.COLOR_PRIMARY_BUTTON: str = "#b43dbe"
        self.COLOR_PRIMARY_BUTTON2: str ="#8c2795"
        self.COLOR_PRIMARY_HOVER: str = "#7c0b80"
        self.COLOR_SECONDARY_BUTTON: str = "#404040"
        self.COLOR_SECONDARY_HOVER: str = "#505050"
        self.COLOR_GRID: str = "#4dff4d"
        self.COLOR_SUCCESS: str = "#4dff4d"
        self.COLOR_ERROR: str = "#ed8484"

        # --- Variáveis de estado ---
        self.image_path: str = ""
        self.end_folder: str = ""
        self._after_id: Optional[str] = None
        self.ctk_img_preview: Optional[ctk.CTkImage] = None
        self.palette_colors: list = []

        # Variáveis de controle para os widgets (referências)
        self.bloco_px_var = ctk.StringVar(value="16")
        self.scale_factor_ = None
        self.btn_execute = None
        self.progressbar = None
        self.preview_label = None
        self.log_textbox = None
        self.tabview = None
        self.status_label = None
        self.palette_frame = None
        
        # --- Configuração da Janela Principal ---
        self._setup_window()
        
        # --- Configuração do Layout da Janela ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Criação dos Widgets usando o construtor da GUI ---
        GUIBuilder.build(self)
        self.bloco_px_var.trace_add("write", self._agendar_atualizacao_preview)
        
        update_log(self.log_textbox, "Bem-vindo ao Editor de Sprites!", self.status_label)


    def _setup_window(self) -> None:
        """Configura as propriedades da janela principal."""
        self.title("Editor de Sprites")
        self.geometry("1100x650")
        self.minsize(800, 600)
        self._set_appearance_mode("dark")
        self.configure(fg_color=self.COLOR_BACKGROUND)
    
    
    def _safe_configure_preview(self, image: Optional[ctk.CTkImage] = None, text: str = "") -> None:
        """Configura o label de preview de forma segura."""
        try:
            if image is None:
                self.ctk_img_preview = None
                self.preview_label.configure(image="", text=text)
            else:
                self.preview_label.configure(image=image, text="")
        except Exception:
            pass
            
            
    def _load_image_path(self, path: str) -> None:
        if path:
            if self.palette_frame:
                for widget in self.palette_frame.winfo_children():
                    widget.destroy()

            self.image_path = path
            update_log(self.log_textbox, f"Imagem selecionada: {os.path.basename(self.image_path)}", self.status_label)
        
            # Seleciona a aba "Preview com Grid" e atualiza o preview
            self._agendar_atualizacao_preview()
            self._update_palette_preview(path)


    def _handle_choose_image(self) -> None:
        """Abre a caixa de diálogo para selecionar uma imagem e atualiza o estado."""
        path = select_image_path()
        self._load_image_path(path)


    def _handle_choose_folder(self) -> None:
        """Abre a caixa de diálogo para selecionar a pasta de saída e atualiza o estado."""
        folder = select_output_folder()
        if folder:
            self.end_folder = folder
            update_log(self.log_textbox, "Pasta de saída definida.", self.status_label)


    def _handle_open_folder_exit(self) -> None:
        """Tenta abrir a pasta de saída no explorador de arquivos do sistema."""
        open_output_folder(self.end_folder, self.log_textbox, self.status_label)
    

    def _agendar_atualizacao_preview(self, *args) -> None:
        """Agenda a atualização do preview para evitar múltiplas chamadas rápidas."""
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        
        try:
            self._after_id = self.after(500, self._update_grid_preview)
        except Exception:
            self._after_id = None


    def _update_grid_preview(self) -> None:
        """Gera e exibe a imagem de preview com o grid."""
        self._after_id = None
        if not self.image_path: return
        
        from PIL import Image, ImageDraw
        try:
            self.update_idletasks()
            bloco_px = int(self.bloco_px_var.get())
            if bloco_px <= 0:
                self._safe_configure_preview(text="Digite um tamanho de bloco válido.")
                return

            original_image = Image.open(self.image_path).convert("RGBA")
            orig_w, orig_h = original_image.size
            preview_box_w = self.preview_label.winfo_width() - 40
            preview_box_h = self.preview_label.winfo_height() - 40
            if preview_box_w <= 1 or preview_box_h <= 1:
                self._after_id = self.after(200, self._update_grid_preview)
                return

            scale = min(preview_box_w / orig_w, preview_box_h / orig_h)
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)
            
            draw = ImageDraw.Draw(preview_image)
            scale_w, scale_h = new_w / orig_w, new_h / orig_h
            for x in range(bloco_px, orig_w, bloco_px):
                draw.line([(x * scale_w, 0), (x * scale_w, new_h)], fill=self.COLOR_GRID, width=1)
            for y in range(bloco_px, orig_h, bloco_px):
                draw.line([(0, y * scale_h), (new_w, y * scale_h)], fill=self.COLOR_GRID, width=1)

            self.ctk_img_preview = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self._safe_configure_preview(self.ctk_img_preview)
        except Exception as e:
            self._safe_configure_preview(text=f"Erro no preview:\n{e}")


    def _update_palette_preview(self, path: str) -> None:
        """Atualiza apenas o preview da imagem na aba de paleta de cores."""
        try:
            original_image = Image.open(path).convert("RGBA")
            preview_box_w = self.palette_preview_label.winfo_width() - 20
            preview_box_h = 250  # altura fixa para não ocupar toda a aba

            if preview_box_w <= 0:
                preview_box_w = 300  # valor padrão se ainda não renderizou

            scale = min(preview_box_w / original_image.width, preview_box_h / original_image.height)
            new_w = max(1, int(original_image.width * scale))
            new_h = max(1, int(original_image.height * scale))
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)

            self.ctk_palette_preview = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self.palette_preview_label.configure(image=self.ctk_palette_preview, text="")
        except Exception as e:
            self.palette_preview_label.configure(text=f"Erro ao carregar preview: {e}")
            

    def _handle_split_image(self) -> None:
        """Inicia o processo de divisão da imagem."""
        if not self.image_path or not self.end_folder:
            update_log(self.log_textbox, "Erro: Selecione a imagem e a pasta de saída.", self.status_label)
            return

        try:
            bloco_px = int(self.bloco_px_var.get())
            scale = int(self.scale_factor_.get())
            if bloco_px <= 0 or scale <= 0:
                raise ValueError("Tamanho do bloco e escala devem ser maiores que zero.")
        except (ValueError, TypeError):
            update_log(self.log_textbox, "Erro: Tamanho do bloco ou fator de escala inválido.", self.status_label)
            return
        
        self._start_threaded_processing(bloco_px, scale)


    def _start_threaded_processing(self, bloco_px: int, scale: int) -> None:
        """Configura e executa o processamento da imagem em uma thread separada."""
        self.btn_execute.configure(state="disabled")
        self.progressbar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.progressbar.set(0)
        update_log(self.log_textbox, "Iniciando processamento...", self.status_label)
        if self.status_label:
            self.status_label.configure(text="Iniciando processamento...", text_color=self.COLOR_TEXT)

        processing_thread = threading.Thread(
            target=self. _thread_processing,
            args=(self.image_path, self.end_folder, bloco_px, scale)
        )
        processing_thread.start()


    def _thread_processing(self, image_path: str, output_folder: str, bloco_px: int, scale: int) -> None:
        """Função que será executada na thread de processamento."""
        try:
            process_and_save_blocks(
                image_path,
                output_folder,
                bloco_px,
                scale,
                lambda progress: self.after(0, self._update_progress, progress)
            )
            self.after(0, update_log, self.log_textbox, "✨ Processamento concluído!", self.status_label)
        except Exception as e:
            self.after(0, update_log, self.log_textbox, f"ERRO: {e}", self.status_label)
        finally:
            self.after(0, self. _end_processing)
    

    def _update_progress(self, progress: float) -> None:
        """Atualiza a barra de progresso na GUI (chamado da thread principal)."""
        self.progressbar.set(progress)
    

    def _end_processing(self) -> None:
        """Reseta a interface após o processamento."""
        self.progressbar.grid_remove()
        self.btn_execute.configure(state="normal")
    

    def _handle_create_palette_button(self) -> None:
        """
        Lida com o clique do botão de criar paleta.
        Usa a imagem já selecionada ou mostra um erro.
        """
        if self.image_path and os.path.exists(self.image_path):
            self.tabview.set("Gerador de Paleta de Cores")
            self._handle_create_palette(self.image_path)
        else:
            update_log(self.log_textbox, "Erro: Selecione uma imagem primeiro para criar a paleta.", self.status_label)


    def _handle_create_palette(self, path: str) -> None:
        update_log(self.log_textbox, f"Criando paleta de cores para: {os.path.basename(path)}", self.status_label)

        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        try:
            original_image = Image.open(path).convert("RGBA")
            preview_box_w = self.palette_preview_label.winfo_width() - 20
            preview_box_h = 250  # altura fixa para não ocupar toda a aba

            if preview_box_w <= 0:
                preview_box_w = 300  # valor padrão se ainda não renderizou

            scale = min(preview_box_w / original_image.width, preview_box_h / original_image.height)
            new_w = max(1, int(original_image.width * scale))
            new_h = max(1, int(original_image.height * scale))
            preview_image = original_image.resize((new_w, new_h), Image.Resampling.NEAREST)

            self.ctk_palette_preview = ctk.CTkImage(light_image=preview_image, size=preview_image.size)
            self.palette_preview_label.configure(image=self.ctk_palette_preview, text="")
        except Exception as e:
            self.palette_preview_label.configure(text=f"Erro ao carregar preview: {e}")

        try:
            self.palette_colors = get_color_palette(path)
            max_cols = 8  # Número de colunas fixo, pode ajustar conforme necessário
            button_height = 40  # Altura fixa para todos os botões
            num_rows = (len(self.palette_colors) + max_cols - 1) // max_cols

            for idx, color in enumerate(self.palette_colors):
                row = idx // max_cols
                col = idx % max_cols
                color_button = ctk.CTkButton(
                    self.palette_frame, text=color, fg_color=color,
                    text_color="black" if self._is_light_color(color) else "white",
                    hover_color=color, command=lambda c=color: self._copy_to_clipboard(c),
                    height=button_height
                )
                color_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            # Configura as colunas para expandirem
            for col in range(max_cols):
                self.palette_frame.grid_columnconfigure(col, weight=1)
            # Configura as linhas para expandirem igualmente
            for row in range(num_rows):
                self.palette_frame.grid_rowconfigure(row, weight=1)
        except Exception as e:
            self.palette_colors = []
            update_log(self.log_textbox, f"ERRO ao criar paleta de cores: {e}", self.status_label)

        update_log(self.log_textbox, "Paleta de cores criada com sucesso! Clique em uma cor para copiar.", self.status_label)


    def _is_light_color(self, hex_color: str) -> bool:
        """
        Verifica se a cor é clara para definir a cor do texto.
        """
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
      
        luminosity = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return luminosity > 0.5
        

    def _copy_to_clipboard(self, text: str) -> None:
        """
        Copia o texto para a área de transferência.
        """
        self.clipboard_clear()
        self.clipboard_append(text)
        update_log(self.log_textbox, f"'{text}' copiado para a área de transferência.", self.status_label)


if __name__ == "__main__":
    app = App()
    app.mainloop()
