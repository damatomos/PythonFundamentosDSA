# Game Ping-Pong

from tkinter import *
import random
import time

# variavel que recebe o valor do nivel digitado, o valor inserido pelo usuario e convertido para inteiro
level = int(input("Qual nível você gostaria de jogar? 1/2/3/4/5 \n"))
# variavel que recebe o valor de 500 dividido pelo nivel informado ( se refere ao tamanho da barra )
length = 500/level

# cria um objeto do tipo TKinter
root = Tk()
# adiciona um titulo ao objeto
root.title("Ping Pong")
#define se a janela vai ser escalonavel e passa 1 ou True para verdadeiro e 0 ou False para falso em cada eixo (x, y)
root.resizable(0, 0) # define que nao pode escalonar em nenhum dos eixo
# wm ou Window Manager se refere as configuracoes que podem ser passadas para a janela
root.wm_attributes("-topmost", 1) # define que a janela vai abrir em cima das outras, sendo 0 para abrir abaixo e outros valores para abrir por cima

# o canvas e uma area retangular para desenhar na tela
# root se refere ao pai da janela que no caso seria o objeto TK com suas configuracoes
# width e height definem o tamanho da tela
# bd define o tamanho da borda
# bg define a cor de background
#highlightthickness se refere a uma borda highlight ao redor da janela
border_size = 0
highlight_size = 50
canvas = Canvas(root, width=800, height=600, bd=border_size, bg="#ffaa00", highlightthickness=highlight_size)
# organiza os elementos da tela em bloco antes de colocar na janela
canvas.pack()

# atualiza e redesenha os elementos na tela
root.update()

# Variável para contar o score
count = 0
# variavel para definir se o jogador perdeu
lost = False

class Bola:
    # construtor que recebe o canvas, o objeto da barra e uma cor
    def __init__(self, canvas, Barra, color, radius=8):
        self.canvas = canvas
        self.Barra = Barra
        self.size = radius * 2
        # cria uma elipse
        # que comeca da posicao 0 e preenche ate size ( posicao 15) em x e y
        self.id = canvas.create_oval(0, 0, self.size, self.size, fill=color)

        self.canvas_height = self.canvas.winfo_height() # pega a altura da janela + a borda / highlight
        self.canvas_width = self.canvas.winfo_width() # pega a largura da janela + a borda / highlight
        #print(self.canvas_width, self.canvas_height)

        # move a elipse para o centro da tela em x e para uma margem de 200 em y
        self.canvas.move(self.id, self.canvas_width / 2 - radius, 200)

        starts_x = [-3, -2, -1, 1, 2, 3]
        # embaralha a lista
        random.shuffle(starts_x)

        self.speedX = starts_x[0] # pega o primeiro valor embaralhado
        self.speedY = -3 # define y como -3


    def draw(self):
        # move o desenho da bola para a posicao x e y definida
        self.canvas.move(self.id, self.speedX, self.speedY)

        pos = self.canvas.coords(self.id) # pega a posicao da bola x1, y1, x2, y2

        # verifica se esta no topo da tela
        if pos[1] <= border_size + highlight_size:
            # mude a velocidade em x para 3
            self.speedY = 3

        # verifica se esta na base da tela
        if pos[3] >= self.canvas_height - ( border_size + highlight_size ):
            # mude a velocidade em y para -3
            self.speedY = -3

        # verifica se esta no limite esquerdo da tela
        if pos[0] <= ( border_size + highlight_size ):
            # mude a velocidade em x para 3
            self.speedX = 3

        # verifica se esta no limite direito da tela
        if pos[2] >= self.canvas_width - ( border_size + highlight_size ):
            # mude a velocidade em x para -3
            self.speedX = -3

        # pega a posicao da barra (x1, y1, x2, y2)
        self.Barra_pos = self.canvas.coords(self.Barra.id)

        # se o canto direito da bola bater no canto esquerdo da barra e
        # o canto esquerdo da bola bater no canto direito da barra
        if pos[2] >= self.Barra_pos[0] and pos[0] <= self.Barra_pos[2]:
            # se a base da bola bater no topo da barra e
            # a base da bola bater na base da barra
            if pos[3] >= self.Barra_pos[1] and pos[3] <= self.Barra_pos[3]:
                # mude a velocidade em y para -3
                self.speedY = -3
                # torna o contador como global
                global count
                # adiciona um score ao contador
                count +=1
                # chama a funcao score
                score()

        # se a bola estiver dentro do canvas, continue movimentando ela
        if pos[3] <= self.canvas_height - ( border_size + highlight_size ):
            # chama a funcao draw em 10 milisegundos
            self.canvas.after(10, self.draw)
        else:
            # chama a funcao gameover
            game_over()
            # pega a variavel global lost
            global lost
            # define que o jogador perdeu
            lost = True


