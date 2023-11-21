import os
class KalahGame:
    def __init__(self, level, side):
        # Initialize the game board
        self.board = [0] + [3] * 6 + [0] + [3] * 6
        self.level = level
        #0 sud 1 nord
        self.side = side
        self.player_khala = 0 if side == 0 else 7
        self.computer_khala = 7 if side == 0 else 0
    
    def display_board(self):
        # Display the board
        os.system('cls')
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
            deplacement = selected_hole - i if 0 <= selected_hole < 7 else 7 + abs(selected_hole - i) if selected_hole - i < 0 else selected_hole + i 
            self.board[(deplacement)] += 1
            #si dernier tours
            if(i == marbles):
                #si la case et vide le joueur rejoue
                if((deplacement == 0 and self.side == 0) or (deplacement == 7 and self.side == 1)):
                    self.player_move()
                #si la case à une ou deux billes le joueur prend les billes dans sont kalah
                elif(1 < self.board[(selected_hole - i) % -12] < 4):
                    self.board[self.player_khala] += self.board[(selected_hole - i) % -12]
                    self.board[(selected_hole - i) % -12] = 0
                    j = 1
                    while True:
                        if (0 < self.board[(selected_hole - i + j)] < 3): 
                            self.board[self.player_khala] += self.board[(selected_hole - i + j)]
                            self.board[(selected_hole - i + j)] = 0
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
                save_game()
                return
        self.end_game()
        print("plateau final :")
        self.display_board()
        print(self.get_winner())


def initalize_game(): 
    while True:
        #choisir le side
        side = int(input("choisisser votre side (0 nord ou 1 sud)"))
        #choisir le niveau de difficulté
        level = int(input("choisisser votre niveau de difficulté (1, 2 ou 3)"))
        game = KalahGame(level, side)
        game.start()
        if input("Voulez vous rejouer ? (O/N)") == "N":
            break

def save_game():
    #à faire
    return

def minMax():
    #à faire
    return
    
initalize_game()


