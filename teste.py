import json
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# Classe Disco
class Disco:
    def __init__(self, titulo, artista, genero, ano, preco, estoque):
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.ano = ano
        self.preco = preco
        self.estoque = estoque


# Classe Loja de Discos
class LojaDiscos:
    def __init__(self):
        self.discos = []

    def adicionar_disco(self, disco):
        self.discos.append(disco)
        salvar_discos()

    def remover_disco(self, titulo):
        for disco in self.discos:
            if disco.titulo.lower() == titulo.lower():
                self.discos.remove(disco)
                return True
        return False

    def listar_disco(self):
        return self.discos
    
    def buscar_disco(self, termo):
        termo = termo.lower()
        return [
            disco for disco in self.discos
            if termo in disco.titulo.lower() or
               termo in disco.artista.lower() or
               termo in disco.genero.lower() or
               termo == str(disco.ano)
        ]
    

# Instância da loja de discos
loja = LojaDiscos()

# Funções de gerenciamento de discos
def adicionar_disco():
    add_window = ctk.CTkToplevel(root)
    add_window.title("Adicionar Disco")
    add_window.geometry("400x450")
    add_window.grab_set()

    # Campos para inserir dados do disco
    campos = ["Título", "Artista", "Gênero", "Ano", "Preço", "Estoque"]
    entradas = {}
    for i, campo in enumerate(campos):
        ctk.CTkLabel(add_window, text=campo).grid(row=i, column=0, padx=10, pady=10)
        entrada = ctk.CTkEntry(add_window, width=200)
        entrada.grid(row=i, column=1, padx=10, pady=10)
        entradas[campo] = entrada

    salvar_discos()


    def confirmar_adicao():
        try:
            titulo = entradas["Título"].get()
            artista = entradas["Artista"].get()
            genero = entradas["Gênero"].get()
            ano = int(entradas["Ano"].get())
            preco = float(entradas["Preço"].get())
            estoque = int(entradas["Estoque"].get())

            if not titulo or not artista or not genero:
                raise ValueError("Preencha todos os campos!")

            novo_disco = Disco(titulo, artista, genero, ano, preco, estoque)
            loja.adicionar_disco(novo_disco)
            messagebox.showinfo("Sucesso", "Disco adicionado com sucesso!")
            add_window.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")

    ctk.CTkButton(add_window, text="Adicionar", command=confirmar_adicao).grid(
        row=len(campos), column=1, pady=10
    )


