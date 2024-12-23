# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:28:58 2024

@author: Brian Holliday
"""

import numpy as np
import pandas as pd

# player names for the simulatoin
names = [
    "Liam", "Noah", "Oliver", "Elijah", "Mateo", "Hiroshi", "Luca", "Arjun", "Mohammed", "Carlos",
    "Ethan", "Benjamin", "Alexander", "William", "James", "Youssef", "Santiago", "Dimitri", "Juan", "Leon",
    "Kai", "Mikhail", "Viktor", "Chen", "Tariq", "Andres", "Igor", "Nikolai", "Samuel", "Sebastian",
    "Ahmed", "Rajesh", "Kenji", "Omar", "Emmanuel", "Hassan", "Diego", "Ali", "Gabriel", "Oscar",
    "Ismail", "Felix", "Hugo", "Aditya", "Julian", "Hamza", "Levi", "Malik", "Thiago", "Reza",
    "Emma", "Olivia", "Ava", "Sophia", "Mia", "Aria", "Fatima", "Yara", "Zara", "Noor",
    "Ananya", "Isabella", "Emily", "Chloe", "Layla", "Amara", "Freya", "Nina", "Camila", "Leila",
    "Akari", "Elena", "Aisha", "Sofia", "Lila", "Hana", "Mei", "Elsa", "Ines", "Rosa",
    "Lucia", "Amira", "Tanya", "Khadija", "Maya", "Clara", "Adele", "Ruby", "Priya", "Luna",
    "Harper", "Violet", "Mariam", "Greta", "Jasmine", "Anika", "Sienna", "Nadia", "Eva", "Maria"
]

# function to set names for the player object
def set_name():
    
    global names
    
    name = np.random.choice(names, size = 1, replace = False)[0]
    
    names.remove(name) # pop name that is going to be assigned to player
    
    return name

def cards_ranker(played_cards): # this function ranks the cards that are played in the trick and identifes the winning card
    
    if len(played_cards) == 0: # raises error if no cards are passed into function
        raise ValueError("Played cards is an empty list.") 
        
    elif played_cards is None: # raises error if played cards list is None
        raise ValueError("Played cards value is NoneType")
        
    else:
        
        highest_rank = 0 
        winning_card = None
        leading_suit = played_cards[0][0] # leading suit is the first card in the the list
        spades_played = [spade for spade in played_cards if spade[0] == "S"] # identify the spades played in the trick
        leading_suit_cards = [leading_suit_card for leading_suit_card in played_cards if leading_suit_card[0] == leading_suit] # identify the cards in the leading suit
        # identify cards that are not in the leading suit or spades
        non_leading_suit_non_spade_cards = [extra_card for extra_card in played_cards if extra_card[0] != "S" and extra_card[0] != leading_suit] 
        ranked_cards_order = [] # list to store ranked cards
        
        if len(spades_played) == 0: # if no spades were played in the round
            # if no spades are played get the highest ranked card of the leading suit
            for card in leading_suit_cards:
                if card[1] >= highest_rank:
                    highest_rank = card[1]
                    winning_card = card
                else:
                    pass
        else: # if spades are played the highest ranking spade is the winning card
            for card in spades_played:
                if card[1] >= highest_rank:
                    highest_rank = card[1]
                    winning_card = card
                    
                else:
                    pass
                
        ranked_cards_order.append(winning_card) # winning card will always be the first in the list
        
        if leading_suit == "S":  # Spades is the leading suit
            
        # add the next level of spades after the winning card
            spades_sorted = sorted(spades_played, key = lambda x: x[1], reverse=True)[1:] 
        # next in order is the non_spade cards ranked by card value
            non_leading_sorted = sorted(non_leading_suit_non_spade_cards, key = lambda x: x[1], reverse = True)
            ranked_cards_order.extend(spades_sorted) # add the ranked spades
            ranked_cards_order.extend(non_leading_sorted) # add the non spade cards
            
        else:  # A non-Spade suit is leading
            
            if winning_card[0] == "S": # if Spades were not the leading suit, but still the leading card
            # sort the spades that were played
                spades_sorted = sorted(spades_played, key=lambda x: x[1], reverse = True)[1:]
                leading_sorted = sorted(leading_suit_cards, key=lambda x: x[1], reverse = True)
                
            else: # if the trick was not won by a Spade card
                spades_sorted = sorted(spades_played, key=lambda x: x[1], reverse = True)
                leading_sorted = sorted(leading_suit_cards, key=lambda x: x[1], reverse = True)[1:]
            non_leading_sorted = sorted(non_leading_suit_non_spade_cards, key = lambda x: x[1], reverse = True)
            ranked_cards_order.extend(spades_sorted) # spades go first
            ranked_cards_order.extend(leading_sorted) # leading suit go next
            ranked_cards_order.extend(non_leading_sorted) # lastly non spade and non leading suit cards

    return winning_card, ranked_cards_order
            
class Player():
    
    def __init__(self):
        
        self.name = set_name() # call the function to set player name at random
        self.hand = [] # list to store player hand for the round
        self.tricks_predicted = None # not used in script
        self.partner = None # not used in trick
        self.tricks_won = 0 # store how many tricks were won in a round
        
    def __str__(self): # print played information
        
        partner_name = self.partner.name if self.partner else "None"
        
        return (f"Player Name: {self.name}\n"
                f"Player Hand: {self.hand}\n"
                f"Player Tricks Predicted: {self.tricks_predicted}\n"
                f"Player Partner: {partner_name}")
    
    
    def has_suit(self, suit): # function to see if player has a card in the leading suit in there hand
        
        has_suit = False
        
        for card in self.hand:
            
            if card[0] == suit:
                has_suit = True
            
        return has_suit
    

class Spades_Game():
    
    def __init__(self, player_list, rounds_to_play):
        self.player_list = player_list # list to store the 4 players in the game
        self.dealing_order = None # stores the list for the dealing order in each round
        self.round_number = 0 # stores how many rounds have been played.
        self.max_rounds = rounds_to_play # stores how many simulations are to be played
        self.suits = ["S", "H", "C", "D"] # suits in a card game (Spades, Diamonds, Clubs, and Hearts)
        self.rank = np.arange(start = 2, stop = 15) # stores ranks for the decks
        self.deck = [(s, r) for s in self.suits for r in self.rank] # deck list used in the game
        self.player_tracking_data = [] # make+ empty list to store player tracking data
        self.player_tricks_won_data = [] # stores how many tricks were won by each player in each round
        self.tricks_data = None # stores each card played in each trick for each round
         
    def set_dealing_order(self): # set the dealing order
    # simulating each player dealing clockwise when it is their turn to deal.
        
        if self.round_number % 4 == 0:
            return np.array([1, 2, 3, 0], dtype = np.int64)
        elif self.round_number % 4 == 1:
            return np.array([2, 3, 0, 1], dtype = np.int64)
        elif self.round_number % 4 == 2:
            return np.array([3, 0, 1, 2], dtype = np.int64)
        else:
            return np.arange(start = 0, stop = 4, dtype = np.int64)
                
    def shuffle_and_deal(self):
        
        deck_shuffled = self.deck.copy() 
        
        np.random.shuffle(deck_shuffled) # shuffle the deck after each round
        
        self.dealing_order = self.set_dealing_order() # set dealing order
        
        while len(deck_shuffled) > 0: # deal cards in deck to each player clockwise
            for player_num in self.dealing_order:
                current_card = deck_shuffled.pop()
                self.player_list[player_num].hand.append(current_card)
    
    def set_teammates(self): # set teammates in game. (Not used in simulation )
        
        # set partners
        self.player_list[0].partner = self.player_list[2]
        self.player_list[2].partner = self.player_list[0]
        self.player_list[1].partner = self.player_list[3]
        self.player_list[3].partner = self.player_list[1]
            
    def search_player_by_name(self, player_name): # search for player in game by name
        
        for i in range(0, len(self.player_list)):
            
            if self.player_list[i].name == player_name:
                return i
            
        raise ValueError(f"Player with name {player_name} not found.")
        
    def round_winner(self, player_and_card_list, winning_card):
        
        # function to match the winning card with winning player
        winning_player = None
        
        for key, value in player_and_card_list.items():
            
            if value == winning_card:
                winning_player = key
                
            else:
                next
        
        if winning_player is None:
            
            raise ValueError("Winning Player value is NoneType")
        
        else:
            
            return winning_player
        
    def card_and_player_link(self, player_name, player_and_card_dict):
        
        # function to link each player with the card that they played
        player_card = None
        
        for player in self.player_list:
                if player.name == player_name:
                    return player_and_card_dict[player_name]
                else:
                    next
                    
        if player_card is None:
            
            raise ValueError("Could not find link between card and player")
        
            
    def play_trick(self): # this function plays each trick for each round
        
        cards_played = 0
        playing_order = self.dealing_order # playing order is the same as the dealing order
        played_cards_list = [] # to store the cards played in the trick
        player_and_card_list = {} # dictionary to link the card with the player that played it
        
        for i in playing_order:
            
            if cards_played == 0: 
                
                # select random card if you are the first player in a round
                random_card_index = np.random.randint(low = 0, high = len(self.player_list[i].hand), size = 1, dtype = np.int64)[0]
                card_selected = self.player_list[i].hand[random_card_index]
                
                player_and_card_list.update({self.player_list[i].name : card_selected}) # link played name and card
                played_cards_list.append(card_selected) # add card to the played cards list
                self.player_list[i].hand.remove(card_selected) # pop hard from hand by index
                
            else:
                
                leading_suit = played_cards_list[0][0] # identify the leading suit for the trick
                has_leading_suit = self.player_list[i].has_suit(leading_suit) # checks if player has the leading suit
                
                if has_leading_suit: # if player has same suit as the leading card
                    filtered_hand = [card for card in self.player_list[i].hand if card[0] == leading_suit] # filters for cards in leading suit
                    random_card_index = np.random.randint(low = 0, high = len(filtered_hand), size = 1, dtype = np.int64)[0] # gets random card from filtered card list
                    card_selected = filtered_hand[random_card_index]
                    
                    player_and_card_list.update({self.player_list[i].name : card_selected}) # link played and card
                    played_cards_list.append(card_selected) # append card to played card list
                    
                    # pop played card from players hand by value
                    self.player_list[i].hand.remove(card_selected) # remove card from players hand
                
                else: # if the played does not have leading suit than just select random card
                    random_card_index = np.random.randint(low = 0, high = len(self.player_list[i].hand), size = 1, dtype = np.int64)[0]
                    card_selected = self.player_list[i].hand[random_card_index]
                    
                    player_and_card_list.update({self.player_list[i].name : card_selected})
                    played_cards_list.append(card_selected)
                    
                    # pop played card from played hand by value
                    self.player_list[i].hand.remove(card_selected)
                    
                    
            cards_played = cards_played + 1
            
        winning_card, cards_played = cards_ranker(played_cards_list) # rank the cards played in the round
        round_winner_name = self.round_winner(player_and_card_list, winning_card) # get the name of the round winner
        
        for i in range(len(self.player_list)):
            
            if round_winner_name == self.player_list[i].name:
                # add 1 to the tricks won in the round if player had the winning card
                self.player_list[i].tricks_won = self.player_list[i].tricks_won + 1
            
            else:
                next
        
        return winning_card, round_winner_name, cards_played, player_and_card_list
    
    def create_player_hand_data(self, rounds_to_play): 
        
        player_count = len(self.player_list)
        max_rows = player_count * self.max_rounds
        
        colnames = ["player_name", "round"] + [s + "_" + str(r) for s in self.suits for r in self.rank] + ["tricks_won"]
        player_hand_data = pd.DataFrame(0, index = range(max_rows), columns = colnames)
        
        return player_hand_data
    
    def update_player_hand_data(self, current_round): # update played hand data after each round
    
    # data is appended to a dictionary after each round
        
        for player in self.player_list: 
            current_dict = {"player_name" : player.name, "round" : current_round}
            for card in player.hand: # loop to store each card in each players hand in each round
                card_string = card[0] + "_" + str(card[1])
                current_dict[card_string] = 1
        
            self.player_tracking_data.append(current_dict)
            
    def update_trick_data(self, current_round):
        
        for player in self.player_list: # to store how many tricks were won by each player in each round
            
            current_dict = {"player_name" : player.name, "round" : current_round, "tricks_won": player.tricks_won}
            self.player_tricks_won_data.append(current_dict)
            
    def play_rounds(self): # this function will simulate an entire round of spades
        
        spades_data = [] # store the tricks data for the round
        
        for round_num in range(self.max_rounds): # run the rounds on a loop
            
            self.round_number = round_num # store the round number
            self.shuffle_and_deal() # deal the cards for the round
            trick = 1 # initalize the trick number
            while any(len(player.hand) > 0 for player in self.player_list): # while each player has a card in their hand
                
                if trick == 1:
                    self.update_player_hand_data(round_num) # store hand data for each player in the beginning of each round
                
                # play each trick while there are still cards in each players hand
                winning_card, round_winner_name, cards_played, player_and_card_list = self.play_trick() 
                
                # link each player with card that they played
                player_0_tuple = self.card_and_player_link(self.player_list[0].name, player_and_card_list)
                player_1_tuple = self.card_and_player_link(self.player_list[1].name, player_and_card_list)
                player_2_tuple = self.card_and_player_link(self.player_list[2].name, player_and_card_list)
                player_3_tuple = self.card_and_player_link(self.player_list[3].name, player_and_card_list)
                
                # get string for each card
                player_0_card = player_0_tuple[0] + "_" + str(player_0_tuple[1])
                player_1_card = player_1_tuple[0] + "_" + str(player_1_tuple[1])
                player_2_card = player_2_tuple[0] + "_" + str(player_2_tuple[1])
                player_3_card = player_3_tuple[0] + "_" + str(player_3_tuple[1])
                
                winning_card_string = winning_card[0] + "_" + str(winning_card[1])
                
                # store cards played in trick in a dictonary
                round_dict = {"round" : round_num, "trick": trick, 
                              "player_0_card" : player_0_card, "player_1_card" : player_1_card, 
                              "player_2_card" : player_2_card, "player_3_card" : player_3_card,
                              "winning_card" : winning_card_string, "round_winner_name" : round_winner_name}
                
                spades_data.append(round_dict)
                trick = trick + 1
            
            self.update_trick_data(round_num) # update the tricks for each player
            
            
            for i in range(len(self.player_list)): # reset number of tricks by each player 
                
                self.player_list[i].tricks_won = 0
            
        self.tricks_data = spades_data
            
players = [Player(), Player(), Player(), Player()] # initalize four players
game = Spades_Game(players, 100000) # simulate 100000 rounds of Spades
game.play_rounds()

tricks_data = pd.DataFrame(game.tricks_data)
tricks_win_data = pd.DataFrame(game.player_tricks_won_data)
player_hands_data = pd.DataFrame(game.player_tracking_data)

# output spades data
tricks_data.to_csv("C:\\Users\\holli\\OneDrive\\Documents\\Graduate School\\Data Mining\\Final Project\\game data\\cards_played_per_trick.csv",
                   header = True, index = False)

tricks_win_data.to_csv("C:\\Users\\holli\\OneDrive\\Documents\\Graduate School\\Data Mining\\Final Project\\game data\\tricks_won_by_player.csv", 
                       header = True, index = False)

player_hands_data.to_csv("C:\\Users\\holli\\OneDrive\\Documents\\Graduate School\\Data Mining\\Final Project\\game data\\player_hands_by_round.csv", 
                         header = True, index = False)

