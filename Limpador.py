
from pathlib import Path
from datetime import datetime, timedelta
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from send2trash import send2trash


# =========================================================
# CONFIGURAÇÕES
# =========================================================

CATEGORIAS = {
    "Documentos": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt",
        ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".ods", ".odp"
    },
    "Imagens": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
        ".svg", ".tif", ".tiff", ".ico"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".m4v"
    },
    "Audios": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"
    },
    "Compactados": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    },
    "Instaladores": {
        ".exe", ".msi", ".msix", ".appx"
    },
    "Codigo": {
        ".py", ".js", ".html", ".css", ".java", ".c", ".cpp",
        ".json", ".xml", ".sql", ".php", ".ts", ".jsx", ".tsx"
    }
}


# =========================================================
# APLICAÇÃO
# =========================================================

class LimpadorDownloads:

    def __init__(self, root):
        self.root = root
        self.root.title("Limpador de Downloads")
        self.root.geometry("1100x720")
        self.root.minsize(850, 580)

        self.pasta_downloads = Path.home() / "Downloads"

        self.cor_fundo = "#F4F7FB"
        self.cor_painel = "#FFFFFF"
        self.cor_primaria = "#2878E8"
        self.cor_texto = "#20334D"
        self.cor_secundaria = "#64748B"

        self.configurar_estilos()
        self.criar_layout()
        self.mostrar_inicio()

    # -----------------------------------------------------
    # ESTILOS E LAYOUT
    # -----------------------------------------------------

    def configurar_estilos(self):
        self.root.configure(bg=self.cor_fundo)

        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Treeview",
            background="white",
            foreground=self.cor_texto,
            fieldbackground="white",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#EAF1FA",
            foreground=self.cor_texto,
            padding=8
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#D9E9FF")],
            foreground=[("selected", self.cor_texto)]
        )

    def criar_layout(self):
        self.sidebar = tk.Frame(
            self.root,
            bg="#EAF1FA",
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="📁 Limpador",
            font=("Segoe UI", 18, "bold"),
            bg="#EAF1FA",
            fg=self.cor_texto
        ).pack(padx=15, pady=(25, 5), anchor="w")

        tk.Label(
            self.sidebar,
            text="DE DOWNLOADS",
            font=("Segoe UI", 9),
            bg="#EAF1FA",
            fg=self.cor_secundaria
        ).pack(padx=18, pady=(0, 25), anchor="w")

        botoes = [
            ("⌂   Início", self.mostrar_inicio),
            ("▤   Listar arquivos", self.mostrar_arquivos),
            ("▣   Organizar arquivos", self.mostrar_organizacao),
            ("⌕   Buscar extensão", self.mostrar_busca),
            ("◷   Analisar espaço", self.mostrar_espaco),
            ("♲   Limpar antigos", self.mostrar_limpeza),
            ("⚙   Configurações", self.mostrar_configuracoes),
        ]

        for texto, comando in botoes:
            tk.Button(
                self.sidebar,
                text=texto,
                command=comando,
                anchor="w",
                padx=18,
                pady=12,
                font=("Segoe UI", 10),
                bg="#EAF1FA",
                fg=self.cor_texto,
                activebackground="#D6E7FF",
                activeforeground=self.cor_texto,
                relief="flat",
                bd=0,
                cursor="hand2"
            ).pack(fill="x", padx=8, pady=2)

        self.status_pasta = tk.Label(
            self.sidebar,
            text="",
            wraplength=185,
            justify="left",
            font=("Segoe UI", 9),
            bg="#EAF1FA",
            fg=self.cor_secundaria
        )
        self.status_pasta.pack(
            side="bottom", padx=15, pady=20, anchor="w"
        )

        # Área principal que conterá o conteúdo
        self.area_principal = tk.Frame(
        self.root,
        bg=self.cor_fundo
        )
        self.area_principal.pack(
            side="left", fill="both", expand=True
        )

        # Canvas que permite rolagem
        self.canvas = tk.Canvas(
            self.area_principal,
            bg=self.cor_fundo,
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical
        self.barra_rolagem = ttk.Scrollbar(
            self.area_principal,
            orient="vertical",
            command=self.canvas.yview
        )
        self.barra_rolagem.pack(side="right", fill="y")

        self.canvas.configure(
            yscrollcommand=self.barra_rolagem.set
        )

        # Frame onde as telas serão criadas
        self.conteudo = tk.Frame(
            self.canvas,
            bg=self.cor_fundo
        )

        self.janela_conteudo = self.canvas.create_window(
            (0, 0),
            window=self.conteudo,
            anchor="nw"
        )

        # Atualiza a região rolável quando o conteúdo mudar
        self.conteudo.bind(
            "<Configure>",
            self._atualizar_area_rolagem
        )

        # Faz o conteúdo acompanhar a largura da janela
        self.canvas.bind(
            "<Configure>",
            self._ajustar_largura_conteudo
        )

        # Rolagem pela roda do mouse
        self.canvas.bind_all(
            "<MouseWheel>",
            self._rolar_com_mouse
        )

        self.atualizar_status()

    def _atualizar_area_rolagem(self, evento=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _ajustar_largura_conteudo(self, evento):
        self.canvas.itemconfigure(
            self.janela_conteudo,
            width=evento.width
        )

    def _rolar_com_mouse(self, evento):
        x = (
            self.root.winfo_pointerx()
            - self.canvas.winfo_rootx()
        )
        y = (
            self.root.winfo_pointery()
            - self.canvas.winfo_rooty()
        )

        if (
            0 <= x < self.canvas.winfo_width()
            and 0 <= y < self.canvas.winfo_height()
        ):
            self.canvas.yview_scroll(
                int(-evento.delta / 120),
                "units"
            )

    def limpar_tela(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def criar_cabecalho(self, titulo, descricao):
        tk.Label(
            self.conteudo,
            text=titulo,
            font=("Segoe UI", 23, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(anchor="w", padx=30, pady=(25, 4))

        tk.Label(
            self.conteudo,
            text=descricao,
            font=("Segoe UI", 10),
            bg=self.cor_fundo,
            fg=self.cor_secundaria
        ).pack(anchor="w", padx=32, pady=(0, 20))

    def criar_botao(self, parent, texto, comando, principal=False):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=9,
            bg=self.cor_primaria if principal else "#E5EDF8",
            fg="white" if principal else self.cor_texto,
            activebackground="#1766CC",
            activeforeground="white" if principal else self.cor_texto,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    def atualizar_status(self):
        self.status_pasta.config(
            text=f"Pasta atual:\n{self.pasta_downloads}"
        )

    # -----------------------------------------------------
    # FUNÇÕES DE ARQUIVOS
    # -----------------------------------------------------

    def listar_arquivos(self, recursivo=False):
        try:
            if not self.pasta_downloads.is_dir():
                return []

            itens = (
                self.pasta_downloads.rglob("*")
                if recursivo
                else self.pasta_downloads.iterdir()
            )

            return sorted(
                [
                    item for item in itens
                    if item.is_file()
                ],
                key=lambda item: item.name.lower()
            )

        except OSError as erro:
            messagebox.showerror(
                "Erro ao acessar a pasta",
                str(erro)
            )
            return []

    def identificar_categoria(self, arquivo):
        extensao = arquivo.suffix.lower()

        for categoria, extensoes in CATEGORIAS.items():
            if extensao in extensoes:
                return categoria

        return "Outros"

    def formatar_tamanho(self, tamanho):
        unidades = ["B", "KB", "MB", "GB", "TB"]
        valor = float(tamanho)

        for unidade in unidades:
            if valor < 1024 or unidade == "TB":
                return f"{valor:.2f} {unidade}"
            valor /= 1024

        return f"{valor:.2f} TB"

    
    def criar_tabela(self, parent, colunas):
        nomes_colunas = tuple(colunas.keys())

        tabela = ttk.Treeview(
            parent,
            columns=nomes_colunas,
            show="headings"
        )

        for coluna, largura in colunas.items():
            tabela.heading(coluna, text=coluna)
            tabela.column(
                coluna,
                width=largura,
                minwidth=80,
                anchor="w"
            )

        barra = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=tabela.yview
        )

        tabela.configure(yscrollcommand=barra.set)

        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        return tabela


    def escolher_destino_unico(self, pasta, nome):
        destino = pasta / nome

        if not destino.exists():
            return destino

        nome_base = Path(nome).stem
        extensao = Path(nome).suffix
        contador = 1

        while True:
            novo_nome = f"{nome_base} ({contador}){extensao}"
            destino = pasta / novo_nome

            if not destino.exists():
                return destino

            contador += 1

    # -----------------------------------------------------
    # INÍCIO
    # -----------------------------------------------------

    def mostrar_inicio(self):
        self.limpar_tela()

        self.criar_cabecalho(
            "Limpador de Downloads",
            "Organize e gerencie seus arquivos em um só lugar."
        )

        arquivos = self.listar_arquivos()
        total_bytes = 0

        for arquivo in arquivos:
            try:
                total_bytes += arquivo.stat().st_size
            except OSError:
                pass

        resumo = tk.Frame(
            self.conteudo,
            bg=self.cor_painel,
            highlightbackground="#DCE6F3",
            highlightthickness=1
        )
        resumo.pack(fill="x", padx=30, pady=5)

        tk.Label(
            resumo,
            text="Resumo da pasta Downloads",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(18, 12))

        tk.Label(
            resumo,
            text=f"Arquivos na raiz: {len(arquivos)}",
            font=("Segoe UI", 12),
            bg="white",
            fg=self.cor_texto
        ).pack(anchor="w", padx=20, pady=4)

        tk.Label(
            resumo,
            text=f"Espaço ocupado: {self.formatar_tamanho(total_bytes)}",
            font=("Segoe UI", 12),
            bg="white",
            fg=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(4, 20))

        tk.Label(
            self.conteudo,
            text="O que deseja fazer?",
            font=("Segoe UI", 15, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(anchor="w", padx=30, pady=(25, 12))

        acoes = [
            ("Listar arquivos", "Consultar os arquivos da pasta.",
             self.mostrar_arquivos),
            ("Organizar arquivos", "Separar arquivos por categoria.",
             self.mostrar_organizacao),
            ("Buscar por extensão", "Encontrar um tipo de arquivo.",
             self.mostrar_busca),
            ("Analisar espaço", "Consultar espaço por categoria.",
             self.mostrar_espaco),
            ("Limpar arquivos antigos", "Revisar arquivos com mais de 7 dias.",
             self.mostrar_limpeza),
            ("Configurações", "Selecionar outra pasta.",
             self.mostrar_configuracoes),
        ]

        grade = tk.Frame(self.conteudo, bg=self.cor_fundo)
        grade.pack(fill="both", expand=True, padx=24, pady=5)

        for indice, (titulo, descricao, comando) in enumerate(acoes):
            linha, coluna = divmod(indice, 2)

            cartao = tk.Frame(
                grade,
                bg="white",
                highlightbackground="#DCE6F3",
                highlightthickness=1
            )
            cartao.grid(
                row=linha, column=coluna,
                padx=6, pady=6, sticky="nsew"
            )

            tk.Label(
                cartao,
                text=titulo,
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg=self.cor_texto
            ).pack(anchor="w", padx=15, pady=(14, 5))

            tk.Label(
                cartao,
                text=descricao,
                font=("Segoe UI", 9),
                bg="white",
                fg=self.cor_secundaria,
                wraplength=260,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 10))

            self.criar_botao(
                cartao, "Acessar", comando, principal=True
            ).pack(anchor="w", padx=15, pady=(0, 14))

        grade.columnconfigure(0, weight=1)
        grade.columnconfigure(1, weight=1)
        grade.rowconfigure(0, weight=1)
        grade.rowconfigure(1, weight=1)
        grade.rowconfigure(2, weight=1)

    # -----------------------------------------------------
    # LISTAR ARQUIVOS
    # -----------------------------------------------------

    def mostrar_arquivos(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Listar arquivos",
            "Arquivos que estão diretamente na pasta selecionada."
        )

        barra = tk.Frame(self.conteudo, bg=self.cor_fundo)
        barra.pack(fill="x", padx=30, pady=(0, 12))

        self.criar_botao(
            barra, "Atualizar lista", self.mostrar_arquivos
        ).pack(side="left")

        area = tk.Frame(self.conteudo, bg=self.cor_fundo)
        area.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        tabela = self.criar_tabela(
            area,
            {
                "Nome": 280,
                "Categoria": 130,
                "Tamanho": 100,
                "Modificado em": 160
            }
        )

        arquivos = self.listar_arquivos()

        for arquivo in arquivos:
            try:
                info = arquivo.stat()
                modificado = datetime.fromtimestamp(
                    info.st_mtime
                ).strftime("%d/%m/%Y %H:%M")

                tabela.insert(
                    "",
                    "end",
                    values=(
                        arquivo.name,
                        self.identificar_categoria(arquivo),
                        self.formatar_tamanho(info.st_size),
                        modificado
                    )
                )
            except OSError:
                continue

        tk.Label(
            self.conteudo,
            text=f"{len(arquivos)} arquivo(s) encontrado(s)",
            bg=self.cor_fundo,
            fg=self.cor_secundaria
        ).pack(anchor="w", padx=32, pady=(0, 10))

    # -----------------------------------------------------
    # ORGANIZAR ARQUIVOS
    # -----------------------------------------------------

    def mostrar_organizacao(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Organizar arquivos",
            "Confira a prévia antes de mover os arquivos para suas categorias."
        )

        arquivos = self.listar_arquivos()

        area = tk.Frame(self.conteudo, bg=self.cor_fundo)
        area.pack(fill="both", expand=True, padx=30, pady=5)

        tabela = self.criar_tabela(
            area,
            {"Arquivo": 300, "Destino": 200}
        )

        for arquivo in arquivos:
            categoria = self.identificar_categoria(arquivo)
            tabela.insert(
                "", "end",
                values=(arquivo.name, categoria)
            )

        def executar():
            atuais = self.listar_arquivos()

            if not atuais:
                messagebox.showinfo(
                    "Organização",
                    "Não há arquivos para organizar."
                )
                return

            if not messagebox.askyesno(
                "Confirmar organização",
                f"Organizar {len(atuais)} arquivo(s)?\n\n"
                "Os arquivos serão movidos para subpastas. "
                "Nada será excluído."
            ):
                return

            movidos = 0
            falhas = 0

            for arquivo in atuais:
                try:
                    categoria = self.identificar_categoria(arquivo)
                    destino_pasta = self.pasta_downloads / categoria
                    destino_pasta.mkdir(
                        parents=True, exist_ok=True
                    )

                    destino = self.escolher_destino_unico(
                        destino_pasta, arquivo.name
                    )

                    shutil.move(str(arquivo), str(destino))
                    movidos += 1

                except (OSError, shutil.Error) as erro:
                    falhas += 1
                    print(f"Erro ao mover {arquivo}: {erro}")

            messagebox.showinfo(
                "Organização concluída",
                f"Arquivos movidos: {movidos}\n"
                f"Falhas: {falhas}"
            )

            self.mostrar_organizacao()

        botoes = tk.Frame(self.conteudo, bg=self.cor_fundo)
        botoes.pack(fill="x", padx=30, pady=15)

        self.criar_botao(
            botoes, "Organizar agora", executar, principal=True
        ).pack(side="left")

        self.criar_botao(
            botoes, "Atualizar prévia", self.mostrar_organizacao
        ).pack(side="left", padx=10)

    # -----------------------------------------------------
    # BUSCAR POR EXTENSÃO
    # -----------------------------------------------------

    def mostrar_busca(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Buscar por extensão",
            "Pesquise arquivos pelo formato, incluindo subpastas."
        )

        controles = tk.Frame(self.conteudo, bg=self.cor_fundo)
        controles.pack(fill="x", padx=30, pady=5)

        tk.Label(
            controles,
            text="Extensão:",
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(side="left", padx=(0, 8))

        entrada = ttk.Entry(controles, width=20)
        entrada.pack(side="left")
        entrada.insert(0, ".pdf")

        area = tk.Frame(self.conteudo, bg=self.cor_fundo)
        area.pack(fill="both", expand=True, padx=30, pady=15)

        tabela = self.criar_tabela(
            area,
            {"Arquivo": 260, "Pasta": 330, "Tamanho": 100}
        )

        resultado = tk.Label(
            self.conteudo,
            text="Digite uma extensão e clique em Buscar.",
            bg=self.cor_fundo,
            fg=self.cor_secundaria
        )
        resultado.pack(anchor="w", padx=32, pady=(0, 10))

        def buscar():
            extensao = entrada.get().strip().lower()

            if not extensao:
                messagebox.showwarning(
                    "Extensão necessária",
                    "Digite uma extensão, por exemplo .pdf."
                )
                return

            if not extensao.startswith("."):
                extensao = "." + extensao

            tabela.delete(*tabela.get_children())
            encontrados = 0

            for arquivo in self.listar_arquivos(recursivo=True):
                if arquivo.suffix.lower() == extensao:
                    try:
                        tamanho = arquivo.stat().st_size
                        tabela.insert(
                            "", "end",
                            values=(
                                arquivo.name,
                                str(arquivo.parent),
                                self.formatar_tamanho(tamanho)
                            )
                        )
                        encontrados += 1
                    except OSError:
                        continue

            resultado.config(
                text=f"{encontrados} arquivo(s) encontrado(s)."
            )

        self.criar_botao(
            controles, "Buscar", buscar, principal=True
        ).pack(side="left", padx=10)

        entrada.bind("<Return>", lambda evento: buscar())
        entrada.focus_set()

    # -----------------------------------------------------
    # ANALISAR ESPAÇO
    # -----------------------------------------------------

    def mostrar_espaco(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Analisar espaço",
            "Veja quanto espaço os arquivos ocupam por categoria, "
            "incluindo subpastas."
        )

        area = tk.Frame(self.conteudo, bg=self.cor_fundo)
        area.pack(fill="both", expand=True, padx=30, pady=5)

        tabela = self.criar_tabela(
            area,
            {
                "Categoria": 220,
                "Quantidade": 130,
                "Espaço ocupado": 180
            }
        )

        totais = {}
        quantidades = {}
        total_geral = 0

        for arquivo in self.listar_arquivos(recursivo=True):
            categoria = self.identificar_categoria(arquivo)

            try:
                tamanho = arquivo.stat().st_size
            except OSError:
                continue

            totais[categoria] = totais.get(categoria, 0) + tamanho
            quantidades[categoria] = quantidades.get(categoria, 0) + 1
            total_geral += tamanho

        for categoria in sorted(totais):
            tabela.insert(
                "", "end",
                values=(
                    categoria,
                    quantidades[categoria],
                    self.formatar_tamanho(totais[categoria])
                )
            )

        resumo = tk.Label(
            self.conteudo,
            text=(
                f"Total: {sum(quantidades.values())} arquivo(s)  |  "
                f"{self.formatar_tamanho(total_geral)}"
            ),
            font=("Segoe UI", 12, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_texto
        )
        resumo.pack(anchor="w", padx=32, pady=15)

        self.criar_botao(
            self.conteudo,
            "Atualizar análise",
            self.mostrar_espaco,
            principal=True
        ).pack(anchor="w", padx=30, pady=(0, 20))

    # -----------------------------------------------------
    # LIMPEZA DE ARQUIVOS ANTIGOS
    # -----------------------------------------------------

    def mostrar_limpeza(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Limpar arquivos antigos",
            "Arquivos com última modificação anterior a 7 dias, "
            "incluindo subpastas."
        )

        tk.Label(
            self.conteudo,
            text="Os arquivos serão enviados para a Lixeira, "
                 "não excluídos permanentemente.",
            bg=self.cor_fundo,
            fg=self.cor_secundaria,
            wraplength=700,
            justify="left"
        ).pack(anchor="w", padx=32, pady=(0, 12))

        arquivos_antigos = []
        limite = datetime.now() - timedelta(days=7)

        for arquivo in self.listar_arquivos(recursivo=True):
            try:
                modificacao = datetime.fromtimestamp(
                    arquivo.stat().st_mtime
                )

                if modificacao < limite:
                    arquivos_antigos.append(arquivo)

            except OSError:
                continue

        area = tk.Frame(self.conteudo, bg=self.cor_fundo)
        area.pack(fill="both", expand=True, padx=30, pady=5)

        tabela = self.criar_tabela(
            area,
            {
                "Arquivo": 220,
                "Pasta": 300,
                "Modificado em": 150
            }
        )

        for arquivo in arquivos_antigos:
            try:
                data = datetime.fromtimestamp(
                    arquivo.stat().st_mtime
                ).strftime("%d/%m/%Y %H:%M")

                tabela.insert(
                    "", "end",
                    values=(
                        arquivo.name,
                        str(arquivo.parent),
                        data
                    )
                )
            except OSError:
                continue

        tk.Label(
            self.conteudo,
            text=f"{len(arquivos_antigos)} arquivo(s) antigo(s) encontrado(s).",
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(anchor="w", padx=32, pady=10)

        def limpar():
            # Recalcula a lista para evitar usar dados desatualizados.
            atuais = []

            for arquivo in self.listar_arquivos(recursivo=True):
                try:
                    if datetime.fromtimestamp(
                        arquivo.stat().st_mtime
                    ) < datetime.now() - timedelta(days=7):
                        atuais.append(arquivo)
                except OSError:
                    continue

            if not atuais:
                messagebox.showinfo(
                    "Limpeza",
                    "Nenhum arquivo antigo foi encontrado."
                )
                self.mostrar_limpeza()
                return

            if not messagebox.askyesno(
                "Confirmar limpeza",
                f"Enviar {len(atuais)} arquivo(s) para a Lixeira?"
            ):
                return

            enviados = 0
            falhas = 0

            for arquivo in atuais:
                try:
                    send2trash(str(arquivo))
                    enviados += 1
                except Exception as erro:
                    falhas += 1
                    print(f"Erro ao enviar {arquivo}: {erro}")

            messagebox.showinfo(
                "Limpeza concluída",
                f"Enviados para a Lixeira: {enviados}\n"
                f"Falhas: {falhas}"
            )

            self.mostrar_limpeza()

        botoes = tk.Frame(self.conteudo, bg=self.cor_fundo)
        botoes.pack(fill="x", padx=30, pady=15)

        self.criar_botao(
            botoes, "Enviar antigos para a Lixeira",
            limpar, principal=True
        ).pack(side="left")

        self.criar_botao(
            botoes, "Atualizar lista", self.mostrar_limpeza
        ).pack(side="left", padx=10)

    # -----------------------------------------------------
    # CONFIGURAÇÕES
    # -----------------------------------------------------

    def mostrar_configuracoes(self):
        self.limpar_tela()
        self.criar_cabecalho(
            "Configurações",
            "Escolha qual pasta será gerenciada pelo aplicativo."
        )

        painel = tk.Frame(
            self.conteudo,
            bg="white",
            highlightbackground="#DCE6F3",
            highlightthickness=1
        )
        painel.pack(fill="x", padx=30, pady=5)

        tk.Label(
            painel,
            text="Pasta monitorada",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(18, 8))

        caminho = tk.Label(
            painel,
            text=str(self.pasta_downloads),
            bg="white",
            fg=self.cor_secundaria,
            wraplength=650,
            justify="left"
        )
        caminho.pack(anchor="w", padx=20, pady=5)

        def selecionar_pasta():
            escolhida = filedialog.askdirectory(
                title="Selecione a pasta a gerenciar",
                initialdir=str(self.pasta_downloads)
            )

            if escolhida:
                nova_pasta = Path(escolhida)

                if not nova_pasta.is_dir():
                    messagebox.showerror(
                        "Pasta inválida",
                        "A pasta selecionada não existe."
                    )
                    return

                self.pasta_downloads = nova_pasta
                caminho.config(text=str(nova_pasta))
                self.atualizar_status()

                messagebox.showinfo(
                    "Configuração atualizada",
                    "A pasta foi alterada nesta sessão."
                )

        self.criar_botao(
            painel, "Selecionar pasta",
            selecionar_pasta, principal=True
        ).pack(anchor="w", padx=20, pady=(12, 20))

        tk.Label(
            self.conteudo,
            text="A alteração da pasta é temporária nesta versão. "
                 "Ao fechar e abrir o programa, o caminho padrão "
                 "será utilizado novamente.",
            bg=self.cor_fundo,
            fg=self.cor_secundaria,
            wraplength=700,
            justify="left"
        ).pack(anchor="w", padx=32, pady=20)


# =========================================================
# INICIALIZAÇÃO
# =========================================================

if __name__ == "__main__":
    janela = tk.Tk()
    app = LimpadorDownloads(janela)
    janela.mainloop()
