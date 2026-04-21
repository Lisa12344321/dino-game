import tkinter as tk

def dino_move():
    global dino_idle_jump

    canvas.delete(dino_idle_jump) #tar bor dino_idle_jump
    dino_idle_jump = canvas.create_image(player_x_pos-10, canvas.coords(player)[1], anchor="nw", image=dino_idle_jump_img) #gör en ny din_idle_jump på hitboxens position

    root.after(10, dino_move)

def jump(event):
    global is_jumping
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



root = tk.Tk()
root.title("Dinosauriespelet")
root.geometry("1280x720")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, width=800, height=480, bg="red")
canvas.pack(pady=70)

#--------------------------

#variables
ground_level = 290
jump_height_value = 7
jump_height = jump_height_value
gravity = 0.2
is_jumping = False

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


#images
ground = canvas.create_image(0, ground_level, anchor="nw", image=ground_img) #övre vänstra hörnet är koordinaterna (0, ground_level)
player = canvas.create_rectangle(player_x_pos, player_y_pos, player_width, player_height, width=0) #hitboxen, är lite smalare än dinosaurien | x1, y1, x2, y2 | player_x_pos och player_y_pos är övre vänstra hörnet, player_width och player_height är undre högra hörnet | width=0 är att det inte är en border runt
dino_idle_jump = canvas.create_image(player_x_pos-10, player_y_pos, anchor="nw", image=dino_idle_jump_img) # dinosaurien är 10px åt vänster om hitboxen

#bind
root.bind("<space>", jump) #om man trycker "space" kommer funktionen jump börja

dino_move()
root.mainloop()