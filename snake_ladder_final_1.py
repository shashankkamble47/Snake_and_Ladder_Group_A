# snake and ladder game
# made by me :)
# this is my first gui project!!

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from random import randint
import pygame
import time

#sound stuffs
class Sound:
    def __init__(self):
        pygame.mixer.init()
        #loading sounds from folder
        self.sounds = {
           "dice": pygame.mixer.Sound(r"C:\Users\shashank.kamble\OneDrive - VCTI\Desktop\Python\Snake_and_ladder_Final\data\roll_dice.mp3"),
            "snake": pygame.mixer.Sound(r"C:\Users\shashank.kamble\OneDrive - VCTI\Desktop\Python\Snake_and_ladder_Final\data\snake.wav"),
            "ladder": pygame.mixer.Sound(r"C:\Users\shashank.kamble\OneDrive - VCTI\Desktop\Python\Snake_and_ladder_Final\data\ladder.mp3"),
            "win": pygame.mixer.Sound(r"C:\Users\shashank.kamble\OneDrive - VCTI\Desktop\Python\Snake_and_ladder_Final\data\winner.wav"),
        }
    
    def dice_roll(self):
        self.sounds["dice"].play() #plays the dice sound
    
    def snake_bite(self):
        self.sounds["snake"].play()
    
    def ladder_up(self):
        self.sounds["ladder"].play()
    
    def winner(self):
        self.sounds["win"].play()  #winning sound!!


#player class for managing players
class Player:
    
    def __init__(self, num_players=4, player_names=None):
        self.num_players = num_players
        self.cnt_active = num_players #how many players still playing
        
        colors = ["red", "blue", "green", "yellow"] #player colors
        
        #making player list
        self.players = [
            {
                "name": player_names[i] if player_names else f"Player {i+1}",
                "color": colors[i], 
                "pos": 0,  #starting position
                "active": True
            }
            for i in range(num_players)
        ]
        
        self.turn = 0 #whose turn is it


