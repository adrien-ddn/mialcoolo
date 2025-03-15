import random
import tkinter as tk
from tkinter import messagebox, font, PhotoImage

class Mialcoolo:
    def __init__(self, root):
        self.root = root
        self.root.title("Mialcoolo")
        self.root.geometry("1360x720")
        self.root.configure(bg="#ffe1f5")
    
        self.players = []
        self.history = []
        self.current_index = -1

        # Définition des boutons comme attributs de la classe
        self.btn_prev = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="⬅", width=3, height=1, command=self.previous_phrase)
        self.btn_next = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="➡", width=3, height=1, command=self.next_phrase)
        self.btn_stop = tk.Button(self.root, bg="red", fg="white", text="X", font=("Arial", 24, "bold"), width=3, height=1, command=self.start_screen)
    
        self.start_screen()

    
    def start_screen(self):
        self.clear_window()
        try:
            self.bg_image = PhotoImage(file="mnt/data/start.png")
        except tk.TclError:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")
            return
        
        self.canvas = tk.Canvas(root, width=1360, height=720)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        
        self.start_button = tk.Button(root, text="Start", font=("Times New Roman", 96, "bold"), bg="#ffe1f5", fg="black", command=self.add_players_screen)
        self.canvas.create_window(680, 360, window=self.start_button)
    
    def add_players_screen(self):
        self.clear_window()

        # Chargement de l'image de fond
        try:
            self.image = PhotoImage(file="mnt/data/players.png")
        except tk.TclError:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")
            return

        # Création du canvas (pour l'image et les joueurs)
        canvas = tk.Canvas(self.root, width=1360, height=720, bg="#ffe1f5", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(680, 360, image=self.image)

        # Création du cadre pour les joueurs (positionné sur le canvas)
        self.players_frame = tk.Frame(canvas, bg="#ffe1f5")
        canvas.create_window(500, 400, window=self.players_frame)  # Centre les joueurs sur l’image

        # Création du cadre des boutons (toujours visible)
        self.btn_frame = tk.Frame(canvas, bg="#3c8c97")
        canvas.create_window(760, 690, window=self.btn_frame)  # Position sous les joueurs

        # Ensuite, vos boutons
        tk.Button(self.btn_frame, text="Add Player", command=self.add_new_player, bg="#3c8c97").pack(side=tk.LEFT, padx=10)
        tk.Button(self.btn_frame, text="Start", command=self.start_game, bg="#3c8c97").pack(side=tk.LEFT, padx=10)


        # Affichage des joueurs sur l'image
        self.update_players_display()

    def update_players_display(self):
        for widget in self.players_frame.winfo_children():
            widget.destroy()
    
        for idx, player in enumerate(self.players):
            frame = tk.Frame(self.players_frame, bg="#ffe1f5", width=800, height=30, bd=2, relief=tk.RIDGE)
            frame.pack(fill=tk.X, pady=3)
    
            # Utiliser anchor='w' pour aligner le texte à gauche
            tk.Label(frame, text=player, font=("Arial", 12), bg="#ffe1f5", anchor='w').pack(side=tk.LEFT, padx=10)

            tk.Button(frame, text="X", bg="#ffe1f5", command=lambda p=player: self.remove_player(p)).pack(side=tk.RIGHT, padx=5)


        # Assurer que le cadre des boutons reste visible
        self.btn_frame.lift()

    
    def add_new_player(self):
        if len(self.players) < 12:
            new_player = self.prompt_for_player()
            if new_player and new_player not in self.players:
                self.players.append(new_player)
                self.update_players_display()
            elif new_player in self.players:
                messagebox.showwarning("Erreur", "Ce joueur est déjà ajouté.")
        else:
            messagebox.showwarning("Erreur", "Le nombre maximum de joueurs est atteint.")
    
    def remove_player(self, player):
        self.players.remove(player)
        self.update_players_display()
    
    def prompt_for_player(self):
        popup = tk.Toplevel(self.root)
        popup.title("Ajouter un joueur")
        tk.Label(popup, text="Entrez le prénom du joueur :").pack(pady=10)
        entry = tk.Entry(popup)
        entry.pack(pady=5)
        
        def confirm():
            self.new_player_name = entry.get().strip()
            popup.destroy()
        
        tk.Button(popup, text="Ajouter", command=confirm).pack(pady=10)
        self.root.wait_window(popup)
        return getattr(self, 'new_player_name', None)
    
    def start_game(self):
        if not self.players:
            messagebox.showwarning("Erreur", "Ajoutez des joueurs avant de commencer.")
            return

        self.clear_window()

        self.image = PhotoImage(file="mnt/data/phrase.png")  # Charger l'image fournie
        self.canvas = tk.Canvas(self.root, width=1360, height=720, bg="#ffe1f5", highlightthickness=0)
        self.canvas.pack()

        self.canvas.create_image(680, 360, image=self.image)  # Centrer l'image

        self.phrase_font = font.Font(family="Baguet Script", size=40, weight="bold")
        self.names_label = self.canvas.create_text(560, 240, text="", font=self.phrase_font, fill="black", width=800)
        self.action_label = self.canvas.create_text(720, 480, text="", font=self.phrase_font, fill="black", width=800,anchor="center")

        self.btn_prev = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="⬅", width=3, height=1, command=self.previous_phrase)
        self.btn_next = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="➡", width=3, height=1, command=self.next_phrase)
        self.btn_stop = tk.Button(self.root, bg="red", fg="white", text="X", font=("Arial", 24, "bold"), width=3, height=1, command=self.start_screen)

        # Positions ajustées pour être en haut à droite
        self.canvas.create_window(100, 360, window=self.btn_prev, anchor="ne")  # "Précédent"
        self.canvas.create_window(1260, 360, window=self.btn_next, anchor="ne")  # "Suivant"
        self.canvas.create_window(1310, 50, window=self.btn_stop, anchor="ne")  # "Arrêter la partie"
    
    def get_random_phrase(self):
        chance = random.randint(1, 100)

        if chance <= 88:
            with open("mnt/data/phrases.txt", "r", encoding="utf-8") as file:
                phrases = file.readlines()

            phrases = [phrase.strip() for phrase in phrases]
    
            if len(self.players) > 1:
                player1, player2 = random.sample(self.players, 2)
            else:
                player1 = random.choice(self.players)
                player2 = player1
    
            phrase = random.choice(phrases)
            full_phrase = phrase.replace("{player1}", player1).replace("{player2}", player2).replace("{n}",str(random.randint(1,3)))
            if "," in full_phrase:
                parts = full_phrase.split(",", 1)
                part1 = parts[0]
                part2 = parts[1]
            else:
                words = full_phrase.split()
                mid = len(words) // 2
                part1 = " ".join(words[:mid])
                part2 = " ".join(words[mid:])


            image_file = "phrase.png"

        else:
            virus_type = "individuel" if random.random() < 0.75 else "collectif"
            file_name = "mnt/data/virus_perso.txt" if virus_type == "individuel" else "mnt/data/virus_collectif.txt"
        
            with open(file_name, "r", encoding="utf-8") as file:
                viruses = file.readlines()

            if virus_type=="individuel":
                if len(self.players) > 1:
                    player1, player2 = random.sample(self.players, 2)
                else:
                    player1 = random.choice(self.players)
                    player2 = player1

                brut = random.choice(viruses).strip()
                part1 = brut.replace("{player1}", player1).replace("{player2}", player2)
                duree = random.randint(3,6)
                part1 = part1 + f" pendant {duree} tours"
            else :
                part1 = random.choice(viruses).strip()
                player1 = player2 = ""
            part2 = ""
            image_file = "virus.png"

        return player1, player2, part1, part2, image_file  # On retourne aussi l'image # Ensure it always returns four values


    def update_display(self, image_file, part1, part2):
        self.clear_window()

        try:
            self.image = PhotoImage(file=f"mnt/data/{image_file}")
        except tk.TclError:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")
            return

        self.canvas = tk.Canvas(self.root, width=1360, bg="#ffe1f5", height=720, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(650, 360, image=self.image)

        if image_file == "virus.png":
            self.virus_frame = tk.Frame(self.root, bg="#ff89d6", padx=0, pady=0)
            self.canvas.create_window(680, 420, window=self.virus_frame, anchor="center")

            tk.Label(
                self.virus_frame, text=part1, font=("Arial", 18, "bold"), 
                bg="#ff89d6", fg="white", wraplength=500
            ).pack()
        else:
            self.phrase_font = font.Font(family="Baguet Script", size=40, weight="bold")

            # Affichage séparé des phrases
            self.canvas.create_text(560, 240, text=part1, font=self.phrase_font, fill="black", width=800, anchor="center")
            self.canvas.create_text(720, 480, text=part2, font=self.phrase_font, fill="black", width=800, anchor="center")

            # Vérifier si la phrase contient "gorgées" et afficher l'image et le nombre
            if "gorgées" in part1 or "gorgées" in part2:
                import re
                match = re.search(r"(\d+) gorgées", part1) or re.search(r"(\d+) gorgées", part2)
                if match:
                    gorgées_count = match.group(1) + " gorgées"
                    try:
                        self.gorgées_image = PhotoImage(file="mnt/data/gorgees.png")
                        self.canvas.create_image(5, 5, image=self.gorgées_image, anchor="nw")
                        self.canvas.create_text(110, 50, text=gorgées_count, font=("Arial", 14, "bold"), fill="black", anchor="nw")
                    except tk.TclError:
                        messagebox.showerror("Erreur", "Impossible de charger l'image des gorgées.")

        # Ajout des boutons
        self.btn_prev = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="⬅", width=3, height=1, command=self.previous_phrase)
        self.btn_next = tk.Button(self.root, bg="#22b14c", fg="white", font=("Arial", 28, "bold"), text="➡", width=3, height=1, command=self.next_phrase)
        self.btn_stop = tk.Button(self.root, bg="red", fg="white", text="X", font=("Arial", 24, "bold"), width=3, height=1, command=self.start_screen)

        self.canvas.create_window(100, 360, window=self.btn_prev, anchor="ne")
        self.canvas.create_window(1260, 360, window=self.btn_next, anchor="ne")
        self.canvas.create_window(1310, 50, window=self.btn_stop, anchor="ne")

    def next_phrase(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            player1, player2, part1, part2, image_file = self.history[self.current_index]
        else:
            player1, player2, part1, part2, image_file = self.get_random_phrase()
            self.history.append((player1, player2, part1, part2, image_file))
            self.current_index += 1

        # Appel correct d'update_display avec part1 et part2
        self.update_display(image_file, part1, part2)


    def previous_phrase(self):
        if self.current_index > 0:
            self.current_index -= 1
            player1, player2, part1, part2, image_file = self.history[self.current_index]
        
            # Appel correct à update_display avec les bonnes valeurs
            self.update_display(image_file, part1, part2)

    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Mialcoolo(root)
    root.mainloop()
