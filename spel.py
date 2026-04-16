import tkinter as tk

root = tk.Tk()
root.title("Dinosauriespelet")
root.geometry("1280x720")
root.resizable(width=False, height=False)

canvas = tk.Canvas(root, width=800, height=480, bg="red")
canvas.pack(pady=70)

#images
ground_img = tk.PhotoImage(file="images/ground.png")



ground = canvas.create_image(0, 290, anchor="nw", image=ground_img)


root.mainloop()