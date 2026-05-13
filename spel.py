import tkinter as tk
from random import randint
from random import choice

#Score
#--------------------------------------------------------------------------------

def update_score():
    global score_label
    global score
    global blink
    global starting

    if starting: #om spelet restartar så ska scoren återställas
        score = 0
        starting = False #det är här som starting blir false för att det är update_score() som kallas sist

    if is_game_over:
        return

    score += 1
    score_label["text"] = f"{score:05}" #updaterar score_label

    if score % 100 == 0: #efter varje 100 score kommer det att blinka
        blink = 1
        score_blinking()

    score_label.after(100, update_score)

def score_blinking():
    global score_label
    global blink

    if blink < 9: #gör så att det blinkar 4 gånger, varannan gång
        if blink % 2 == 0: #om blink är jämt
            score_label.place(x=720, y=2) #syns
        else:
            score_label.place_forget() #om blink är ojämt, syns inte
        blink += 1
    else:
        return
    
    root.after(250, score_blinking)

#--------------------------------------------------------------------------------

#Kaktusar/fåglar och nudda kaktus/fågel och fågelanimation
#--------------------------------------------------------------------------------

def create_enemy(): #skapar kaktusar/fåglar (båda heter cactus...)
    global cactus
    global starting
    global is_game_over
    global which_cactus
    global cactus_x_pos

    if starting: #gör så att det inte blir flera kaktusar, så om man restartar tas den kaktus som är kvar bort innan spelet börjar
        canvas.delete(cactus)

    cactus_list = [cactus_1_img, cactus_2_img, cactus_3_img, cactus_4_img, bird_1_img]
    which_cactus = choice(cactus_list) #väljer vilken kaktus det ska vara eller fågel
    cactus_x_pos = randint(750, 850) #för att det ska bli lite mer variation

    if which_cactus == cactus_4_img:
        cactus = canvas.create_image(cactus_x_pos, player_y_pos + 31, anchor="nw", image=which_cactus) #cactus 4 är inte lika hög så den måste vara längre ner för att inte vara i luften
    else:
        cactus = canvas.create_image(cactus_x_pos, player_y_pos, anchor="nw", image=which_cactus)
    
    move_enemy()


def move_enemy(): #flyttar enemies
    global cactus
    global is_game_over
    global which_cactus
    global cactus_x_pos
    global bird_animation_num

    #om man nuddar kaktusen/fågeln
    if canvas.coords(cactus)[0] <= canvas.coords(player)[2] and canvas.coords(player)[3] >= canvas.coords(cactus)[1] + 30: #+ 30 för att man ska kunna nudda pyttelite längst upp, så att det blir lättare
        is_game_over = True
        game_over()
        return

    #fågelanimation, funkar på samma sätt som dinoanimationen, fast långsammare
    if which_cactus == bird_1_img: #om det är en fågel så ska det vara en animation
        canvas.delete(cactus) #tar bort fågeln
        if bird_animation_num >= 400:
            cactus = canvas.create_image(cactus_x_pos, player_y_pos, anchor="nw", image=bird_2_img) #gör en ny på nya positionen
            if bird_animation_num >= 800: #om båda bilderna ska vara lika länge måste det här värdet vara dubbelt så stort som det andra
                bird_animation_num = 0
        else:
            cactus = canvas.create_image(cactus_x_pos, player_y_pos, anchor="nw", image=bird_1_img) #gör en ny på nya positionen
        
        bird_animation_num += 30
    else:
        canvas.move(cactus, enemy_speed, 0) #om det är en kaktus så ska den bara flytta sig utan animation


    if canvas.coords(cactus)[0] < -100: #om kaktusen/fågeln har gått över hela skärmen
        canvas.delete(cactus)
        create_enemy()
        return

    cactus_x_pos += enemy_speed #måste flytta fågeln på det här sättet istället för move, eftersom att man tar bort fågeln och gör sedan en ny och då måste den veta på vilken position den ska skapa den nya

    root.after(10, move_enemy)


#--------------------------------------------------------------------------------

#game over
#--------------------------------------------------------------------------------

def game_over():
    global is_game_over

    #visar game over texten och restartknappen
    game_over_text.place(x=210, y=100)
    restart_button.place(x=364, y=200)

    if is_game_over:
        root.unbind("<space>") #gör så att man inte hoppar på space längre
        root.bind("<space>", restart) #man restartar istället på space
    else: #när det inte längre är game over
        game_over_text.place_forget() #tar bort game over texten och restartknappen
        restart_button.place_forget()
        root.unbind("<space>") #måste göra "unbind" så att inte båda grejerna händer när man trycker space
        root.bind("<space>", jump) #nu hoppar man på space och inte restart
        return
    
    root.after(10, game_over)