# Board class - this is the main game board
class Board:
    
    def __init__(self):
        #board settings
        self.offset_x = 40
        self.offset_y = 40
        self.sepration_x = 60  #space between cells
        self.sepration_y = 60
        
        # snakes dictionary (head: tail)
        self.snakes = {
            16: 7, 59: 17, 63: 19, 67: 30, 
            87: 24, 93: 69, 95: 75, 99: 77
        }
        
        #ladders dictionary (bottom: top)
        self.ladders = {
            9: 27, 18: 37, 25: 54, 28: 51,
            56: 64, 68: 88, 76: 97, 79: 100
        }
    
    def get_coordinates(self, pos):
        # converts position number to x,y coordinates
        if pos == 0:
            return self.offset_x, self.offset_y + 9 * self.sepration_y
        
        row = (pos - 1) // 10
        col = (pos - 1) % 10
        
        #alternating rows (snake pattern!)
        if row % 2 == 1:
            col = 9 - col
        
        x = self.offset_x + col * self.sepration_x
        y = (self.offset_y + 9 * self.sepration_y) - row * self.sepration_y
        
        return x, y
    
    def show_ranking(self, ranking):
        #final ranking window
        rank_win = tk.Toplevel(root)
        rank_win.title("🏆 Final Ranking")
        rank_win.geometry("300x350")
        rank_win.resizable(False, False)
        
        tk.Label(
            rank_win, 
            text="Final Player Ranking",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        #showing all players ranks
        for idx, (color, player_name) in enumerate(ranking, start=1):
            tk.Label(
                rank_win,
                text=f"{idx}. {player_name}",
                font=("Arial", 14),
                fg=color
            ).pack(pady=3)
        
        tk.Button(
            rank_win, 
            text="Close Game", 
            font=("Arial", 12, "bold"),
            command=root.destroy, 
            bg="lightgray"
        ).pack(pady=15)
    
    def play_turn(self):
        #main game logic!!!
        
        button.config(state="disabled") #disable button so cant click twice
        
        s.dice_roll() #play sound
        time.sleep(0.1)
        dice = randint(1, 6) #roll dice!
        
        #update dice label
        dice_label.config(text=f"🎲 Dice: {dice}", font=("Arial", 18, "bold"))
        
        #get current player
        i = p.turn % p.num_players
        while not p.players[i]["active"]:
            p.turn += 1
            i = p.turn % p.num_players
        
        score = p.players[i]["pos"]
        color = p.players[i]["color"]
        player_name = p.players[i]["name"]
        msg = f"🎲 {player_name} rolled a {dice}."
        
        #update current player display
        current_player_label.config(
            text=f"Current Turn: {player_name}",
            fg=color,
            font=("Arial", 14, "bold")
        )
        
        status_label.config(text=msg, fg=color)
        
        #check if going over 100
        if score + dice > 100:
            msg += " Cannot move beyond 100."
            status_label.config(text=msg, fg=color)
            p.turn += 1
            button.config(state="normal")
            return
        
        total = score + dice
        
        canvas.delete(f"player{i}") #remove old piece
        
        final_pos = total
        
        #check for snakes
        if total in self.snakes:
            s.snake_bite() #snake sound!
            final_pos = self.snakes[total]
            msg = f"🐍 Snake! {player_name}: {total} → {final_pos}"
            status_label.config(text=msg, fg=color)
            
        #check for ladders
        elif total in self.ladders:
            s.ladder_up()  #ladder sound
            final_pos = self.ladders[total]
            msg = f"🪜 Ladder! {player_name}: {total} → {final_pos}"
            status_label.config(text=msg, fg=color)
        
        p.players[i]["pos"] = final_pos #update position
        
        #draw piece on board
        x, y = self.get_coordinates(final_pos)
        
        #offset so players dont overlap completely
        offset_x = (i % 2) * 12 - 6
        offset_y = (i // 2) * 12 - 6
        
        canvas.create_oval(
            x + offset_x - 8, y + offset_y - 8, 
            x + offset_x + 8, y + offset_y + 8,
            fill=color, outline="black", tags=f"player{i}"
        )
        
        #check if won!!
        if final_pos == 100:
            s.winner() #play winning sound
            Ranking.append((color, player_name))
            msg = f"{player_name} is the winner! 🎉"
            p.players[i]["active"] = False
            p.cnt_active -= 1
            
            if p.cnt_active == 1: #game over
                button.config(state="disabled")
                msg = " 🎯 Game Over!"
                
                #add last player
                ranked_colors = [c for c, _ in Ranking]
                for j in range(p.num_players):
                    if p.players[j]["color"] not in ranked_colors:
                        Ranking.append((p.players[j]["color"], p.players[j]["name"]))
                        break
                
                root.after(500, lambda: self.show_ranking(Ranking))
        
        p.turn += 1 #next turn
        status_label.config(text=msg, fg=color)
        
        button.config(state="normal") #enable button again


#main program starts here
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("🎲 Snake and Ladder Game - Simplified")
    root.configure(bg="lightblue")
    
    Ranking = [] #for storing rankings
    
    #ask how many players
    num = simpledialog.askinteger(
        "Number of Players",
        "Enter number of players (2–4):",
        parent=root,
        minvalue=2,
        maxvalue=4
    )
    if not num:
        num = 2 #default to 2
    
    #get player names
    player_names = []
    for i in range(num):
        name = simpledialog.askstring(
            "Player Name",
            f"Enter name for Player {i+1}:",
            parent=root
        )
        if not name or name.strip() == "":
            name = f"Player {i+1}" #default name
        player_names.append(name.strip())
    
    #main container frame
    main_container = tk.Frame(root, bg="lightblue")
    main_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    #LEFT PANEL for controls
    left_panel = tk.Frame(main_container, bg="white", relief="ridge", bd=3, width=250)
    left_panel.pack(side="left", fill="y", padx=(0, 10))
    left_panel.pack_propagate(False)
    
    #title
    tk.Label(
        left_panel,
        text="🎮 GAME CONTROLS",
        font=("Arial", 16, "bold"),
        bg="darkblue",
        fg="white"
    ).pack(fill="x", pady=(0, 10))
    
    #current turn section
    current_player_frame = tk.LabelFrame(
        left_panel,
        text="Current Turn",
        font=("Arial", 12, "bold"),
        bg="white"
    )
    current_player_frame.pack(fill="x", padx=10, pady=10)
    
    current_player_label = tk.Label(
        current_player_frame,
        text="Waiting to start...",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="blue"
    )
    current_player_label.pack(pady=10)
    
    #dice display section
    dice_frame = tk.LabelFrame(
        left_panel,
        text="Dice Roll",
        font=("Arial", 12, "bold"),
        bg="white"
    )
    dice_frame.pack(fill="x", padx=10, pady=10)
    
    dice_label = tk.Label(
        dice_frame,
        text="🎲 Dice: -",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="orange"
    )
    dice_label.pack(pady=10)
    
    #roll button
    button = tk.Button(
        left_panel,
        text="🎲 ROLL DICE",
        font=("Arial", 14, "bold"),
        bg="orange",
        fg="white",
        activebackground="darkorange",
        command=lambda: b.play_turn()
    )
    button.pack(fill="x", padx=10, pady=10)
    

    # #bottom status bar
    # bottom_frame = tk.Frame(left_panel, bg="lightgray", relief="ridge", bd=2,height=50)
    # bottom_frame.pack(fill="x", padx=10, pady=10)
    
    status_label = tk.Label(
        left_panel,
        text="🎮 Welcome to Snake and Ladder!",
        font=("Arial", 14),
        bg="lightgray",
        height=5,
        wraplength=200,
        justify="center"
    )
    status_label.pack(side="top", padx=5, pady=5)
    


    #RIGHT PANEL for board
    right_panel = tk.Frame(main_container, bg="lightblue")
    right_panel.pack(side="right", fill="both", expand=True)
    
    board_container = tk.Frame(right_panel, bg="white", relief="ridge", bd=3)
    board_container.pack()
    
    #load board image
    img = Image.open(r"C:\Users\shashank.kamble\OneDrive - VCTI\Desktop\Python\Snake_and_ladder_Final\data\snake_ladder.png")
    photo = ImageTk.PhotoImage(img)
    
    canvas = tk.Canvas(
        board_container,
        width=photo.width(),
        height=photo.height()
    )
    canvas.pack()
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    
    
    
    #initialize everything
    s = Sound() #sound system
    b = Board() #board
    p = Player(num_players=num, player_names=player_names) #players
    
    #start game loop
    root.mainloop()
