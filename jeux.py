import os
import json
class KalahGame:
    def __init__(self):
        # Initialize the game board
        self.board = [0] + [3] * 6 + [0] + [3] * 6
        self.level = None
        #0 sud 1 nord
        self.side = None
        self.player_khala = None
        self.computer_khala = None
       
    def display_board(self):
        #clear the user terminal 
        os.system('cls')
        # Display the board
        print("  ", "  ".join(map(str, self.board[0:6])))
        print(self.board[0], " " * 17, self.board[7])
        print("  ", "  ".join(map(str, self.board[7:13][::-1])))

    def end_game(self):
        # End the game and collect remaining seeds
        self.board[12] += sum(self.board[:6])
        self.board[13] += sum(self.board[6:12])
        for i in range(12):
            self.board[i] = 0

    def is_game_over(self):
        # The game is over when one side of the board is empty
        return sum(self.board[:6]) == 0 or sum(self.board[6:12]) == 0

    def get_winner(self):
        # Determine the winner based on the number of seeds in Kalahs
        if self.board[12] == self.board[13]:
            return "Egalité !"
        if self.board[12] > self.board[13] and self.side == 0:
            return "Vous avez gagné !"
        else:
            return "L'ordinateur a gagné !"
        
    def selectHole(self):
        while True:
            min_hole = 1 if self.side == 0 else 8
            max_hole = 6 if self.side == 0 else 13
            caseNumber = int(input(f"choisisser une case en saisisant un nombre compris entre {min_hole} et {max_hole} (de gauche a droite)"))
            if not(min_hole <= caseNumber <= max_hole):
                print("case invalide")
            else: 
                #on ajoute 6 pour tenir compte du side
                return caseNumber + 6 if self.side == 1 else caseNumber
            
    def player_move(self):
        selected_hole = self.selectHole()
        marbles = self.board[selected_hole]
        self.board[selected_hole] = 0
        for i in range(marbles):
            #determine la case dans lequel semé une graine
            deplacement = selected_hole - i if 0 <= selected_hole < 7 else 7 + abs(selected_hole - i) if selected_hole - i < 0 else 7 - (selected_hole + i) -13  if selected_hole + i > 13  else selected_hole + i 
            self.board[(deplacement)] += 1
            #si dernier tours
            if(i == marbles):
                #si la dernière billes et placé dans sont kalah le joueur rejoue
                if((deplacement == 0 and self.side == 0) or (deplacement == 7 and self.side == 1)):
                    self.player_move()
                #si la case avait une ou deux billes le joueur prend les billes dans sont kalah
                elif(1 < self.board[deplacement] < 4):
                    self.board[self.player_khala] += self.board[deplacement]
                    self.board[deplacement] = 0
                    j = 1
                    while True:
                        #recule d'une case à chaque fois que la case contient 1 ou 2 billes et les ajoute au kalah du joueur
                        deplacementJ = deplacement + j if 0 <= deplacement + j < 7 else deplacement - j if deplacement - j > 7 else 13 if deplacement + j == 7 else 0 if deplacement - j == 7 else None
                        if (0 < self.board[deplacementJ] < 3): 
                            self.board[self.player_khala] += self.board[deplacementJ]
                            self.board[deplacementJ] = 0
                            j += 1
                        else : 
                            break
    
    def computer_move(self):
        return

    def start(self):
        while True:
            self.display_board()

            self.player_move()
            if self.is_game_over():
                break  

            self.computer_move()
            if self.is_game_over():
                break
            
            if(input("souhaiter vous sauvegarder la partie ? (O/N)") == "O"):
                self.save_game()
                return
        self.end_game()
        print("plateau final :")
        self.display_board()
        print(self.get_winner())
    
    def save_game(self, filename="kalah_save.json"):
    # Créer un dictionnaire avec l'état du jeu
        game_state = {
            "board": self.board,
            "level": self.level,
            "side": self.side,
            "player_khala": self.player_khala,
            "computer_khala": self.computer_khala
        }
        # Sauvegarder dans un fichier
        with open(filename, 'w') as file:
            json.dump(game_state, file)
        print("Jeu sauvegardé !")

    def load_game(self, board, level, side, player_khala, computer_khala):
        self.board = board
        self.level = level
        self.side = side
        self.player_khala = player_khala
        self.computer_khala = computer_khala
    
    def set_game(self, level, side):
        self.level = level
        #0 sud 1 nord
        self.side = side
        self.player_khala = 0 if side == 0 else 7
        self.computer_khala = 7 if side == 0 else 0

def initalize_game(): 
    while True:
        game = KalahGame()
        #pour reprendre une partie sauvegarder
        if (input("souhaiter vous reprendre la dernière partie") == "O"):
            board, level, side, player_khala, computer_khala = load_game()
            game = game.load_game(board, level, side, player_khala, computer_khala)
        else :
            #choisir le side
            side = int(input("choisisser votre side (0 nord ou 1 sud)"))
            #choisir le niveau de difficulté
            level = int(input("choisisser votre niveau de difficulté (1, 2 ou 3)"))
            game.set_game(level, side)
        game.start()
        if input("Voulez vous rejouer ? (O/N)") == "N":
            break

def load_game(filename="kalah_save.json"):
    # Charger le jeu depuis un fichier
    with open(filename, 'r') as file:
        game_state = json.load(file)
    return game_state["board"], game_state["level"], game_state["side"], game_state["player_khala"], game_state["computer_khala"]

def minMax():
    #à faire
    return
    
initalize_game()