#--------------------------------------------------------------------------------

#Start, restart
#--------------------------------------------------------------------------------

def restart(event):
    global is_game_over

    is_game_over = False
    start_game() #startar om spelet
    return

def start_game():
    global starting

    starting = True
    #kallar funktionerna som kallas i början igen
    dino_move()
    create_cloud()
    ground_move()
    create_enemy()
    update_score()
    return

#--------------------------------------------------------------------------------

#dinosaurie animation
#--------------------------------------------------------------------------------

def dino_move(): #flyttar dinosaurien
    global dino
    global animation_num
    global starting
    
    if is_game_over:
        canvas.delete(dino)
        dino = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_dead_img)
        return
    
    if starting:
        canvas.delete(dino)
        dino = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_run_1_img)


    canvas.delete(dino) #tar bort dino varje 10 millisekunder, sedan ersätts den med en ny på en ny position
    
    if not is_jumping:
        #båda bilderna kommer vara lika länge
        if animation_num >= 200: #om animation_num är mer än 200 tills det är 400, kommer det vara run 1
            dino = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_run_1_img) #gör en ny dino på hitboxens position
            if animation_num >= 400: #återställs
                animation_num = 0
        else: #om animation_num är mindre än 200 kommer det vara run 2
            dino = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_run_2_img) #gör en ny dino på hitboxens position
    else: #om man hoppar ska den inte springa samtidigt
        dino = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_idle_jump_img) #gör en ny dino på hitboxens position


    animation_num += 30 # +30 varje 10 millisekunder

    root.after(10, dino_move)

#--------------------------------------------------------------------------------

#ground animation
#--------------------------------------------------------------------------------

def ground_move(): #de gör samma sak men de börjar på olika x
    global ground
    global ground_2

    if starting: #återställer
        canvas.delete(ground)
        canvas.delete(ground_2)
        ground = canvas.create_image(0, ground_level, anchor="nw", image=ground_img)
        ground_2 = canvas.create_image(800, ground_level, anchor="nw", image=ground_img)

    if is_game_over:
        return

    if canvas.coords(ground)[0] < -800: #när den har gått över hela skärmen...
        canvas.delete(ground) #...så ska den tas bort...
        ground = canvas.create_image(800, ground_level, anchor="nw", image=ground_img) #..och sen görs en ny på andra sidan skärmen
    else:
        canvas.move(ground, enemy_speed, 0)

    #samma sak
    if canvas.coords(ground_2)[0] < -800:
        canvas.delete(ground_2)
        ground_2 = canvas.create_image(800, ground_level, anchor="nw", image=ground_img)
    else:
        canvas.move(ground_2, enemy_speed, 0)

    root.after(10, ground_move)

#--------------------------------------------------------------------------------

#molnanimation
#--------------------------------------------------------------------------------

def create_cloud():
    global cloud_list

    if starting:
        for cloud in cloud_list:
            canvas.delete(cloud)
        cloud_list.clear()
            


    cloud_1 = canvas.create_image(randint(800, 1500), randint(0, 150), anchor="nw", image=cloud_img)
    cloud_2 = canvas.create_image(randint(800, 1500), randint(0, 150), anchor="nw", image=cloud_img)
    cloud_3 = canvas.create_image(randint(800, 1500), randint(0, 150), anchor="nw", image=cloud_img)
    cloud_list = [cloud_1, cloud_2, cloud_3]

    move_cloud()
    return

def move_cloud():

    if is_game_over:
        return

    for cloud in cloud_list: #för varje moln i listan
        canvas.move(cloud, (enemy_speed/2), 0) #flyttas hälften så snabbt som enemy
        if canvas.coords(cloud)[0] < -100: #när den gått över skärmen
            canvas.delete(cloud) #tas bort från canvasen
            cloud_list.remove(cloud) #tas bort från listan
            
    
    if cloud_list == []: #om alla moln har gått över skärmen
        create_cloud() #börjar om | blir dock att det blir tre moln i omgångar, men man märker inte så mycket
        return
    
    root.after(10, move_cloud)

#--------------------------------------------------------------------------------

#Hoppa
#--------------------------------------------------------------------------------

def jump(event):
    global is_jumping
    global jump_height
    global jump_height_value

    if is_game_over:
        return

    if not is_jumping: #om man inte hoppar
        check_y_pos()
    else:
        return #om man hoppar kommer inget hända

