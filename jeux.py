import os
import json
class KalahGame:
    def __init__(self):
        # Initialize the game board
        self.board = [0] + [8] * 6 + [0] + [8] * 6
        self.level = None
        #0 sud 1 nord
        self.player_side = None
        self.computer_side = None
        self.player_khala = None
        self.computer_khala = None
       
    def display_board(self):
        #clear the user terminal 
        #os.system('cls')
        # Display the board
        print("  ", "  ".join(map(str, self.board[1:7])))
        print(self.board[0], " " * 17, self.board[7])
        print("  ", "  ".join(map(str, self.board[8:14])))

    def end_game(self, board):
        # End the game and collect remaining seeds
        board[0] += sum(board[1:7])
        board[7] += sum(board[8:14])
        for i in range(1,14):
            if (i != 7):
                board[i] = 0

    def is_game_over(self):
        # The game is over when one side of the board is empty
        return sum(self.board[1:7]) == 0 or sum(self.board[8:14]) == 0

    def get_winner(self):
        # Determine the winner based on the number of seeds in Kalahs
        if self.board[self.player_khala] == self.board[self.computer_khala]:
            return "Egalité !"
        if self.board[self.player_khala] > self.board[self.computer_khala]:
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
            
    def move(self, kalah, enemy_kalah, selected_hole, board, is_computer_call, depth):
        #dans le cas ou on est à un niveau de profondeur inférieur au treshold
        if(selected_hole == None):
            return
        marbles = board[selected_hole]
        board[selected_hole] = 0
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
            board[(deplacement)] += 1
            marbles -= 1
            #si dernier tours
            if(marbles == 0):
                #si la dernière bille est placée dans son kalah le joueur rejoue
                if(deplacement == kalah):
                    #si la fonction à été appeler au tour du joueur
                    if(not self.is_game_over()) : 
                        if(not is_computer_call):
                            self.display_board()
                            print("Vous rejouez")
                            self.move(kalah, enemy_kalah, self.selectHole(), board, False, depth -1)
                        else: 
                            self.move(kalah, enemy_kalah, self.computer_move(board, depth), board, True, depth -1)
                #si la case avait une ou deux billes le joueur prend les billes dans sont kalah
                elif(1 < board[deplacement] < 4):
                    board[kalah] += board[deplacement]
                    board[deplacement] = 0
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
                        if (1 < board[deplacementJ] < 4): 
                            board[kalah] += board[deplacementJ]
                            board[deplacementJ] = 0
                            j += 1
                        else : 
                            break
    
    def computer_move(self, computer_board, max_depth):
        bestMove = None
        bestValue = -float('inf')
        if (max_depth <= 0):
            return None
        for hole in range(self.computer_khala +1, self.computer_khala + 7):
            #coupe la branche si la case est vide
            if(computer_board[hole] == 0):
                continue
            #fait une copy du plateau pour ne pas modifier le plateau original
            boardCopy = computer_board[:]
            #simule un tour de jeu
            self.move(self.computer_khala, self.player_khala, hole, boardCopy, True, max_depth -1)       
            branche_value = self.alphaBeta(max_depth, boardCopy, False, -float('inf'), float('inf'))
            bestValue = max(bestValue, branche_value)
            if bestValue == branche_value:
                bestMove = hole
            return bestMove

    def minMax(self, depth, board, ourTurn):
        if(depth <= 0 or self.is_game_over()):
            return self.evaluate_board(board)
        #on prend le max pour soi meme
        if(ourTurn):
            bestValue = -float('inf')
            for hole in range(self.computer_khala +1, self.computer_khala + 7):
                if(board[hole] == 0):
                    continue
                boardCopy = board[:]
                self.move(self.computer_khala, self.player_khala, hole, boardCopy, True, depth -1)
                bestValue = max(bestValue, self.minMax(depth - 1, boardCopy, False))
            return bestValue
        #et le min pour l'adverssaire
        else:
            bestValue = float('inf')
            for hole in range(self.player_khala +1, self.player_khala + 7):
                if(board[hole] == 0):
                    continue
                boardCopy = board[:]
                self.move(self.player_khala, self.computer_khala, hole, boardCopy, True, depth -1)
                bestValue = min(bestValue, self.minMax(depth - 1, boardCopy, True))
            return bestValue
        
    def alphaBeta(self, depth, board, ourTurn, alpha, beta):
        if depth <= 0 or self.is_game_over():
            return self.evaluate_board(board)
        if ourTurn:  # Maximiseur
            bestValue = -float('inf')
            for hole in range(self.computer_khala + 1, self.computer_khala + 7):
                if board[hole] == 0:
                    continue
                boardCopy = board[:]
                self.move(self.computer_khala, self.player_khala, hole, boardCopy, True, depth - 1)
                value = self.alphaBeta(depth - 1, boardCopy, False, alpha, beta)
                bestValue = max(bestValue, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Élagage Beta
            return bestValue
        else:  # Minimiseur
            bestValue = float('inf')
            for hole in range(self.player_khala + 1, self.player_khala + 7):
                if board[hole] == 0:
                    continue
                boardCopy = board[:]
                self.move(self.player_khala, self.computer_khala, hole, boardCopy, True, depth - 1)
                value = self.alphaBeta(depth - 1, boardCopy, True, alpha, beta)
                bestValue = min(bestValue, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Élagage Alpha
        return bestValue
        
    def evaluate_board(self, board):
        if self.is_game_over():
            self.end_game(board)
            difference = board[self.computer_khala] - board[self.player_khala]
            if difference > 0:
                # Préférer gagner avec plus de graines
                return float('inf') + difference 
            elif difference < 0:
                # Minimiser la perte
                return float('-inf') + difference
            else:
                return 0  # Égalité
        else:
            kalah_difference = board[self.computer_khala] - board[self.player_khala]
            position_value = 0

            #on gagne des points à chaque fois qu'une case offre un avantage positionnel
            for hole in range(self.computer_khala + 1, self.computer_khala + 7):
                #si la case permet de rejouer
                if (board[hole] == (7 - hole)):
                    position_value += 5
                #si la case permet de prendre les graines est d'entrainer une reaction en chaine :
                #si la case à deux graines à offrir
                elif (board[hole] == 2):
                    position_value += 2
                #si elle en à trois
                elif (board[hole] == 3):
                    position_value += 2.5

            #on perd des points à chaque fois qu'une case offre un avantage stratégique à l'adversaire
            for enemy_hole in range(self.player_khala + 1, self.player_khala + 7):
                if (board[enemy_hole] == (7 - enemy_hole)):
                    position_value -= 5
                elif (board[enemy_hole] == 2):
                    position_value -= 2
                elif (board[enemy_hole] == 3):
                    position_value -= 2.5

            #plus on à de graines de notre coté par rapport à camp adversaire plus on gagne de points
            position_value += (sum(board[self.computer_khala + 1: self.computer_khala +7]) - sum(board[self.player_khala + 1: self.player_khala +7]) *1.5)
            return kalah_difference  * 2 + position_value
            

    def start(self):
        self.display_board()
        max_depth = 3 if self.level == 1 else 5 if self.level == 2 else 9 if self.level == 3 else None
        while True:
            
            self.move(self.player_khala, self.computer_khala, self.selectHole(), self.board, False, max_depth)
            if self.is_game_over():
                break  

            self.move(self.computer_khala, self.player_khala, self.computer_move(self.board, max_depth), self.board, True, max_depth)
            if self.is_game_over():
                break

            self.display_board()

            if(input("souhaiter vous sauvegarder la partie ? (O/N)") == "O"):
                self.save_game()
                return
        self.end_game(self.board)
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

    
initalize_game()


