# Aqui começa os testes realizados nas aulas de TKINTER
# A partir do vídeo: https://www.youtube.com/watch?v=RtrZcoVD1WM&list=PLqx8fDb-FZDFznZcXb_u_NyiQ7Nai674-
# Aula 16, 17 e 18> Estilizar os botões da tela e criando executável do projeto
#
#
#
from tkinter import *
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
# from PIL import ImageTk_, Image
#
# váriável com o nome da janela
root = Tk()
# criando configurações dentro da janela
# criação de classes


class Relatorios():
    def printCliente(self):
        # Exibe e salva o arquivo PDF
        webbrowser.open("cliente.pdf")

    def gerarRelatCliente(self):
        # Edita o arquivo
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone:')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.telefoneRel)
        self.c.drawString(150, 600, self.cidadeRel)
        # Para criar linhas espaçamentos molduras
        self.c.rect(20, 720, 550, 200, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        print("Conectando ao banco de dados")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando ao banco de dados")

    def montaTabelas(self):
        self.conecta_bd()
        # Criação da tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
                            cod INTEGER PRIMARY KEY,
                            nome_cliente CHAR(40) NOT NULL,
                            telefone INTEGER(20),
                            cidade CHAR(40)
                            );
                        """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def variáveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        self.variáveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
                                    ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variáveis()
        self.conecta_bd()
        self.cursor.execute(
            """DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variáveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ? """,
                            (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()


class Aplication(Funcs, Relatorios):
    # dentro dessa classe é criado FUNÇÕES (DEF) para ela, e para isso as varáveis precisam ser repetidas dentro do self
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='gray7')
        self.root.geometry("700x500")
        # define se a tela será expansiva (horizontal, vertical) exemplo (tela fixa: false, false)
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)
    # função especifica para os frames

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='lemon chiffon',
                             highlightbackground='SlateBlue2', highlightthickness=3)
        # aqui pode ser usado o PLACE O PACK OU O GRID
        # place coloca a posição especifica na tela, tem mais liberdade
        # 0 a 1 - 0 lado esquerdo 1 lado direito da tela
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame_2 = Frame(self.root, bd=4, bg='lemon chiffon',
                             highlightbackground='SlateBlue2', highlightthickness=3)
        # 0 a 1 - 0 lado esquerdo 1 lado direito da tela
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='#1e3743',
                                highlightbackground='gray', highlightthickness=5)
        self.canvas_bt.place(relx=0.19, rely=0.08,
                             relwidth=0.22, relheight=0.19)
        # Criação do botão limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=3,
                                bg='#107db2', fg='white', activebackground='#108ecb', activeforeground="white", font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=3,
                                bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão novo
        self.bt_novo = Button(self.frame_1, text="Novo", bd=3,
                              bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=3,
                                 bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=3,
                                bg='#107db2', fg='white', font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

    # Criação da label e entrada do código
        self.lb_codigo = Label(self.frame_1, text="Código",
                               bg='lemon chiffon', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

     # Criação da label e entrada do nome do cliente
        self.lb_nome = Label(self.frame_1, text="Nome",
                             bg='lemon chiffon', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

     # Criação da label e entrada do telefone
        self.lb_telefone = Label(
            self.frame_1, text="Telefone", bg='lemon chiffon', fg='#107db2')
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

     # Criação da label e entrada do cidade
        self.lb_cidade = Label(self.frame_1, text="Cidade",
                               bg='lemon chiffon', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(
            self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1,
                               relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatórios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Limpa cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente",
                              command=self.gerarRelatCliente)


# chamar a classe
Aplication()
# repete a varíavel, ja que sem essa repetição a janela se abre e se fecha por milisegundos
root.mainloop()
