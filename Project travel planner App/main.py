import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Text, messagebox

from planeador import ViagemCrazy
from utilizador import User
import database


class AppTrivago:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Planeador de Viagens")
        self.raiz.geometry("300x300")

        # Utilizador atualmente "com sessão iniciada" na app
        self.utilizador_atual = None
        self.utilizador_atual_id = None

        # Prepara a base de dados (cria as tabelas se ainda não existirem)
        database.criar_tabelas()

        # Se existir um dados.json antigo, migra automaticamente para a BD
        migradas = database.migrar_json_para_bd()
        if migradas:
            print(f"{migradas} sugestões migradas do dados.json para a base de dados.")

        Button(raiz, text="Utilizador", command=self.utilizador).pack(pady=20)
        Button(raiz, text="Administrador", command=self.administrador).pack(pady=20)

    # ---------------- Utilizador ----------------

    def utilizador(self):
        janela = Toplevel(self.raiz)
        janela.title("Utilizador")
        janela.geometry("300x300")

        self.nome_input = Entry(janela)
        self.idade_input = Entry(janela)
        self.email_input = Entry(janela)

        Label(janela, text="Nome:").pack()
        self.nome_input.pack()

        Label(janela, text="Idade:").pack()
        self.idade_input.pack()

        Label(janela, text="Email:").pack()
        self.email_input.pack()

        Button(janela, text="Marcar viagem", command=self.verificar_entradas).pack(pady=20)

    def verificar_entradas(self):
        nome = self.nome_input.get().strip()
        idade_texto = self.idade_input.get().strip()
        email = self.email_input.get().strip()

        if not nome or not idade_texto or not email:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.")
            return

        if not idade_texto.isdigit():
            messagebox.showwarning("Idade Inválida", "A idade tem de ser um número inteiro.")
            return

        idade = int(idade_texto)
        if idade <= 0 or idade > 120:
            messagebox.showwarning("Idade Inválida", "Insira uma idade real.")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showwarning("Email Inválido", "Insira um endereço de email válido.")
            return

        # --- Aqui a classe User é finalmente criada e usada ---
        self.utilizador_atual = User(nome, idade, email)
        self.utilizador_atual.exibir()  # útil para acompanhar na consola
        self.utilizador_atual_id = database.guardar_utilizador(nome, idade, email)

        self.nova_viagem()

    # ---------------- Administrador ----------------

    def administrador(self):
        janela = Toplevel(self.raiz)
        janela.title("Admin Only")
        janela.geometry("300x300")

        self.admin_password_input = Entry(janela, show="*")
        Label(janela, text="Password:").pack()
        self.admin_password_input.pack()

        Button(janela, text="Login", command=self.verificar_password).pack(pady=10)

    def verificar_password(self):
        password = self.admin_password_input.get()

        if password == "admin123":
            self.abrir_opcoes_administrador()
        else:
            messagebox.showerror("Erro", "Senha de administrador incorreta!")

    def abrir_opcoes_administrador(self):
        janela = Toplevel(self.raiz)
        janela.title("Opções do Administrador")
        janela.geometry("300x300")

        Button(janela, text="Adicionar Sugestões", command=self.adicionar_sugestoes).pack(pady=10)
        Button(janela, text="Carregar Sugestões", command=self.carregar_sugestoes).pack(pady=10)
        Button(janela, text="Ver Todas as Reservas", command=self.ver_todas_reservas).pack(pady=10)

    def ver_todas_reservas(self):
        """Vista de administrador: mostra as reservas de todos os utilizadores."""
        reservas = database.carregar_todas_reservas()

        janela = Toplevel(self.raiz)
        janela.title("Todas as Reservas")
        janela.geometry("420x420")

        if not reservas:
            Label(janela, text="Ainda não há reservas registadas.").pack(pady=30)
            return

        lista_frame = self._criar_area_scrollavel(janela)

        for r in reservas:
            texto = (
                f"Cliente: {r['Nome']} ({r['Email']})\n"
                f"Destino: {r['Destino']}\n"
                f"Reserva: {r['Reserva']}\n"
                f"Preço: {r['Orçamento']}\n"
                f"Data: {r['Data']}"
            )
            Label(
                lista_frame,
                text=texto,
                justify="left",
                anchor="w",
                relief="groove",
                borderwidth=1,
                wraplength=370,
            ).pack(fill="x", padx=10, pady=5)

    def adicionar_sugestoes(self):
        janela = Toplevel(self.raiz)
        janela.title("Inserir Sugestões")
        janela.geometry("300x200")

        self.entrada_destino = Entry(janela)
        self.entrada_reserva = Entry(janela)
        self.entrada_orcamento = Entry(janela)

        Label(janela, text="Destino:").pack()
        self.entrada_destino.pack()

        Label(janela, text="Reserva:").pack()
        self.entrada_reserva.pack()

        Label(janela, text="Preço:").pack()
        self.entrada_orcamento.pack()

        Button(janela, text="Salvar", command=self.salvar_dados_int).pack(pady=20)

    def salvar_dados_int(self):
        destino = self.entrada_destino.get().strip()
        reserva = self.entrada_reserva.get().strip()
        orcamento = self.entrada_orcamento.get().strip()

        if not destino or not reserva or not orcamento:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.")
            return

        # --- Aqui a classe ViagemCrazy é finalmente criada e usada ---
        nova_sugestao = ViagemCrazy(destino, reserva, orcamento)
        nova_sugestao.exibir()  # útil para acompanhar na consola

        database.guardar_sugestao(
            nova_sugestao.destino, nova_sugestao.reserva, nova_sugestao.orcamento
        )
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso na base de dados!")

    def carregar_sugestoes(self):
        dados = database.carregar_sugestoes()
        janela = Toplevel(self.raiz)
        janela.title("Sugestões Carregadas")
        janela.geometry("300x300")

        texto_sugestoes = Text(janela)
        texto_sugestoes.pack(expand=True, fill="both")

        if not dados:
            texto_sugestoes.insert(tk.END, "Ainda não há sugestões guardadas.")
            return

        for dado in dados:
            texto_sugestoes.insert(
                tk.END,
                f"Destino: {dado['Destino']}\nReserva: {dado['Reserva']}\nPreço: {dado['Orçamento']}\n\n",
            )

    # ---------------- Pesquisa de viagens ----------------

    def nova_viagem(self):
        janela = Toplevel(self.raiz)
        janela.title("Nova Viagem")
        janela.geometry("300x300")

        frame_destino = tk.Frame(janela)
        frame_destino.pack(pady=10, fill="x")
        Label(frame_destino, text="Insira o Destino: ").pack(side="left")
        self.destino_input = Entry(frame_destino)
        self.destino_input.pack(side="right", expand=True, fill="x")

        Button(janela, text="Procurar", command=self.opcoes).pack(pady=10)
        Button(janela, text="As Minhas Reservas", command=self.ver_minhas_reservas).pack(pady=5)

    def opcoes(self):
        destino = self.destino_input.get().strip()

        if not destino:
            messagebox.showwarning("Campo vazio", "Por favor, insira um destino.")
            return

        # Pesquisa parcial (contém o texto), já não precisa de ser exato
        encontrados = database.procurar_por_destino(destino)

        # Regista a pesquisa (independentemente de haver ou não resultados)
        if self.utilizador_atual_id is not None:
            database.registar_viagem_marcada(self.utilizador_atual_id, None, destino)

        janela = Toplevel(self.raiz)
        janela.title("Opções")
        janela.geometry("400x420")

        if not encontrados:
            Label(
                janela,
                text="Nenhuma opção encontrada para o destino especificado.",
                wraplength=340,
                justify="left",
            ).pack(pady=30, padx=20)
            return

        Label(
            janela, text=f"Resultados para '{destino}':", font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))

        lista_frame = self._criar_area_scrollavel(janela)

        for dado in encontrados:
            self._criar_linha_opcao(lista_frame, dado)

    def _criar_area_scrollavel(self, janela):
        """Cria uma área com scroll vertical dentro da janela e devolve o
        frame interior onde podes adicionar as linhas de conteúdo."""
        canvas = tk.Canvas(janela, highlightthickness=0)
        scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
        frame_interior = tk.Frame(canvas)

        frame_interior.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=frame_interior, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame_interior

    def _criar_linha_opcao(self, lista_frame, dado):
        """Cria uma linha com os dados da sugestão e um botão 'Reservar'."""
        linha = tk.Frame(lista_frame, relief="groove", borderwidth=1)
        linha.pack(fill="x", padx=10, pady=5)

        texto = (
            f"Destino: {dado['Destino']}\n"
            f"Reserva: {dado['Reserva']}\n"
            f"Preço: {dado['Orçamento']}"
        )
        Label(linha, text=texto, justify="left", anchor="w", wraplength=250).pack(
            side="left", padx=5, pady=5, fill="x", expand=True
        )

        ja_reservado = database.utilizador_ja_reservou(self.utilizador_atual_id, dado["id"])

        botao = Button(
            linha,
            text="Reservado ✓" if ja_reservado else "Reservar",
            state="disabled" if ja_reservado else "normal",
        )
        botao.pack(side="right", padx=10)
        botao.config(command=lambda d=dado, b=botao: self.reservar_quarto(d, b))

    def reservar_quarto(self, dado, botao):
        """Confirma e regista a reserva de um quarto/opção específica."""
        confirmar = messagebox.askyesno(
            "Confirmar Reserva",
            f"Confirmas a reserva de:\n\n"
            f"{dado['Reserva']}\n"
            f"Destino: {dado['Destino']}\n"
            f"Preço: {dado['Orçamento']}",
        )
        if not confirmar:
            return

        database.criar_reserva(self.utilizador_atual_id, dado["id"])
        botao.config(text="Reservado ✓", state="disabled")
        messagebox.showinfo("Reserva Confirmada", "A tua reserva foi confirmada com sucesso!")

    def ver_minhas_reservas(self):
        """Mostra ao utilizador todas as reservas que já confirmou."""
        reservas = database.carregar_reservas_utilizador(self.utilizador_atual_id)

        janela = Toplevel(self.raiz)
        janela.title("As Minhas Reservas")
        janela.geometry("400x400")

        if not reservas:
            Label(janela, text="Ainda não tens nenhuma reserva confirmada.").pack(pady=30)
            return

        lista_frame = self._criar_area_scrollavel(janela)

        for r in reservas:
            texto = (
                f"Destino: {r['Destino']}\n"
                f"Reserva: {r['Reserva']}\n"
                f"Preço: {r['Orçamento']}\n"
                f"Reservado em: {r['Data']}"
            )
            Label(
                lista_frame,
                text=texto,
                justify="left",
                anchor="w",
                relief="groove",
                borderwidth=1,
                wraplength=350,
            ).pack(fill="x", padx=10, pady=5)


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppTrivago(raiz)
    raiz.mainloop()
