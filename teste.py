import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Disco:
    def __init__(self, titulo, artista, genero, preco, estoque):
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.preco = preco
        self.estoque = estoque

class LojaDiscos:
    def __init__(self):
        self.discos = []

    def adicionar_disco(self, disco):
        self.discos.append(disco)

    def remover_disco(self, titulo):
        for disco in self.discos:
            if disco.titulo.lower() == titulo.lower():
                self.discos.remove(disco)
                return True
        return False

    def listar_disco(self):
        return self.discos

    def buscar_disco(self, artista):
        return [disco for disco in self.discos if artista.lower() in disco.artista.lower()]

# Instância da loja de discos
loja = LojaDiscos()

# Função de cada botão
def adicionar_disco():
    add_window = ctk.CTkToplevel(root)
    add_window.title("Adicionar Disco")
    add_window.geometry("400x400")
    add_window.grab_set()

    ctk.CTkLabel(add_window, text="Título").grid(row=0, column=0, padx=10, pady=10)
    titulo_entry = ctk.CTkEntry(add_window, width=200)
    titulo_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Artista").grid(row=1, column=0, padx=10, pady=10)
    artista_entry = ctk.CTkEntry(add_window, width=200)
    artista_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Gênero").grid(row=2, column=0, padx=10, pady=10)
    genero_entry = ctk.CTkEntry(add_window, width=200)
    genero_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Preço").grid(row=3, column=0, padx=10, pady=10)
    preco_entry = ctk.CTkEntry(add_window, width=200)
    preco_entry.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(add_window, text="Estoque").grid(row=4, column=0, padx=10, pady=10)
    estoque_entry = ctk.CTkEntry(add_window, width=200)
    estoque_entry.grid(row=4, column=1, padx=10, pady=10)

    def confirmar_adicao(event=None):
        titulo = titulo_entry.get()
        artista = artista_entry.get()
        genero = genero_entry.get()
        preco = preco_entry.get()
        estoque = estoque_entry.get()

        if titulo and artista and genero and preco and estoque:
            try:
                preco = float(preco)
                estoque = int(estoque)
                novo_disco = Disco(titulo, artista, genero, preco, estoque)
                loja.adicionar_disco(novo_disco)
                messagebox.showinfo("Sucesso", "Disco adicionado com sucesso!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Preço e estoque devem ser números.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    ctk.CTkButton(add_window, text="Confirmar", command=confirmar_adicao).grid(row=5, column=1, pady=20)
    add_window.bind("<Return>", confirmar_adicao)

def listar_discos():
    list_window = ctk.CTkToplevel(root)
    list_window.title("Lista de Discos")
    list_window.geometry("400x400")
    list_window.grab_set()

    # Lista discos
    scrollable_frame = ctk.CTkScrollableFrame(list_window, width=380, height=380)
    scrollable_frame.pack(padx=10, pady=10, expand=True, fill="both")

    discos = loja.listar_disco()
    if not discos:
        ctk.CTkLabel(scrollable_frame, text="Nenhum disco cadastrado.").pack(pady=10)
    else:
        for disco in discos:
            disco_info = f"Título: {disco.titulo} | Artista: {disco.artista} | Gênero: {disco.genero} | Preço: R${disco.preco:.2f} | Estoque: {disco.estoque}"
            ctk.CTkLabel(scrollable_frame, text=disco_info, anchor="w").pack(pady=5, padx=5, fill="x")

def remover_disco():
    remove_window = ctk.CTkToplevel(root)
    remove_window.title("Remover Disco")
    remove_window.geometry("400x200")
    remove_window.grab_set()

    ctk.CTkLabel(remove_window, text="Título do Disco").grid(row=0, column=0, padx=10, pady=10)
    titulo_entry = ctk.CTkEntry(remove_window, width=200)
    titulo_entry.grid(row=0, column=1, padx=10, pady=10)

    def confirmar_remocao(event=None):
        titulo = titulo_entry.get()
        if titulo:
            if loja.remover_disco(titulo):
                messagebox.showinfo("Sucesso", "Disco removido com sucesso!")
                remove_window.destroy()
            else:
                messagebox.showerror("Erro", "Disco não encontrado.")
        else:
            messagebox.showerror("Erro", "Preencha o campo de título.")

    ctk.CTkButton(remove_window, text="Remover", command=confirmar_remocao).grid(row=1, column=1, pady=10)
    remove_window.bind("<Return>", confirmar_remocao)

def buscar_artista():
    buscar_window = ctk.CTkToplevel(root)
    buscar_window.title("Buscar Disco")
    buscar_window.geometry("400x200")
    buscar_window.grab_set()

    ctk.CTkLabel(buscar_window, text="Artista").grid(row=0, column=0, padx=10, pady=10)
    artista_entry = ctk.CTkEntry(buscar_window, width=200)
    artista_entry.grid(row=0, column=1, padx=10, pady=10)

    def confirmar_busca(event=None):
        artista = artista_entry.get()
        if artista:
            discos_encontrados = loja.buscar_disco(artista)
            if discos_encontrados:
                resultados_window = ctk.CTkToplevel(buscar_window)
                resultados_window.title("Discos Encontrados")
                resultados_window.geometry("400x300")
                resultados_window.grab_set()

                resultados_frame = ctk.CTkScrollableFrame(resultados_window, width=380, height=280)
                resultados_frame.pack(padx=10, pady=10, expand=True, fill="both")

                for disco in discos_encontrados:
                    disco_info = f"Título: {disco.titulo} | Artista: {disco.artista} | Gênero: {disco.genero} | Preço: R${disco.preco:.2f} | Estoque: {disco.estoque}"
                    ctk.CTkLabel(resultados_frame, text=disco_info, anchor="w").pack(pady=5, padx=5, fill="x")
            else:
                messagebox.showinfo("Resultado", "Nenhum disco encontrado para esse artista.")
        else:
            messagebox.showerror("Erro", "Preencha o campo de artista.")

    ctk.CTkButton(buscar_window, text="Buscar", command=confirmar_busca).grid(row=1, column=1, pady=10)
    buscar_window.bind("<Return>", confirmar_busca)

# Janela principal
root = ctk.CTk()
root.title("Início - Let's Rock - Discos de vinil")
root.geometry("400x400")


frame_central = ctk.CTkFrame(root)
frame_central.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkButton(frame_central, text="Adicionar Disco", command=adicionar_disco, width=200).pack(pady=5)
ctk.CTkButton(frame_central, text="Remover Disco", command=remover_disco, width=200).pack(pady=5)
ctk.CTkButton(frame_central, text="Listar Discos", command=listar_discos, width=200).pack(pady=5)
ctk.CTkButton(frame_central, text="Buscar por Artista", command=buscar_artista, width=200).pack(pady=5)

root.mainloop()