from tkinter import *
from random import *

def dessinerGrille():
    #dessin de linges verticales
    for i in range(nbCasesX+1):
        can.create_line(i*largeur, 0, i*largeur, largeur*nbCasesY, fill=couleurLg)
    #dessin de linges  horizontales
    for i in range(nbCasesY+1):
        can.create_line(0, i*largeur, nbCasesX*largeur, i*largeur, fill=couleurLg)
def creatCellule(x, y, couleur):
    objG = can.create_rectangle(x*largeur, y*largeur, (x+1)*largeur, (y+1)*largeur, fill=couleur)
    return [objG, x, y, couleur]

def initialiserJeu():
    global repas
    #1-dessiner la grille
    dessinerGrille()
    #2-cree 5 cellules pour ke serpont
    #cree 5 cellules pour le serpent
    corps.append(creatCellule(6, 2, couleurTete))
    corps.append(creatCellule(5, 2, couleurCorps))
    corps.append(creatCellule(4, 2, couleurCorps))
    corps.append(creatCellule(3, 2, couleurCorps))
    corps.append(creatCellule(2, 2, couleurCorps))

    #3- cree  les obstacles
    for x in range(nbCasesX//4, 3*nbCasesX//4, 1):
        obstacle.append(creatCellule(x, nbCasesY//3,couleurObstacle))
        obstacle.append(creatCellule(x,2*nbCasesY//3,couleurObstacle))
    print(obstacle)
    #4-generation du repas
    repas = genererRepas()

def ChangerDirection(event):
    global direction
    if event.keysym =='Right' and direction!='Left':
        direction = 'Right'

    if event.keysym =='Left' and direction!='Right':
        direction = 'Left'

    if event.keysym =='Up' and direction!='Down':
        direction = 'Up'

    if event.keysym == 'Down' and direction!='Up':
        direction = 'Down'
    print(direction)


def SnakeUpdate():
    for cel in corps:
        can.coords(cel[0], cel[1]*largeur, cel[2]*largeur, (cel[1]+1)*largeur, (cel[2]+1)*largeur)


def move():
    global repas
    global play
    #1_ deplacer le corps
    for i in range(len(corps)-1, 0, -1):
        corps[i][1] = corps[i-1][1]
        corps[i][2] = corps[i-1][2]
    #2-calcul de la nouvelle position de la tete
    if direction == 'Right':
        corps[0][1] +=1
    if direction == 'Left':
        corps[0][1] -=1
    if direction == 'Down':
        corps[0][2] +=1
    if direction == 'Up':
        corps[0][2] -=1
    #3-cadrer la tete pour ne pas depacer les bords de canavas
    if corps[0][1] == nbCasesX:
        corps[0][1] = 0
    if corps[0][1] == -1:
        corps[0][1] = nbCasesX-1
    if corps[0][2] == nbCasesY:
        corps[0][2] = 0
    if corps[0][2] == -1:
        corps[0][2] = nbCasesY-1
    #4- tester si le serpent a mange ou non
    if corps[0][1]==repas[1] and corps[0][2]==repas[2]:
        can.delete(repas[0])
        repas=genererRepas()
        corps.append(creatCellule(corps[1][1], corps[1][2],couleurCorps))

    def game_over():
        can.delete(ALL)
        can.create_text(can.winfo_width() / 2,can.winfo_height() / 2,font=('consolas ', 70),text = 'GAME OVER',fill='red',tag='gameover ')
    fenetre.update()
    #5-test d'arret
    for cellule in obstacle:
        if cellule[1]==corps[0][1] and cellule[2]==corps[0][2]:
            game_over()
            play = -1
    for i in range(1,len(corps)):
            if corps[0][1]==corps[i][1] and corps[0][2]==corps[i][2]:
                game_over()
                play=-1

    if play == 1:
        SnakeUpdate()
        fenetre.after(200, move)

def genererRepas():


    x = randrange(nbCasesX)
    y = randrange(nbCasesY)
    return creatCellule(x, y, couleurRepas)
def start():
    global play
    if play==0:
        play=1
    move()
def pause():
    global play
    play=0
#---------programme principal
# Parametre de notre application
largeur ,nbCasesX ,nbCasesY = 20, 40, 20
couleurBg, couleurLg,couleurTete, couleurCorps, couleurRepas, couleurObstacle = 'black', 'gray', 'red', 'lightgreen', 'blue', 'yellow'
direction = 'Right' # 1:Right 2:Down 3:Left 4:Up

corps, repas = [], []
obstacle = []

play = 0
fenetre = Tk()


#declaration des composants
fenetre.title('Snake Game - UEMF - 24/10/2022')
b1 = Button(fenetre, text='start', width=25, height=2, bg='lightgray',command=start)
b2 = Button(fenetre, text='pause', width=25, height=2, bg='lightgray',command=pause)
label = Label(fenetre, text='Realise par Assia Jaroui')
can = Canvas(fenetre, width=largeur*nbCasesX, height=largeur*nbCasesY, bg=couleurBg)

#placer les composants dans la fentre
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
can.grid(row=1, column=0, columnspan=2)
label.grid(row=2, column=0, columnspan=2)

#initialiser le jeu
initialiserJeu()
move()
fenetre.bind('<Key>', ChangerDirection)

fenetre.mainloop()