def check_y_pos():
    global jump_height
    global jump_height_value
    
    if int(canvas.coords(player)[1]) > int(player_y_pos): #om koordinaten av y1 är mer (alltså längre ner) än den ursprungliga positionen som den har när den står på marken...
       canvas.move(player, 0, -0.1) #...kommer den att flyttas uppåt tills den är på den ursprungliga positionen, det här behövs eftersom om man skulle spamhoppa så skulle markpositionen kunna ändras lite hela tiden så att det blir fel efter ett tag och spelet slutar funka så bra
    elif int(canvas.coords(player)[1]) == int(player_y_pos): #canvas.coords(player)[1] är samma som y1, om koordinaten av y1 är samma som ursprungliga positionen (om den står på marken)
        jump_height = jump_height_value #återställer jump_height
        move_up()
        return #gör att loopen slutar
    root.after(10, check_y_pos) #varje 10 millisekunder börjar check_y_pos om som en loop, om man inte gör det här kommer check_y_pos bara hända en gång

def move_up(): #själva hoppet
    global is_jumping
    global jump_height
    global gravity
    
    is_jumping = True
    
    canvas.move(player, 0, -jump_height) #spelaren flyttas jump_height uppåt varje gång det loopar, när jump_height blir negativ flyttas spelaren neråt istället
    jump_height -= gravity #jump_height blir mindre och mindre och blir även negativ | först skjiljer sig jump_height mycket från 0 och då flyttas den snabbt uppåt sen blir det mindre och mindre tills det vänder och blir mer och mer negativt | det här gör att det ser mer ut som ett faktiskt hopp än att den flyttas med jämn hastighet
    if canvas.coords(player)[1] >= player_y_pos: #om man nuddar marken igen
        is_jumping = False
        return #gör att loopen slutar

    root.after(10, move_up) #loopar varje 10 millisekunder

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

root = tk.Tk()
root.title("Dinosauriespelet")
root.geometry("1280x720")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, width=800, height=480, bg="white", highlightthickness=0)
canvas.pack(pady=70)

#variables
#--------------------------

ground_level = 290
jump_height_value = 11
jump_height = jump_height_value
gravity = 0.5
is_jumping = False
enemy_speed = -8
score = 0
animation_num = 0
bird_animation_num = 0
cloud_list = []
is_game_over = False
starting = False

#x1=player_x_pos, y1=player_y_pos, x2=player_width, y2=player_height
#hitboxens koordinater och storlek
player_x_pos = 50
player_y_pos = ground_level-70 # 70px högre upp än ground_level
player_width = player_x_pos + 55
player_height = player_y_pos + 93

#---------------------------

#imports
ground_img = tk.PhotoImage(file="images/ground.png")
dino_idle_jump_img = tk.PhotoImage(file="images/idle-jump.png")
dino_run_1_img = tk.PhotoImage(file="images/run_1.png")
dino_run_2_img = tk.PhotoImage(file="images/run_2.png")
dino_dead_img = tk.PhotoImage(file="images/dead.png")
cactus_1_img = tk.PhotoImage(file="images/kaktus_1.png")
cactus_2_img = tk.PhotoImage(file="images/kaktus_2.png")
cactus_3_img = tk.PhotoImage(file="images/kaktus_3.png")
cactus_4_img = tk.PhotoImage(file="images/kaktus_4.png")
cloud_img = tk.PhotoImage(file="images/cloud.png")
bird_1_img = tk.PhotoImage(file="images/fågel_1.png")
bird_2_img = tk.PhotoImage(file="images/fågel_2.png")
game_over_img = tk.PhotoImage(file="images/game_over.png")
restart_img = tk.PhotoImage(file="images/restart_button.png")


#images
ground = canvas.create_image(0, ground_level, anchor="nw", image=ground_img) #övre vänstra hörnet är koordinaterna (0, ground_level)
ground_2 = canvas.create_image(800, ground_level, anchor="nw", image=ground_img) #den ena börjar på x=0 och den andra x=800
player = canvas.create_rectangle(player_x_pos, player_y_pos, player_width, player_height, width=0) #hitboxen, är lite smalare än dinosaurien | x1, y1, x2, y2 | player_x_pos och player_y_pos är övre vänstra hörnet, player_width och player_height är undre högra hörnet | width=0 är att det inte är en border runt
dino = canvas.create_image(player_x_pos-10, player_y_pos, anchor="nw", image=dino_idle_jump_img) # dinosaurien är 10px åt vänster om hitboxen


#Labels
score_label = tk.Label(canvas, text="", font=("Arial", 20), bg="white")
score_label.place(x=720, y=2)
game_over_text = tk.Label(canvas, image=game_over_img, bg="white")
restart_button = tk.Label(canvas, image=restart_img, bg="white")


#bind
root.bind("<space>", jump) #om man trycker "space" kommer funktionen jump börja


dino_move()
create_cloud()
ground_move()
create_enemy()
update_score()
root.mainloop()