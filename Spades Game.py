# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:28:58 2024

@author: Brian Holliday
"""

import numpy as np
import pandas as pd
import math

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

def set_name():
    
    global names
    
    name = np.random.choice(names, size = 1, replace = False)[0]
    
    names.remove(name) # pop name that is going to be assigned to player
    
    return name

def cards_ranker(played_cards):
    
    if len(played_cards) == 0:
        raise ValueError("Played cards is an empty list.")
        
    elif played_cards is None:
        raise ValueError("Played cards value is NoneType")
        
    else:
        
        highest_rank = 0
        winning_card = None
        leading_suit = played_cards[0][0]
        spades_played = [spade for spade in played_cards if spade[0] == "S"]
        leading_suit_cards = [leading_suit_card for leading_suit_card in played_cards if leading_suit_card[0] == leading_suit]
        non_leading_suit_non_spade_cards = [extra_card for extra_card in played_cards if extra_card[0] != "S" and extra_card[0] != leading_suit]
        ranked_cards_order = []
        
        if len(spades_played) == 0: # if no spades were played in the round
            
            for card in leading_suit_cards:
                if card[1] >= highest_rank:
                    highest_rank = card[1]
                    winning_card = card
                else:
                    pass
        else: 
            for card in spades_played:
                if card[1] >= highest_rank:
                    highest_rank = card[1]
                    winning_card = card
                    
                else:
                    pass
                
        ranked_cards_order.append(winning_card)
        
        if leading_suit == "S":  # Spades is the leading suit
        
            spades_sorted = sorted(spades_played, key = lambda x: x[1], reverse=True)[1:]
            non_leading_sorted = sorted(non_leading_suit_non_spade_cards, key = lambda x: x[1], reverse = True)
            ranked_cards_order.extend(spades_sorted)
            ranked_cards_order.extend(non_leading_sorted)
            
        else:  # A non-Spades suit is leading
            
            if winning_card[0] == "S":
                spades_sorted = sorted(spades_played, key=lambda x: x[1], reverse = True)[1:]
                leading_sorted = sorted(leading_suit_cards, key=lambda x: x[1], reverse = True)
                
            else:
                spades_sorted = sorted(spades_played, key=lambda x: x[1], reverse = True)
                leading_sorted = sorted(leading_suit_cards, key=lambda x: x[1], reverse = True)[1:]
            non_leading_sorted = sorted(non_leading_suit_non_spade_cards, key = lambda x: x[1], reverse = True)
            ranked_cards_order.extend(spades_sorted)
            ranked_cards_order.extend(leading_sorted)
            ranked_cards_order.extend(non_leading_sorted)

    return winning_card, ranked_cards_order
            
class Player():
    
    def __init__(self):
        
        self.name = set_name()
        self.hand = []
        self.tricks_predicted = None
        self.partner = None
        self.tricks_won = 0
        
    def __str__(self):
        
        partner_name = self.partner.name if self.partner else "None"
        
        return (f"Player Name: {self.name}\n"
                f"Player Hand: {self.hand}\n"
                f"Player Tricks Predicted: {self.tricks_predicted}\n"
                f"Player Partner: {partner_name}")
    
    
    def has_suit(self, suit):
        
        has_suit = False
        
        for card in self.hand:
            
            if card[0] == suit:
                has_suit = True
            
        return has_suit
    

class Spades_Game():
    
    def __init__(self, player_list, rounds_to_play):
        self.player_list = player_list
        self.dealing_order = None
        self.round_number = 0
        self.max_rounds = rounds_to_play
        self.suits = ["S", "H", "C", "D"]
        self.rank = np.arange(start = 2, stop = 15) 
        self.deck = [(s, r) for s in self.suits for r in self.rank]
        self.player_tracking_data = [] # make+ empty list to store player tracking data
        self.player_tricks_won_data = []
        self.tricks_data = None
         
    def set_dealing_order(self):
        
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
        
        np.random.shuffle(deck_shuffled)
        
        self.dealing_order = self.set_dealing_order()
        
        while len(deck_shuffled) > 0:
            for player_num in self.dealing_order:
                current_card = deck_shuffled.pop()
                self.player_list[player_num].hand.append(current_card)
    
    def set_teammates(self):
        
        # set partners
        self.player_list[0].partner = self.player_list[2]
        self.player_list[2].partner = self.player_list[0]
        self.player_list[1].partner = self.player_list[3]
        self.player_list[3].partner = self.player_list[1]
        
    def get_hand_ranks(self):
        
        for player in self.player_list:
            
            player.get_hand_rank()
            
    def search_player_by_name(self, player_name):
        
        for i in range(0, len(self.player_list)):
            
            if self.player_list[i].name == player_name:
                return i
            
        raise ValueError(f"Player with name {player_name} not found.")
        
    def round_winner(self, player_and_card_list, winning_card):
        
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
        
        player_card = None
        
        for player in self.player_list:
                if player.name == player_name:
                    return player_and_card_dict[player_name]
                else:
                    next
                    
        if player_card is None:
            
            raise ValueError("Could not find link between card and player")
        
            
    def play_trick(self):
        
        cards_played = 0
        playing_order = self.dealing_order
        played_cards_list = []
        player_and_card_list = {}
        
        for i in playing_order:
            
            if cards_played == 0:
                
                # select random card if you are the first player in a round
                random_card_index = np.random.randint(low = 0, high = len(self.player_list[i].hand), size = 1, dtype = np.int64)[0]
                card_selected = self.player_list[i].hand[random_card_index]
                
                player_and_card_list.update({self.player_list[i].name : card_selected})
                played_cards_list.append(card_selected)
                self.player_list[i].hand.remove(card_selected) # pop by index
                
            else:
                
                leading_suit = played_cards_list[0][0]
                has_leading_suit = self.player_list[i].has_suit(leading_suit)
                
                if has_leading_suit: # if player has same suit as the leading card
                    filtered_hand = [card for card in self.player_list[i].hand if card[0] == leading_suit]
                    random_card_index = np.random.randint(low = 0, high = len(filtered_hand), size = 1, dtype = np.int64)[0]
                    card_selected = filtered_hand[random_card_index]
                    
                    player_and_card_list.update({self.player_list[i].name : card_selected})
                    played_cards_list.append(card_selected)
                    
                    # pop played card from players hand by value
                    self.player_list[i].hand.remove(card_selected)
                
                else: # if the played does not have leading suit than just select random card
                    random_card_index = np.random.randint(low = 0, high = len(self.player_list[i].hand), size = 1, dtype = np.int64)[0]
                    card_selected = self.player_list[i].hand[random_card_index]
                    
                    player_and_card_list.update({self.player_list[i].name : card_selected})
                    played_cards_list.append(card_selected)
                    
                    # pop played card from played hand by value
                    self.player_list[i].hand.remove(card_selected)
                    
                    
            cards_played = cards_played + 1
            
        winning_card, cards_played = cards_ranker(played_cards_list)    
        round_winner_name = self.round_winner(player_and_card_list, winning_card)
        
        for i in range(len(self.player_list)):
            
            if round_winner_name == self.player_list[i].name:
    
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
    
    def update_player_hand_data(self, current_round):
        
        for player in self.player_list:
            current_dict = {"player_name" : player.name, "round" : current_round}
            for card in player.hand:
                card_string = card[0] + "_" + str(card[1])
                current_dict[card_string] = 1
        
            self.player_tracking_data.append(current_dict)
            
    def update_trick_data(self, current_round):
        
        for player in self.player_list:
            
            current_dict = {"player_name" : player.name, "round" : current_round, "tricks_won": player.tricks_won}
            self.player_tricks_won_data.append(current_dict)
            
    def play_rounds(self):
        
        spades_data = []
        
        for round_num in range(self.max_rounds):
            
            self.round_number = round_num
            self.shuffle_and_deal()
            trick = 1
            while any(len(player.hand) > 0 for player in self.player_list):
                
                if trick == 1:
                    self.update_player_hand_data(round_num)
                
                winning_card, round_winner_name, cards_played, player_and_card_list = self.play_trick()
                
                player_0_tuple = self.card_and_player_link(self.player_list[0].name, player_and_card_list)
                player_1_tuple = self.card_and_player_link(self.player_list[1].name, player_and_card_list)
                player_2_tuple = self.card_and_player_link(self.player_list[2].name, player_and_card_list)
                player_3_tuple = self.card_and_player_link(self.player_list[3].name, player_and_card_list)
                
                player_0_card = player_0_tuple[0] + "_" + str(player_0_tuple[1])
                player_1_card = player_1_tuple[0] + "_" + str(player_1_tuple[1])
                player_2_card = player_2_tuple[0] + "_" + str(player_2_tuple[1])
                player_3_card = player_3_tuple[0] + "_" + str(player_3_tuple[1])
                
                winning_card_string = winning_card[0] + "_" + str(winning_card[1])
                
                round_dict = {"round" : round_num, "trick": trick, 
                              "player_0_card" : player_0_card, "player_1_card" : player_1_card, 
                              "player_2_card" : player_2_card, "player_3_card" : player_3_card,
                              "winning_card" : winning_card_string, "round_winner_name" : round_winner_name}
                
                spades_data.append(round_dict)
                trick = trick + 1
            
            self.update_trick_data(round_num) # update the tricks for each player
            
            
            for i in range(len(self.player_list)):
                
                self.player_list[i].tricks_won = 0
            
        self.tricks_data = spades_data
            
players = [Player(), Player(), Player(), Player()]
game = Spades_Game(players, 100000)
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