class Barra:
    # pega o canvas e uma cor
    def __init__(self, canvas, color):
        self.canvas = canvas
        # cria um retangulo da posicao 0, 0 ate length, 10 onde length e a largura e 10 a altura
        self.id = canvas.create_rectangle(0, 0, length, 10, fill=color)

        self.canvas_height = self.canvas.winfo_height()  # pega a altura da janela + a borda / highlight
        self.canvas_width = self.canvas.winfo_width()  # pega a largura da janela + a borda / highlight

        # move o retangulo ate a posicao 200 em x e 400 em y
        self.canvas.move(self.id, self.canvas_width / 2 - length / 2, 400)

        # define a velocidade em x como zero
        self.speedX = 0

        # chama a funcao move_left quando pressionar a tecla Left
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        # chama a funcao move_right quando pressionar a tecla Right
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    def draw(self):
        # movimenta a barra no eixo x
        self.canvas.move(self.id, self.speedX, 0)

        # pega a posicao da barra (x1, y1, x2, y2)
        self.pos = self.canvas.coords(self.id)

        # se o lado esquerdo da barra estiver no limite a velocidade em x fica em 0
        if self.pos[0] <= (border_size + highlight_size + 2):
            self.speedX = 0

        # se o lado direito da barra estiver no limite direito da janela a velocidade em x fica 0
        if self.pos[2] >= self.canvas_width - (border_size + highlight_size + 2):
            self.speedX = 0

        # pega a variavel global lost
        global lost

        # verifica se o jogador perdeu se nao, ele desenha a barra chamando a funcao draw a cada 10 milisegundos
        if lost == False:
            self.canvas.after(10, self.draw)

    # recebe um event e modifica a velocidade em x da barra
    def move_left(self, event):
        # se a posicao da barra for maior do que o limite esquerdo, ele muda a velocidade para ir para esquerda
        if self.pos[0] >= 0:
            self.speedX = -3

    # recebe um event e modifica a velocidade em x da barra
    def move_right(self, event):
        # se a posicao da barra for menor do que o limite direito, ele muda a velocidade para ir para a direita
        if self.pos[2] <= self.canvas_width:
            self.speedX = 3

# inicia o jogo
def start_game(event):
    # define duas variaveis globais
    global lost, count
    lost = False
    count = 0
    # atualiza o score
    score()
    # configura o text game para vazio
    canvas.itemconfig(game, text=" ")
    # da uma pausa de 1ms
    time.sleep(1)
    # desenha a barra
    Barra.draw()
    # desenha a bola
    Bola.draw()


# funcao para atualizar o valor dos pontos
def score():
    canvas.itemconfig(score_now, text="Pontos: " + str(count))

# muda o text game para Game Over
def game_over():
    canvas.itemconfig(game, text="Game over!")


# cria a barra com cor laranja
Barra = Barra(canvas, "orange")
# cria a bola com cor roxa
Bola = Bola(canvas, Barra, "purple")

# cria o texto do score
score_now = canvas.create_text(430, 20, text="Pontos: " + str(count), fill = "green", font=("Arial", 16))
# cria o texto de game (game over)
game = canvas.create_text(450, 300, text="Press any key to start", fill="white", font=("Arial", 20))

# verifica se algum botao for pressionado, se sim ele inicia o jogo
canvas.bind_all("<Button-1>", start_game)

# atualiza a tela
root.mainloop()



