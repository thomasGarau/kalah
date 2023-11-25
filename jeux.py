import os
import json
class KalahGame:
    def __init__(self):
        # Initialize the game board
        self.board = [0] + [3] * 6 + [0] + [3] * 6
        self.level = None
        #0 sud 1 nord
        self.player_side = None
        self.computer_side = None
        self.player_khala = None
        self.computer_khala = None
       
    def display_board(self):
        #clear the user terminal 
        os.system('cls')
        # Display the board
        print("  ", "  ".join(map(str, self.board[1:7])))
        print(self.board[0], " " * 17, self.board[7])
        print("  ", "  ".join(map(str, self.board[8:14])))

    def end_game(self):
        # End the game and collect remaining seeds
        self.board[0] += sum(self.board[1:7])
        self.board[7] += sum(self.board[8:14])
        for i in range(1,14):
            if (i != 7):
                self.board[i] = 0

    def is_game_over(self):
        # The game is over when one side of the board is empty
        return sum(self.board[1:7]) == 0 or sum(self.board[8:14]) == 0

    def get_winner(self):
        # Determine the winner based on the number of seeds in Kalahs
        if self.player_khala == self.computer_khala:
            return "Egalité !"
        if self.player_khala > self.computer_khala:
            return "Vous avez gagné !"
        else:
            return "L'ordinateur a gagné !"
        
    def selectHole(self):
        while True:
            min_hole = 1 if self.player_side == 0 else 8
            max_hole = 6 if self.player_side == 0 else 13
            caseNumber = int(input(f"choisisser une case en saisisant un nombre compris entre {min_hole} et {max_hole} (de gauche a droite)"))
            if not(min_hole <= caseNumber <= max_hole):
                print("case invalide")
            else: 
                return caseNumber
            
    def move(self, kalah, enemy_kalah, selected_hole):
        marbles = self.board[selected_hole]
        self.board[selected_hole] = 0
        #on ajoute 1 pour que i commence à 1
        deplacement = selected_hole
        while marbles > 0:
            #determine la case dans lequel semé une graine
            if deplacement == 0:
                deplacement = 8
            elif deplacement == 13:
                deplacement = 7
            else : 
                if 0 < deplacement < 8:
                    deplacement -=1
                else : 
                    deplacement +=1

            #si la case est le kalah de l'adversaire ou la case initalement choisi on passe
            if(deplacement == enemy_kalah or deplacement == selected_hole):
                continue
            self.board[(deplacement)] += 1
            marbles -= 1
            #si dernier tours
            if(marbles == 0):
                #si la dernière bille est placée dans son kalah le joueur rejoue
                if(deplacement == kalah):
                    self.display_board()
                    print("Vous rejouez")
                    self.move(kalah, enemy_kalah, self.selectHole())
                #si la case avait une ou deux billes le joueur prend les billes dans sont kalah
                elif(1 < self.board[deplacement] < 4):
                    self.board[kalah] += self.board[deplacement]
                    self.board[deplacement] = 0
                    j = 1
                    while True:
                        #recule d'une case à chaque fois que la case contient 1 ou 2 billes et les ajoute au kalah du joueur
                        if(deplacement - j == 7):
                            deplacement = 0
                            j = 0
                        elif(deplacement + j == 7):
                            deplacement = 13
                            j = 0
                        deplacementJ = deplacement + j if 0 <= deplacement + j < 7 else deplacement - j 
                        if(deplacementJ == kalah or deplacementJ == enemy_kalah):
                            j += 1
                            continue
                        if (1 < self.board[deplacementJ] < 4): 
                            self.board[kalah] += self.board[deplacementJ]
                            self.board[deplacementJ] = 0
                            j += 1
                        else : 
                            break
    
    def computer_move(self):
        return 1 if self.computer_side == 0 else 8

    def start(self):
        self.display_board()
        while True:
            
            self.move(self.player_khala, self.computer_khala, self.selectHole())
            if self.is_game_over():
                break  

            self.move(self.computer_khala, self.player_khala, self.computer_move())
            if self.is_game_over():
                break

            self.display_board()

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
            "player_side": self.player_side,
            "computer_side": self.computer_side,
            "player_khala": self.player_khala,
            "computer_khala": self.computer_khala
        }
        # Sauvegarder dans un fichier
        with open(filename, 'w') as file:
            json.dump(game_state, file)
        print("Jeu sauvegardé !")

    def load_game(self, board, level, player_side, computer_side, player_khala, computer_khala):
        self.board = board
        self.level = level
        self.player_side = player_side
        self.computer_side = computer_side
        self.player_khala = player_khala
        self.computer_khala = computer_khala
    
    def set_game(self, level, player_side):
        self.level = level
        #0 sud 1 nord
        self.player_side = player_side
        self.computer_side = 0 if player_side == 1 else 1
        self.player_khala = 0 if player_side == 0 else 7
        self.computer_khala = 7 if player_side == 0 else 0

def initalize_game(): 
    while True:
        game = KalahGame()
        #pour reprendre une partie sauvegarder
        if (input("souhaiter vous reprendre la dernière partie") == "O"):
            board, level, player_side, computer_side, player_khala, computer_khala = load_JSON()
            game.load_game(board, level, player_side, computer_side, player_khala, computer_khala)
        else :
            #choisir le side
            side = int(input("choisisser votre side (0 nord ou 1 sud)"))
            #choisir le niveau de difficulté
            level = int(input("choisisser votre niveau de difficulté (1, 2 ou 3)"))
            game.set_game(level, side)
        game.start()
        if input("Voulez vous rejouer ? (O/N)") == "N":
            break

def load_JSON(filename="kalah_save.json"):
    # Charger le jeu depuis un fichier
    with open(filename, 'r') as file:
        game_state = json.load(file)
    return game_state["board"], game_state["level"], game_state["side"], game_state["player_khala"], game_state["computer_khala"]

def minMax():
    #à faire
    return
    
initalize_game()