def listar_discos():
    list_window = ctk.CTkToplevel(root)
    list_window.title("Lista de Discos")
    list_window.geometry("600x400")
    list_window.grab_set()

    scrollable_frame = ctk.CTkScrollableFrame(list_window, width=580, height=380)
    scrollable_frame.pack(padx=10, pady=10, expand=True, fill="both")

    discos = loja.listar_disco()
    if not discos:
        ctk.CTkLabel(scrollable_frame, text="Nenhum disco cadastrado.").pack(pady=10)
    else:
        for disco in discos:
            frame = ctk.CTkFrame(scrollable_frame, border_width=1, corner_radius=5)
            frame.pack(fill="x", padx=5, pady=5)

            disco_info = (
                f"Título: {disco.titulo} | Artista: {disco.artista} | "
                f"Gênero: {disco.genero} | Ano: {disco.ano} | "
                f"Preço: R${disco.preco:.2f} | Estoque: {disco.estoque}"
            )
            ctk.CTkLabel(frame, text=disco_info, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkButton(frame, text="Editar", command=lambda d=disco: editar_disco(d)).pack(
                side="right", padx=5, pady=5
            )


def buscar_disco():
    search_window = ctk.CTkToplevel(root)
    search_window.title("Buscar Disco")
    search_window.geometry("600x400")
    search_window.grab_set()

    ctk.CTkLabel(search_window, text="Digite o termo de busca:").pack(pady=10)
    termo_entry = ctk.CTkEntry(search_window, width=400)
    termo_entry.pack(pady=10)

    def realizar_busca():
        termo = termo_entry.get()
        resultados = loja.buscar_disco(termo)
        resultados_frame = ctk.CTkScrollableFrame(search_window, width=580, height=300)
        resultados_frame.pack(padx=10, pady=10, expand=True, fill="both")

        for widget in resultados_frame.winfo_children():
            widget.destroy()  # Limpar resultados anteriores

        if not resultados:
            ctk.CTkLabel(resultados_frame, text="Nenhum resultado encontrado.").pack(pady=10)
        else:
            for disco in resultados:
                frame = ctk.CTkFrame(resultados_frame, border_width=1, corner_radius=5)
                frame.pack(fill="x", padx=5, pady=5)

                disco_info = (
                    f"Título: {disco.titulo} | Artista: {disco.artista} | "
                    f"Gênero: {disco.genero} | Ano: {disco.ano} | "
                    f"Preço: R${disco.preco:.2f} | Estoque: {disco.estoque}"
                )
                ctk.CTkLabel(frame, text=disco_info, anchor="w").pack(side="left", padx=5, pady=5)

    ctk.CTkButton(search_window, text="Buscar", command=realizar_busca).pack(pady=10)


def remover_disco():
    remove_window = ctk.CTkToplevel(root)
    remove_window.title("Remover Disco")
    remove_window.geometry("400x200")
    remove_window.grab_set()

    ctk.CTkLabel(remove_window, text="Título do Disco").grid(row=0, column=0, padx=10, pady=10)
    titulo_entry = ctk.CTkEntry(remove_window, width=200)
    titulo_entry.grid(row=0, column=1, padx=10, pady=10)

    def confirmar_remocao():
        titulo = titulo_entry.get()
        if loja.remover_disco(titulo):
            messagebox.showinfo("Sucesso", "Disco removido com sucesso!")
            remove_window.destroy()
        else:
            messagebox.showerror("Erro", "Disco não encontrado.")

    ctk.CTkButton(remove_window, text="Remover", command=confirmar_remocao).grid(
        row=1, column=1, pady=10
    )

def editar_disco(disco):
    edit_window = ctk.CTkToplevel(root)
    edit_window.title(f"Editar Disco: {disco.titulo}")
    edit_window.geometry("400x450")
    edit_window.grab_set()

    # Campos para editar dados do disco
    campos = {
        "Título": disco.titulo,
        "Artista": disco.artista,
        "Gênero": disco.genero,
        "Ano": disco.ano,
        "Preço": disco.preco,
        "Estoque": disco.estoque,
    }
    entradas = {}
    for i, (campo, valor) in enumerate(campos.items()):
        ctk.CTkLabel(edit_window, text=campo).grid(row=i, column=0, padx=10, pady=10)
        entrada = ctk.CTkEntry(edit_window, width=200)
        entrada.insert(0, str(valor))
        entrada.grid(row=i, column=1, padx=10, pady=10)
        entradas[campo] = entrada

    def salvar_edicao():
        try:
            disco.titulo = entradas["Título"].get()
            disco.artista = entradas["Artista"].get()
            disco.genero = entradas["Gênero"].get()
            disco.ano = int(entradas["Ano"].get())
            disco.preco = float(entradas["Preço"].get())
            disco.estoque = int(entradas["Estoque"].get())
            messagebox.showinfo("Sucesso", "Disco atualizado com sucesso!")
            edit_window.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Verifique os campos e tente novamente.")

    ctk.CTkButton(edit_window, text="Salvar", command=salvar_edicao).grid(
        row=len(campos), column=1, pady=10
    )
# Função para salvar discos
def salvar_discos():
    with open('discos.json', 'w') as file:
        json.dump([disco.__dict__ for disco in loja.discos], file, indent=4)

#Função para carregar discos
def carregar_discos():
    try:
        with open('discos.json', 'r', encoding="utf-8") as file:
            discos_data = json.load(file)
            for data in discos_data:
                loja.adicionar_disco(Disco(**data))
    except FileNotFoundError:
        pass


# Funções de autenticação
def carregar_usuarios():
    try:
        with open('usuarios.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def verificar_credenciais(username, password, usuarios):
    for usuario in usuarios:
        if usuario["username"] == username and usuario["password"] == password:
            return True
    return False


def tela_login():
    login_window = ctk.CTk()
    login_window.title("Login - Let's Rock")
    login_window.geometry("600x400")

    usuarios = carregar_usuarios()

    frame_login = ctk.CTkFrame(login_window)
    frame_login.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame_login, text="Usuário").grid(row=0, column=0, padx=10, pady=10)
    username_entry = ctk.CTkEntry(frame_login, width=200)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_login, text="Senha").grid(row=1, column=0, padx=10, pady=10)
    password_entry = ctk.CTkEntry(frame_login, width=200, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def verificar_login():
        if verificar_credenciais(username_entry.get(), password_entry.get(), usuarios):
            messagebox.showinfo("Login", "Bem-vindo! ")
            login_window.destroy()
            tela_principal()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")

    ctk.CTkButton(frame_login, text="Entrar", command=verificar_login).grid(
        row=2, column=1, pady=10
    )

    login_window.mainloop()


# Tela principal!!!!
def tela_principal():
    global root
    root = ctk.CTk()
    root.title("Let's Rock - Loja de Discos")
    root.geometry("600x400")

    frame_main = ctk.CTkFrame(root)
    frame_main.place(relx=0.5, rely=0.5, anchor="center")


    ctk.CTkButton(frame_main, text="Adicionar Disco", command=adicionar_disco).grid(
        row=0, column=0, padx=10, pady=10
    )
    ctk.CTkButton(frame_main, text="Listar Discos", command=listar_discos).grid(
        row=0, column=1, padx=10, pady=10
    )
    ctk.CTkButton(frame_main, text="Buscar por Termo", command=buscar_disco).grid(
        row=1, column=0, padx=10, pady=10
    )
    ctk.CTkButton(frame_main, text="Remover Disco", command=remover_disco).grid(
        row=1, column=1, padx=10, pady=10
    )

    carregar_discos()

    root.mainloop()


# Programa começa com a parte do login
tela_login()
