import numpy as np
import operator
import collections
import random
import time
import traceback
import sys


#This is the main game loop
def play(Pandemic):
    active_player_index = 0
    infected_last = [0,0,0,0,0]
    while Pandemic.GameBoard.game_over == False:
        active_player = Pandemic.Players[active_player_index]
        print "Player", active_player_index, "please choose an action!"
        print "Please type 'What can I do?' to see a list of actions."
        while active_player.actions > 0:
            try:
                input = raw_input("Your action: ")
                parse_action(Pandemic, active_player, input)
                time.sleep(0.25)
            except KeyError:
                a = "Key Error!  Did you capitalize a color"
                b = " or mistype a city name?"
                a = a + b
                print a
                print "Please make sure to type the command EXACTLY"
                sys.exc_info()[3]
            
        print "Drawing two Player cards..."
        #Set event_in_hand to false for the initial check
        event_in_hand = False
        #Check for events in the player's hand
        for card in active_player.hand:
            if Pandemic.GameBoard.events.count(card) > 0:
                event_in_hand = True
        #Draw a card
        card = Pandemic.GameBoard.player_deck.pop(0)
        #Epidemic check
        if card == "Epidemic":
            print "Epidemic has been drawn!"
            #If the player has an event, let them have the chance to use it.
            if event_in_hand:
                print "Would you like to use an Event Card?"
                input = raw_input("If not, type 'Pass': ")
                parse_action(Pandemic, active_player, input)
            #Call epidemic, check for game over, and update the board
            epidemic(Pandemic.GameBoard, Pandemic.Players)
            Pandemic.GameBoard.check_if_game_over
            Pandemic.draw_board()
        #If it's not an epidemic, add it to their hand
        else:
            active_player.hand.append(card)
        #Set event_in_hand to false for the second check
        event_in_hand = False
        for card in active_player.hand:
            if Pandemic.GameBoard.events.count(card) > 0:
                event_in_hand = True
        #And draw a second card.
        card = Pandemic.GameBoard.player_deck.pop(0)
        #Epidemic check
        if card == "Epidemic":
            print "Epidemic has been drawn!"
            #If the player has an event, let them have the chance to use it.
            if event_in_hand:
                print "Would you like to use an Event Card?"
                input = raw_input("If not, type 'Pass': ")
                parse_action(Pandemic, active_player, input)
            #Call epidemic, check for game over, and update the board
            epidemic(Pandemic.GameBoard, Pandemic.Players)
            Pandemic.GameBoard.check_if_game_over
            Pandemic.draw_board()
        #If it's not an epidemic, add it to their hand
        else:
            active_player.hand.append(card)
            #And print their hand now that they're done drawing.
            print "Player", active_player_index, "Hand:"
            active_player.print_hand(Pandemic.GameBoard)
        while len(active_player.hand) > 7:
            a = "Player", active_player_index
            print a, "has too many cards in their hand!"
            discard(GameBoard, active_player)
        #Set event_in_hand to false for the third check
        event_in_hand = False
        for card in active_player.hand:
            if Pandemic.GameBoard.events.count(card) > 0:
                event_in_hand = True
        #If they have an event in hand before the Infect stage,
        #give them a chance to use it
        if event_in_hand:
            print "Would you like to use an Event Card?"
            input = raw_input("If not, type 'Pass': ")
            parse_action(Pandemic, active_player, input)
        #Then infect
        print "Infecting cities..."
        infection_stage(Pandemic.GameBoard, Pandemic.Players)
        #Check for game over
        Pandemic.GameBoard.check_if_game_over
        #Draw the board
        Pandemic.draw_board()
        #Note the newly infected cities:
        print
        for city in Pandemic.GameBoard.infected_cities:
            if city != 0:
                if Pandemic.GameBoard.infected_cities.index(city) == 0:
                    print "An Epidemic occurred in ", city
                elif Pandemic.GameBoard.infected_cities.index(city) == 1:
                    print "An Epidemic occurred in ", city
                else:
                    print city, "was infected!"
                index = Pandemic.GameBoard.infected_cities.index(city)
                Pandemic.GameBoard.infected_cities[index] = 0
        #And advance the turn to the next player.
        active_player_index += 1
        if active_player_index >= len(Pandemic.Players):
            active_player_index = 0
        print "Player", active_player_index," can take their turn now."

def parse_action(Pandemic, player, input):
    words = input.split()
    location = player.location
    home_city = Pandemic.GameBoard.cities[location]
    if words[0] == "What":
        allowable_actions(player, Pandemic)
    elif words[0] == "Walk":
        if words[1] == "to":
            #one step walk
            #get city object
            destination = Pandemic.GameBoard.cities[words[2]]
            move_action(Pandemic.GameBoard, player, destination)
        elif len(words) == 5:
            #Multi-step walk
            move_player(Pandemic.GameBoard, player, words[4], int(words[1]))
        elif len(words) == 4:
            #Multi-step walk
            move_player(Pandemic.GameBoard, player, words[3], int(words[1]))
    elif words[0] == "Fly":
        #Direct flight
        direct_flight(Pandemic.GameBoard, player, words[3])
    elif words[0] == "Charter":
        #Charter flight
        charter_flight(Pandemic.GameBoard, player, words[3])
    elif words[0] == "Shuttle":
        #Shuttle flight
        shuttle_flight(Pandemic.GameBoard, player, words[3])
    elif words[0] == "Dispatch":
        #dispatcher flight
        P = Pandemic.Players
        G = Pandemic.GameBoard
        target = Pandemic.Players[int(words[1])]
        dest = Pandemic.Players[int(words[3])].location
        dispatch_flight(G, P, player, target, dest)
    elif words[0] == "Dispatcher:":
        if words[1] == "Walk":
            if words[3] == "to":
                #one step walk
                dest = Pandemic.GameBoard.cities[words[4]]
                move_action(Pandemic.GameBoard, int(words[2]), dest, player)
            elif len(words) == 6:
                #Multi-step walk
                move_player(Pandemic.GameBoard, int(words[2]), words[6],
                            words[3], player)
            elif len(words) == 5:
                #Multi-step walk
                move_player(Pandemic.GameBoard, int(words[2]), words[5],
                            words[3], player)
        elif words[1] == "Fly":
            #Direct flight
            target = Pandemic.Players[int(words[2])]
            direct_flight(Pandemic.GameBoard, target, words[5], player)
        elif words[1] == "Charter":
            #Charter flight
            target = Pandemic.Players[int(words[3])]
            charter_flight(Pandemic.GameBoard, target, words[5], player)
        elif words[1] == "Shuttle":
            #Shuttle flight
            target = Pandemic.Players[int(words[3])]
            shuttle_flight(Pandemic.GameBoard, target, words[5], player)
        else:
            return
    elif words[0] == "Discard":
        #Operations Flight
        index = player.hand.index(words[1])
        operations_flight(Pandemic.GameBoard, player, words[5], index)
    elif words[0] == "Give":
        #Give Knowledge
        index = player.hand.index(words[1])
        target = Pandemic.Players[int(words[3])]
        give_knowledge(player, target, index)
    elif words[0] == "Take":
        #Take knowledge
        other_player = Pandemic.Players[int(words[3])]
        index = other_player.hand.index(words[1])
        take_knowledge(other_player, player, index)
    elif words[0] == "Treat":
        #Treat
        home_city.treat(player, Pandemic.GameBoard, words[1])
    elif words[0] == "Cure":
        #Cure
        if player.role == "Scientist":
            cure(Pandemic.GameBoard, player, words[4], words[5], words[6],
                 words[7])
        else:
            cure(Pandemic.GameBoard, player, words[4], words[5], words[6],
                 words[7], words[8])
    elif words[0] == "Build":
        #Try to build a research station
        if location in player.hand:
            index = player.hand.index(location)
            home_city.research(player, index, Pandemic.GameBoard)
    elif words[0] == "Move":
        #Try to move a research station
        if location in player.hand:
            index = player.hand.index(location)
            other_city = Pandemic.GameBoard.cities[words[4]]
            home_city.research(player, index, Pandemic.GameBoard, other_city)
    elif words[0] == "Pass":
        return
        #Pass the opportunity to use an Event card.
    elif words[0] == "Examine":
        if words[1] == "Player" or words[1] == "player":
            Pandemic.Players[int(words[2])].player_info(Pandemic.GameBoard)
        elif words[1] in Pandemic.GameBoard.city_index:
            #Examine city.
            Pandemic.GameBoard.cities[words[1]].print_city(GameBoard)
        elif words[1] == "Game":
            Pandemic.draw_board()
        else:
            return
    elif words[0] == "Use":
        #Event cards
        if words[1] == "Airlift":
            #Airlift
            target = Pandemic.Players[int(words[4])]
            airlift(Pandemic.GameBoard, player, target, words[6])
        elif words[1] == "Forecast":
            #Forecast
            forecast(Pandemic.GameBoard, player)
        elif words[1] == "Government":
            #Govgrant
            if words[4] == "build":
                gov_grant(Pandemic.GameBoard, player, words[9])
            if words[4] == "move":
                other_city = Pandemic.GameBoard.cities[11]
                gov_grant(Pandemic.GameBoard, player, words[9], other_city)
        elif words[1] == "One":
            #One Quiet Night
            one_quiet_night(Pandemic.GameBoard, player)
        elif words[1] == "Resilient":
            #Resilient Population
            resilient_population(Pandemic.GameBoard, player, words[5])
        else:
            return
    elif words[0]=="Quit" or words[0] == "Exit":
        exit()
    elif words[0] == "Help" or words[0] == "help":
        help()
    else:
        return

def help():
    print "Commands:"
    print "Note that for all commands, city names should not have spaces."
    print "'St. Petersburg' will not work; use 'StPetersburg' instead."
    print
    print "Player Movement:"
    print "Walk to Neighbor: 'Walk to [name of destination]'"
    print "Multi-action Walk: 'Walk [number of steps] steps towards [name of"
    print "destination]'"
    print "Direct Flight: 'Fly directly to [name of destination'"
    print "Charter Flight: 'Charter fly to [name of destination]'"
    print "Shuttle Flight: 'Shuttle fly to [name of destination]'"
    print "Operations Flight: 'Discard [name of card] to fly to [name of"
    print "destination]'"
    print "Dispatch Flight: 'Fly [target player number] to [destination player"
    print "number]'"
    print
    print "Dispatcher Movement:"
    print "Walk to Neighbor: 'Dispatcher: Walk [player number] to [name of"
    print "destination]'"
    print "Multi-action Walk: 'Dispatcher: Walk [player number] [number of"
    print "steps] steps towards [name of destination]'"
    print "Direct Flight: 'Dispatcher: Fly [player number] directly to [name of"
    print "destination]'"
    print "Charter Flight: 'Dispatcher: Charter fly [player number] to [name of"
    print "destination]'"
    print "Shuttle Flight: 'Dispatcher: Shuttle fly [player name] to [name of"
    print "destination]'"
    print
    print "Give Knowledge: 'Give [name of card] to [name of other player]'"
    print "Take Knowledge: 'Take [name of card] from [name of other player]'"
    print "Note that only researchers can share cards for one city while in"
    print "another city."
    print
    print "Treat a disease: 'Treat [color of disease tokens] in [name of city]'"
    print "Cure a disease: 'Cure [color of disease] by discarding [first card"
    print "name], [second card name], [third card name], [fourth card name], and"
    print "[fifth card name]*'"
    print "*Scientists may leave off the 5th card."
    print "Build a Research Station*: 'Build research station in [name of"
    print "destination]'"
    print "Move a Research Station: 'Move research station in [name of home city]"
    print "to [name of destination city]'"
    print "Note: there must be 7 research stations on the board to do the above."
    print
    print
    print "Meta Commands:"
    print "Look at Player's Information: 'Examine Player [player number]'"
    print "Look at a City's information: 'Examine [name of city]'"
    print "Look at Game Board: 'Examine Game Board'"
    print
    print
    print "Event Cards:"
    print
    print "Airlift: 'Use Airlift to fly [name of player] to [name of destination]'"
    print "Forecast: 'Use Forecast'"
    print "Government Grant: 'Use Government Grant to [build or move] a research"
    print "station in [name of destination]'"
    print "One Quiet Night: 'Use One Quiet Night'"
    print "Resilient Population: 'Use Resilient Population to remove [name of"
    print "infection card]'"

class GameBoard(object):
    terms = {"uncured": 0, "cured": 1, "eradicated": 2, "blue": 0, "yellow": 1,
             "black": 2, "red": 3, 0: "blue", 1: "yellow", 2: "black", 3: "red"}
    roles = ["Contingency", "Dispatcher", "Medic", "Operations",
             "Quarantine", "Researcher", "Scientist"]
    events = ["Epidemic", "Government Grant", "Airlift", "Forecast",
              "One Quiet Night", "Resilient Population"]
    actions = ["walk", "direct flight", "charter flight", "shuttle flight",
               "dispatch flight", "operations flight", "give knowledge",
               "take knowledge", "cure", "treat", "contingency"]
    infected_cities = [0,0,0,0,0,0]

    def __init__(self, Pandemic):
        self.Pandemic = Pandemic
        self.reset_game()

    def reset_game(self):
        """
        Reset all of the game attributes to their starting values
        """
        self.game_over = False
        self.cities = collections.OrderedDict(
             Atlanta= Atlanta("Atlanta"), Washington= Washington("Washington"),
             SanFrancisco= SanFrancisco("SanFrancisco"),
             Chicago= Chicago("Chicago"), Montreal= Montreal("Montreal"),
             NewYork= NewYork("NewYork"), London= London("London"),
             Madrid= Madrid("Madrid"), Paris= Paris("Paris"),
             Essen= Essen("Essen"), Milan= Milan("Milan"),
             StPetersburg= StPetersburg("StPetersburg"),
             LosAngeles= LosAngeles("LosAngeles"),
             MexicoCity= MexicoCity("MexicoCity"), Miami= Miami("Miami"),
             Bogota= Bogota("Bogota"), Lima= Lima("Lima"),
             Santiago= Santiago("Santiago"),
             BuenosAires= BuenosAires("BuenosAires"),
             SaoPaulo= SaoPaulo("SaoPaulo"), Lagos= Lagos("Lagos"),
             Kinsasha= Kinsasha("Kinsasha"),
             Johannesburg= Johannesburg("Johannesburg"),
             Khartoum= Khartoum("Khartoum"), Algiers= Algiers("Algiers"),
             Cairo= Cairo("Cairo"), Istanbul= Istanbul("Istanbul"),
             Moscow= Moscow("Moscow"), Baghdad= Baghdad("Baghdad"),
             Riyadh= Riyadh("Riyadh"), Tehran= Tehran("Tehran"),
             Karachi= Karachi("Karachi"), Mumbai= Mumbai("Mumbai"),
             Delhi= Delhi("Delhi"), Chennai= Chennai("Chennai"),
             Kolkata= Kolkata("Kolkata"), Bangkok= Bangkok("Bangkok"),
             Jakarta= Jakarta("Jakarta"), Sydney= Sydney("Sydney"),
             HoChiMinhCity= HoChiMinhCity("HoChiMinhCity"),
             Manila= Manila("Manila"), HongKong= HongKong("HongKong"),
             Taipei= Taipei("Taipei"), Osaka= Osaka("Osaka"),
             Tokyo= Tokyo("Tokyo"), Seoul= Seoul("Seoul"),
             Shanghai= Shanghai("Shanghai"), Beijing= Beijing("Beijing"))

        self.city_index =["Atlanta", "Washington", "SanFrancisco", "Chicago",
                          "Montreal", "NewYork", "London", "Madrid", "Paris",
                          "Essen", "Milan", "StPetersburg", "LosAngeles",
                          "MexicoCity", "Miami", "Bogota", "Lima", "Santiago",
                          "BuenosAires", "SaoPaulo", "Lagos", "Kinsasha",
                          "Johannesburg", "Khartoum", "Algiers", "Cairo",
                          "Istanbul", "Moscow", "Baghdad", "Riyadh", "Tehran",
                          "Karachi", "Mumbai", "Delhi", "Chennai", "Kolkata",
                          "Bangkok", "Jakarta", "Sydney", "HoChiMinhCity",
                          "Manila", "HongKong", "Taipei", "Osaka", "Tokyo",
                          "Seoul", "Shanghai", "Beijing"]
    
        self.player_deck = ["Atlanta", "Washington", "SanFrancisco",
                            "Chicago", "Montreal", "NewYork", "London",
                            "Madrid", "Paris", "Essen", "Milan",
                            "StPetersburg", "LosAngeles", "MexicoCity",
                            "Miami", "Bogota", "Lima", "Santiago",
                            "BuenosAires", "SaoPaulo", "Lagos",
                            "Kinsasha", "Johannesburg", "Khartoum",
                            "Algiers", "Cairo", "Istanbul", "Moscow",
                            "Baghdad", "Riyadh", "Tehran", "Karachi",
                            "Mumbai", "Delhi", "Chennai", "Kolkata",
                            "Bangkok", "Jakarta", "Sydney",
                            "HoChiMinhCity", "Manila", "HongKong",
                            "Taipei", "Osaka", "Tokyo", "Seoul", "Shanghai",
                            "Beijing", "Government Grant", "Airlift",
                            "Forecast", "One Quiet Night",
                            "Resilient Population"]
        
        self.infect_deck = ["Atlanta", "Washington", "SanFrancisco",
                            "Chicago", "Montreal", "NewYork", "London",
                            "Madrid", "Paris", "Essen", "Milan",
                            "StPetersburg", "LosAngeles", "MexicoCity",
                            "Miami", "Bogota", "Lima", "Santiago",
                            "BuenosAires", "SaoPaulo", "Lagos",
                            "Kinsasha", "Johannesburg", "Khartoum",
                            "Algiers", "Cairo", "Istanbul", "Moscow",
                            "Baghdad", "Riyadh", "Tehran", "Karachi",
                            "Mumbai", "Delhi", "Chennai", "Kolkata",
                            "Bangkok", "Jakarta", "Sydney",
                            "HoChiMinhCity", "Manila", "HongKong",
                            "Taipei", "Osaka", "Tokyo", "Seoul", "Shanghai",
                            "Beijing"]
        
        self.research_stations = [self.cities["Atlanta"],
                                  -1, -1, -1, -1, -1, -1]
        self.map_grids = create_distances(self.cities, self.city_index)
        self.distance = self.map_grids[0]
        self.previous = self.map_grids[1]
        self.outbreak_marker = 0
        self.infection_rate_marker = 0
        self.one_quiet_night_marker = 0
        self.cubes_remaining = [24, 24, 24, 24]
        self.card_colors_remaining = [12, 12, 12, 12]
        self.cures = [0,0,0,0]
        self.intensify_list = []
        self.infect_discard = []
        self.player_discard = []
        self.reason_over = ""
        

    def epidemic_this_turn(Pandemic):
        Pandemic.epidemic_drawn = True
        
    def check_if_game_over(self):
        """
        Checks if game is over. If it's over, sets self.game_over = True
        and defines a new attribute self.reason_over. It it's not over
        it does not do anything since self.game_over = False for a new
        board until it's changed here.
        """
        if len(self.player_deck) == 0:
            self.game_over = True
            self.reason_over = "Last player card dealt"
        elif self.outbreak_marker == 8:
            self.game_over = True
            self.reason_over = "Eight outbreaks"
        elif self.cubes_remaining.count(-24) > 0:
            self.game_over = True
            color = self.cubes_remaining.index(-1)
            self.reason_over = "Ran out of", color,"Disease Tokens"
        elif self.cures[self.terms["blue"]] > 0:
            if self.cures[self.terms["red"]] > 0:
                if self.cures[self.terms["yellow"]] > 0:
                    if self.cures[self.terms["black"]] > 0:
                        self.game_over = True
                        self.reason_over = "Victory!"

    
        


class City(object):
    def __init__(self, name):
        self.name = name
        self.color = -1
        self.disease_tokens = [-1,-1,-1,-1]
        self.research_station = -1
        self.city_connections = {}
        self.cubes_placed = 1
        self.draw_chance = 0
        self.outbroken = 0

    #This method just prints the city's information in an easy-to-read fashion.
    def print_city(self, GameBoard):
        self.numbers_to_colors = {0: "Blue", 1: "Yellow", 2: "Black", 3: "Red"}
        print "Name:            ", self.name
        print "Color:           ", self.numbers_to_colors[self.color]
        print "U | Y | B | R"
        self.u = str(self.disease_tokens[0])
        self.y = str(self.disease_tokens[1])
        self.b = str(self.disease_tokens[2])
        self.r = str(self.disease_tokens[3])
        print self.u,  "|", self.y, "|", self.b, "|", self.r
        if self.research_station == 1:
            print "Research Station? Built"
        else:
            print "Research Station? Not Built"
        
        print "Draw Chance:     ", self.draw_chance
        print "Damage if Drawn: ", self.cubes_placed
        print "Risk Assessment: ", float(self.draw_chance) * self.cubes_placed
        self.a = ""
        for city, distance in self.city_connections.iteritems():
            self.infected = False
            self.a += city + " ("
            for tokens in GameBoard.cities[city].disease_tokens:
                if tokens > 0:
                    self.color = GameBoard.cities[city].disease_tokens.index(tokens)
                    self.a += GameBoard.terms[self.color] + ": "
                    self.a += str(tokens)
                    if self.infected:
                        self.a += " "
                    self.infected = True
            if not self.infected:
                self.a += "uninfected"
            self.a += ")"
            if len(self.ciy_connections)
        print self.a


    #This method determines the number of cubes this city will put on the board
    #the next time it is infected.  It updates the city's cubes_placed every
    #time the city is infected or treated.
    def assess_risk(self, GameBoard):
        #If the city has three cubes of one color and could outbreak,
        if self.disease_tokens[self.color] == 3:
            self.cubes_placed = self.check_neighbors_for_outbreak(GameBoard)
            self.undo_neighbor_check(GameBoard)
        #Otherwise, it can only add one cube to the board.
        else:
            self.cubes_placed = 1
            
            
    #This method assists the above method in checking neighbors; it gets called
    #recursively until no neighbors with 3 disease cubes of the given color are
    #found.  It tracks which cities have already been checked by making their
    #disease cube count negative, which is reversed by the below method,
    #undo_neighbor_check. Open to better ideas.
    def check_neighbors_for_outbreak(self, GameBoard):
        #Set this city's cube count to be negative so it won't be counted twice
        self.disease_tokens[self.color] += -6
        #Create a returnable cube counter
        self.r = 0
        #Look through all of the city's neighbors.
        for neighbors in self.city_connections.keys():
            #Grab the neighbor being looked at by the loop
            self.neighbor = GameBoard.cities[neighbors]
            #If they have 3 cubes of the same color...
            if (self.neighbor.disease_tokens[self.color] == 3):
                #call this method on them, too.
                self.r += self.neighbor.check_neighbors_for_outbreak(GameBoard)
            #Otherwise, if they haven't already been checked...
            elif self.neighbor.disease_tokens[self.color] >= 0:
                #increment the returnable, as they can be infected
                self.r += 1
        return self.r

    #This method repairs the damage done by the above method,
    #check_neighbors_for_outbreak.
    def undo_neighbor_check(self, GameBoard):
        #Restore this city's cube count
        self.disease_tokens[self.color] += 6
        #Look through all of the city's neighbors.
        for neighbors in self.city_connections.keys():
            #Grab the neighbor being looked at by the loop
            self.neighbor = GameBoard.cities[neighbors]
            #If they've been negated
            if (self.neighbor.disease_tokens[self.color] == -3):
                #call this method on them, too.
                self.neighbor.undo_neighbor_check(GameBoard)

    #This method determines the likelihood that this city will be infected this
    #turn.  It examines the city's neighbors for potential sources of infection
    #by checking the probability of each neighboring city with 3 cubes being
    #infected, and by examining the Intensify pile and Infect Discard pile to
    #locate the city's card and estimate the odds of drawing it.
    def find_draw_chance(self, GameBoard):
        #Always safe to start with a 100% chance
        self.draw_chance = float(1.0)
        #Since the number of cards drawn is determined by the Infection Rate...
        self.infection_draw = 2
        if GameBoard.infection_rate_marker > 2:
            self.infection_draw += 1
        if GameBoard.infection_rate_marker > 5:
            self.infection_draw += 1
        #If the city's card is in the infect discard pile
        if self.name in GameBoard.infect_discard:
            #Then the only way to draw it is to draw an epidemic
            #so the draw chance is at worst, the chance to draw an epidemic
            #divided by the size of of the next Intensify pile, times the number
            #of cards drawn in the Infection stage.

            #First, check if the next Epidemic would increment the infection
            #draw rate.
            if GameBoard.infection_rate_marker == 3:
                self.infection_draw += 1
            elif GameBoard.infection_rate_marker == 6:
                self.infection_draw += 1
            #Then, multiply the infection draw rate by the chance of an epidemic
            self.e = GameBoard.Pandemic.epidemic_chance * self.infection_draw
            #Then, get the size of the new Intensify pile should an epidemic be
            #drawn this turn
            self.d = 1 + len(GameBoard.infect_discard)
            #and lastly, set the draw chance to the quotient of the above. 
            self.draw_chance = self.e / float(self.d)
        #If there are any cards in the Intensify pile
        elif len(GameBoard.intensify_list) > 0:
            #Check if this city is one of them
            if self.name in GameBoard.intensify_list:
                #If so, draw_chance = infection_draw / length(infection_pile)
                self.d = self.draw_chance / float(len(GameBoard.intensify_list))
                self.draw_chance = self.d * float(self.infection_draw)
            #If it isn't, and it's not in the discard pile, it hasn't been drawn
            else:
                #And can't be 'til all the cards in the Intensify pile are drawn
                self.draw_chance = 0
        #Otherwise, the city's card has yet to be drawn and the Intensify pile
        #is empty
        else:
            #so draw_chance = infection_draw / length(infect_deck)
            self.d = self.infection_draw
            self.draw_chance = self.d / float(len(GameBoard.infect_deck))
        
                
    #The active player builds a research station in this city.
    #Self is the city, player is the player building the research
    #station, discard_index is the index of the card being discarded in
    #the player's hand, GameBoard is GameBoard, and *args is the city
    #which needs to have its research station removed to make room for
    #the new one.
    def research(self, player, discard_index, GameBoard, *args):
        #Check that there isn't ALREADY a research station at this location...
        if (self.research == 1):
            print "Already a research station here!"
            return
        #if there are any additional arguments given...
        elif (len(args) > 0):
            #take the first one and delete the research station located in
            #that city.
            args[0].research = 0
            #And remove the above city from the list of research stations
            index = research_stations.index(args[0])
            GameBoard.research_stations[index] = -1
            print "Research Station in", args[0].name, "removed."
        #If no argument for research station removal is provided and there
        #are six research stations already built...
        elif (len(args) != 1 and GameBoard.research_stations.count(-1) == 0):
            print "Too many research stations already!  Need to remove one."
            return
        
        #If the player is an Operations Expert
        if (player.role == "Operations"):
            #Plop down the research station at his location
            self.research = 1
            #Add the research station to the first open spot on the list
            index = GameBoard.research_stations.index(-1)
            GameBoard.research_stations[index] = self
        #if the player is NOT an operations expert and has the card...
        elif GameBoard.cities[player.location] == self:
            if GameBoard.cities[player.hand[discard_index]] == self:
                #Build the research station there
                index = GameBoard.research_stations.index(-1)
                GameBoard.research_stations[index] = self
                #Note the color of the discarded city card in colorsRemaining
                color = GameBoard.cities[player.hand[discard_index]].color
                GameBoard.card_colors_remaining[color] += -1
                #Discard the card
                GameBoard.player_discard.append(player.hand.pop(discard_index))
                #Consume an action
                player.actions += -1


    #The active player treats one color in this city.  Self is self, player
    #is the player treating the disease, GameBoard is Game Board, and color
    #is the color of the disease being treated.
    def treat(self, player, GameBoard, color):
        color_int = GameBoard.terms[color]
        if self == GameBoard.cities[player.location]:
            #If there are no disease cubes of the chosen color, return.
            if self.disease_tokens[color_int] < 1:
                return
            #If the disease is already cured, or the player is a medic
            elif GameBoard.cures[color_int] > GameBoard.terms["uncured"]:
                #Grab the number of cubes of the chosen color off the city
                cubes = self.disease_tokens[color_int]
                #Return them to the cubes_remaining pool
                GameBoard.cubes_remaining[color_int] += cubes
                #and wipe them off the city
                self.disease_tokens[color_int] = 0
                player.actions += -1
                self.assess_risk(GameBoard)
            #If the player is a medic...
            elif  player.role == "Medic":
                #Grab the number of cubes of the chosen color off the city
                cubes = self.disease_tokens[color_int]
                #Return them to the cubes_remaining pool
                GameBoard.cubes_remaining[color_int] += cubes
                #and wipe them off the city
                self.disease_tokens[color_int] = 0
                player.actions += -1
                self.assess_risk(GameBoard)
            #If the player is not a medic and the disease isn't cured
            else:
                #remove one cube and place it back in the cubes_remaining pool
                self.disease_tokens[color_int] += -1
                GameBoard.cubes_remaining[color_int] += 1
                player.actions += -1
                self.assess_risk(GameBoard)

            
    #The game itself infects the city.  *args are, optionally, the color
    #of the disease being added.
    def infect(self, GameBoard, Players, *args):
        #Grab the color to add, if there are any args.
        if (len(args)>0):
            color = int(args[0])
        #Otherwise use the city's own color.
        else:
            color = self.color
        #if the disease has been eradicated, abort the infect.
        if GameBoard.cures[color] == GameBoard.terms["eradicated"]:
            return
        #Loop through all players
        for i in xrange(len(Players)):
            #Check for medics in the city when the disease has been cured
            if Players[i].role == "Medic":
                if GameBoard.cures[color] > GameBoard.terms["uncured"]:
                    if GameBoard.cities[Players[i].location] == self:
                        #Abort the infect
                        return
            #If there is a Quarantine Specialist...
            elif Players[i].role == "Quarantine":
                #Get the quarantine specialist's location
                city = GameBoard.cities[Players[i].location]
                #Check to see if this city is connected to their location
                if self.name in city.city_connections:
                    #and abort if it is.
                    return
        #Check to see if an Outbreak will occur now.
        if self.disease_tokens[color] == 3:
            self.outbreak(GameBoard, Players)
            self.assess_risk(GameBoard)
        else:
            #Otherwise, add one cube of the chosen color to the city
            self.disease_tokens[color] += 1
            #and remove it from Cubes_remaining.
            GameBoard.cubes_remaining[color] += -1
            if GameBoard.cubes_remaining[color] <= 0:
                GameBoard.cubes_remaining[color] = -24
                GameBoard.check_if_game_over()
            self.assess_risk(GameBoard)
                
            
        
    #The game itself makes the city Outbreak.
    def outbreak(self, GameBoard, Players):
        if self.outbroken == 0:
            print "Outbreak at", self.name
            self.outbroken = 1
            for city_name, distance in self.city_connections.iteritems():
                if distance == 1:
                    city = GameBoard.cities[city_name]
                    city.infect(GameBoard, Players, self.color)
        else:
            return



class Atlanta(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 1
        self.city_connections = {"Atlanta": 0,
                                 "Chicago": 1,
                                 "Washington": 1,
                                 "Miami": 1}
class Washington(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Washington": 0,
                                 "Atlanta": 1,
                                 "Montreal": 1,
                                 "NewYork": 1}
class SanFrancisco(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"SanFrancisco": 0,
                                 "Tokyo": 1,
                                 "Manila": 1,
                                 "LosAngeles": 1,
                                 "Chicago": 1}
class Chicago(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Chicago": 0,
                                 "SanFrancisco": 1,
                                 "MexicoCity": 1,
                                 "Atlanta": 1,
                                 "LosAngeles": 1,
                                 "Montreal": 1}
class Montreal(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Montreal": 0,
                                 "Chicago": 1,
                                 "Washington": 1,
                                 "NewYork": 1}
class NewYork(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"NewYork": 0,
                                 "Montreal": 1,
                                 "Washington": 1,
                                 "London": 1,
                                 "Madrid": 1}
class London(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"London": 0,
                                 "NewYork": 1,
                                 "Madrid": 1,
                                 "Paris": 1,
                                 "Essen": 1}
class Madrid(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Madrid": 0,
                                 "NewYork": 1,
                                 "London": 1,
                                 "SaoPaulo": 1,
                                 "Algiers": 1,
                                 "Paris": 1}
class Paris(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Paris": 0,
                                 "Madrid": 1,
                                 "London": 1,
                                 "Essen": 1,
                                 "Milan": 1,
                                 "Algiers": 1}
class Essen(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Essen": 0,
                                 "London": 1,
                                 "Paris": 1,
                                 "Milan": 1,
                                 "StPetersburg": 1}
class Milan(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Milan": 0,
                                 "Essen": 1,
                                 "Paris": 1,
                                 "Istanbul": 1}

class StPetersburg(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"StPetersburg": 0,
                                 "Essen": 1,
                                 "Istanbul": 1,
                                 "Moscow": 1}

class LosAngeles(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"LosAngeles": 0,
                                 "SanFrancisco": 1,
                                 "MexicoCity": 1,
                                 "Chicago": 1,
                                 "Sydney": 1}

class MexicoCity(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"MexicoCity": 0,
                                 "LosAngeles": 1,
                                 "Chicago": 1,
                                 "Miami": 1,
                                 "Lima": 1,
                                 "Bogota": 1}
class Miami(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Miami": 0,
                                 "MexicoCity": 1,
                                 "Bogota": 1,
                                 "Atlanta": 1,
                                 "Washington": 1}
class Bogota(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Bogota": 0,
                                 "MexicoCity": 1,
                                 "Lima": 1,
                                 "BuenosAires": 1,
                                 "SaoPaulo": 1,
                                 "Miami": 1}
class Lima(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Lima": 0,
                                 "MexicoCity": 1,
                                 "Bogota": 1,
                                 "Santiago": 1}
class Santiago(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Santiago": 0,
                                 "Lima": 1}
class BuenosAires(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"BuenosAires": 0,
                                 "Bogota": 1,
                                 "SaoPaulo": 1}
class SaoPaulo(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"SaoPaulo": 0,
                                 "Bogota": 1,
                                 "BuenosAires": 1,
                                 "Madrid": 1,
                                 "Lagos": 1}
class Lagos(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Lagos": 0,
                                 "SaoPaulo": 1,
                                 "Kinsasha": 1,
                                 "Khartoum": 1}

class Kinsasha(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Kinsasha": 0,
                                 "Lagos": 1,
                                 "Khartoum": 1,
                                 "Johannesburg": 1}
class Johannesburg(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Johannesburg": 0,
                                 "Khartoum": 1,
                                 "Kinsasha": 1}
class Khartoum(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Khartoum": 0,
                                 "Lagos": 1,
                                 "Kinsasha": 1,
                                 "Johannesburg": 1,
                                 "Cairo": 1}
class Algiers(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Algiers": 0,
                                 "Madrid": 1,
                                 "Paris": 1,
                                 "Istanbul": 1,
                                 "Cairo": 1}
class Cairo(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Cairo": 0,
                                 "Algiers": 1,
                                 "Khartoum": 1,
                                 "Istanbul": 1,
                                 "Baghdad": 1,
                                 "Riyadh": 1}
class Istanbul(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Istanbul": 0,
                                 "Milan": 1,
                                 "Algiers": 1,
                                 "Cairo": 1,
                                 "Baghdad": 1,
                                 "Moscow": 1,
                                 "StPetersburg": 1}

class Moscow(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Moscow": 0,
                                 "StPetersburg": 1,
                                 "Istanbul": 1,
                                 "Tehran": 1}

class Baghdad(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Baghdad": 0,
                                 "Istanbul": 1,
                                 "Cairo": 1,
                                 "Riyadh": 1,
                                 "Karachi": 1,
                                 "Tehran": 1}

class Riyadh(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Riyadh": 0,
                                 "Cairo": 1,
                                 "Baghdad": 1,
                                 "Karachi": 1}

class Tehran(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Tehran": 0,
                                 "Moscow": 1,
                                 "Baghdad": 1,
                                 "Karachi": 1,
                                 "Delhi": 1}

class Karachi(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Karachi": 0,
                                 "Baghdad": 1,
                                 "Riyadh": 1,
                                 "Mumbai": 1,
                                 "Delhi": 1,
                                 "Tehran": 1}

class Mumbai(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Mumbai": 0,
                                 "Karachi": 1,
                                 "Delhi": 1,
                                 "Chennai": 1}

class Delhi(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Delhi": 0,
                                 "Tehran": 1,
                                 "Karachi": 1,
                                 "Mumbai": 1,
                                 "Chennai": 1,
                                 "Kolkata": 1}
class Chennai(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Chennai": 0,
                                 "Mumbai": 1,
                                 "Delhi": 1,
                                 "Kolkata": 1,
                                 "Bangkok": 1,
                                 "Jakarta": 1}

class Kolkata(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Kolkata": 0,
                                 "Delhi": 1,
                                 "Chennai": 1,
                                 "Bangkok": 1,
                                 "HongKong": 1}
class Bangkok(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Bangkok": 0,
                                 "Kolkata": 1,
                                 "Chennai": 1,
                                 "Jakarta": 1,
                                 "HoChiMinhCity": 1,
                                 "HongKong": 1}
class Jakarta(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Jakarta": 0,
                                 "Chennai": 1,
                                 "Sydney": 1,
                                 "Kolkata": 1,
                                 "HoChiMinhCity": 1,
                                 "HongKong": 1}
class Sydney(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Sydney": 0,
                                 "Jakarta": 1,
                                 "Manila": 1,
                                 "LosAngeles": 1}

class HoChiMinhCity(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"HoChiMinhCity": 0,
                                 "Bangkok": 1,
                                 "Jakarta": 1,
                                 "Manila": 1,
                                 "HongKong": 1}
class Manila(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Manila": 0,
                                 "HoChiMinhCity": 1,
                                 "Sydney": 1,
                                 "SanFrancisco": 1,
                                 "Taipei": 1,
                                 "HongKong": 1}
class HongKong(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"HongKong": 0,
                                 "HoChiMinhCity": 1,
                                 "Bangkok": 1,
                                 "Kolkata": 1,
                                 "Manila": 1,
                                 "Taipei": 1,
                                 "Shanghai": 1}
class Taipei(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Taipei": 0,
                                 "HongKong": 1,
                                 "Osaka": 1,
                                 "Manila": 1,
                                 "Shanghai": 1}
class Osaka(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Osaka": 0,
                                 "Tokyo": 1,
                                 "Taipei": 1}
class Tokyo(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Tokyo": 0,
                                 "Seoul": 1,
                                 "Osaka": 1,
                                 "SanFrancisco": 1,
                                 "Shanghai": 1}
class Seoul(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Seoul": 0,
                                 "Beijing": 1,
                                 "Tokyo": 1,
                                 "Shanghai": 1}
class Shanghai(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Shanghai": 0,
                                 "Beijing": 1,
                                 "Seoul": 1,
                                 "Tokyo": 1,
                                 "Taipei": 1,
                                 "HongKong": 1}
class Beijing(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.cubes_placed = 1
        self.draw_chance = 0
        self.research_station = 0
        self.city_connections = {"Beijing": 0,
                                 "Seoul": 1,
                                 "Shanghai": 1}

class Player(object):
    def __init__(self, role):
        self.location = "Atlanta"
        self.role = role
        self.actions = 4
        self.stored = 0
        self.hand = []
        
    def player_info(self, GameBoard):
        print "Role:          ", self.role
        print "Location:      ", self.location
        self.a = "Hand:           "
        for card in self.hand:
            if card in GameBoard.city_index:
                self.color = GameBoard.cities[card].color
                self.a += card + " ("+GameBoard.terms[self.color] + ")"
            else:
                self.a += card
            self.a += ", "
        print self.a
        print "Actions left:  ", self.actions
        if self.role == "Contingency":
            print "Stored Event:  ", self.stored
        elif self.role == "Operations":
            print "Op. Flights:   ", self.stored
        print

    def print_hand(self, GameBoard):
        self.a = ""
        for card in self.hand:
            if card in GameBoard.city_index:
                self.color = GameBoard.cities[card].color
                self.a += card + " ("+GameBoard.terms[self.color] + ")"
            else:
                self.a += card
            self.a += ", "
        print self.a
        
        

#This method creates a 2d array of distances.  It is detailed below the method.
def create_distances(cities, city_index):
    size = len(city_index)
    distance = np.zeros(shape = (size,size), dtype=int)
    previous = np.zeros(shape = (size,size), dtype=int)
    for home_name in city_index:
        for destination_name in city_index:
            home_index = city_index.index(home_name)
            destination_index = city_index.index(destination_name)
            if home_name == destination_name:
                distance[home_index,destination_index] = 0
                previous[home_index,destination_index] = destination_index
            elif destination_name in cities[home_name].city_connections:
                distance[home_index,destination_index] = 1
                previous[home_index,destination_index] = home_index
            else:
                distance[home_index,destination_index] = 48
                previous[home_index,destination_index] = -1
    for intermediary_name in city_index:
        for home_name in city_index:
            for destination_name in city_index:
                home_index = city_index.index(home_name)
                destination_index = city_index.index(destination_name)
                intermediary_index = city_index.index(intermediary_name)
                d1 = distance[home_index, intermediary_index]
                d2 = distance[intermediary_index, destination_index]
                d3 = distance[home_index, destination_index]
                if d1 + d2 < d3:
                    d3 = d1 + d2
                    distance[home_index, destination_index] = d3
                    previous[home_index, destination_index] = intermediary_index
    return [distance, previous]

#This method takes two city objects, Home and Destination.
def get_path(home, destination, GameBoard):
    if home == destination or destination.name in home.city_connections:
        #print home, "neighbors", destination, "so exiting recursion"
        return destination
    else:
        home_index = GameBoard.city_index.index(home.name)
        destination_index = GameBoard.city_index.index(destination.name)
        next_index = GameBoard.previous[home_index, destination_index]
        #print GameBoard.city_index[next_index]
        next_city = GameBoard.cities[GameBoard.city_index[next_index]]
        path = get_path(home, next_city, GameBoard)
        if home == path or path.name in home.city_connections:
            #print home, "neighbors", path, "on the way to", destination, "so exiting recursion"
            return path

#distance grid:
#J is the source city, I is the intermediary, K is the destination.
#i goes from 1 to 48, j goes from 1 to 48; this is x and y in a grid.
#The i,j coordinates are the shortest known distances (currently) from i to j
#initialize the matrix such that i to i is 0, i to a neighbor (rip these from
#the current city info) is 1, and i to everything else is 9 (I think that's the
#max pathing distance from any one node to another)
#if the distance from i to j is less than infinity, then check to see J's path
#to every other city (k goes from 1 to 48), and if the distance from (J to I) +
#(I to K) is less than the current distance from J to k
#set the dist of J to K to be that sum.
#set prev(j,k)=i.

#SECOND 2d array, this one storing an intermediary; initialize it such that I
#to I = i, i to j (if they're neighbors) = i, and everything else is undefined
#and will be defined later.


#to find distance, use one 2d array; to find direction, use two 2d arrays- one
#to store the distance, one to store the previous location between i and k
#prev(j,k) returns one step on the way from j to k.  if j=k, return k; if k
#neighbors j, then return k.  If neither, call this function on (i, prev(i,k).
#Recursively call until one of the two initial conditions are met.


#This simple method shuffles any list it is given and returns it.  it takes as
#arguments a list.  It modifies no variables.
def shuffle(givenList):
    #Create a blank list
    shuffledList = []
    #For each card in the given list...
    while (len(givenList)>0):
        #Grab one at random and add it to the blank list
        random_int = np.random.random_integers(0,len(givenList)-1)
        shuffledList.append(givenList.pop(random_int))
    #Then return the formerly-blank list
    return shuffledList


#Super-class top-of-the-line object which controls the game.  Simulate method
#will call this.
class Pandemic(object):
    
    epidemic_chance = 1.0
    epidemic_drawn = False
    
    def __init__(self, player_count, difficulty):
        self.create_game(player_count, difficulty)
        self.find_epidemic_chance()
        self.update_draw_chance()
        
    #Create the game!
    def create_game(self, player_count, difficulty):
        #Make the board, and shuffle its player_deck, infect_deck, and roles.
        self.GameBoard = GameBoard(self)
        self.GameBoard.reset_game()
        self.GameBoard.player_deck = shuffle(self.GameBoard.player_deck)
        self.GameBoard.infect_deck = shuffle(self.GameBoard.infect_deck)
        self.GameBoard.roles = shuffle(self.GameBoard.roles)

        #Create the Player list
        self.Players = []
        #determine the number of cards in each player's starting hand.
        self.hand_size = 9 / player_count
        #For each player
        for i in xrange(player_count):
            #Create a new player with a random role
            self.player = Player(self.GameBoard.roles.pop())
            print "Player", i, "drew the", self.player.role, "card!"
            self.player.location = "Atlanta"
            #Deal the player a hand of cards
            for j in xrange(self.hand_size):
                self.player.hand.append(self.GameBoard.player_deck.pop())
            #And add the player to the Player list.
            self.Players.append(self.player)

        #Generate the game's player deck: split it into as many smaller piles
        #as there are Epidemic cards (the Difficulty), add one Epidemic to each,
        #shuffle them, and then stack them together to create the player deck.

        #Find the size of each cut of the player deck
        self.pile_size = len(self.GameBoard.player_deck) / difficulty
        #Find any remaining cards after the deck is divided up.
        self.remaining_cards = len(self.GameBoard.player_deck) % difficulty
        #create a temporary list to hold the cuts while they're being made.
        self.combined_cuts = []
        #For each Epidemic card to be added to the deck
        for i in xrange(difficulty):
            #Create an empty cut of the player_deck
            self.cut = []
            #And add cards until it's the right size
            for j in xrange(self.pile_size):
                self.cut.append(self.GameBoard.player_deck.pop(0))
            #Top it up from the remaining_cards count
            if self.remaining_cards > 0:
                self.cut.append(self.GameBoard.player_deck.pop(0))
                #and reduce that count so it doesn't happen too many times.
                self.remaining_cards += -1
            #Give it an epidemic
            self.cut.append("Epidemic")
            #Shuffle it, and add it to the combined cuts pile
            self.combined_cuts += shuffle(self.cut)
        #Lastly, update the GameBoard's player_deck.
        self.GameBoard.player_deck = self.combined_cuts

        #This for loop infects three cities with 3 cubes, three with 2 and 3
        #with 1 as part of the board's initial setup.  The cards are discarded
        #to the infect_discard pile.
        for i in xrange(9):
            self.card = self.GameBoard.infect_deck.pop(0)
            self.city = self.GameBoard.cities[self.card]
            self.GameBoard.infect_discard.append(self.card)
            if i < 3:
                self.city.infect(self.GameBoard, self.Players)
                self.city.infect(self.GameBoard, self.Players)
                self.city.infect(self.GameBoard, self.Players)
                print self.city.name, "is", self.GameBoard.terms[self.city.color], "and was infected thrice."
            elif i > 2 and i < 6:
                self.city.infect(self.GameBoard, self.Players)
                self.city.infect(self.GameBoard, self.Players)
                print self.city.name, "is", self.GameBoard.terms[self.city.color], "and was infected twice."
            else:
                self.city.infect(self.GameBoard, self.Players)
                print self.city.name, "is", self.GameBoard.terms[self.city.color], "and was infected once."
        self.update_draw_chance()

    def find_epidemic_chance(self):
        self.cards_left = 0
        if self.epidemic_drawn:
            epidemic_chance = 0
        else:
            self.cards_left = len(self.GameBoard.player_deck) % self.pile_size
            self.epidemic_chance = (1.0 / self.cards_left)

    def update_draw_chance(self):
        for city_name in self.GameBoard.cities.keys():
            self.GameBoard.cities[city_name].find_draw_chance(self.GameBoard)

    def draw_board(self):
        for city_tuple in self.GameBoard.cities.iteritems():
            self.city = self.GameBoard.cities[city_tuple[0]]
            self.city.print_city(self.GameBoard)
            for i in xrange(len(self.Players)):
                if self.Players[i].location == city_tuple[0]:
                    print self.Players[i].role, "(",i,") is in this city."
            print
        print
        print "Outbreak Marker: ", self.GameBoard.outbreak_marker
        if self.GameBoard.outbreak_marker > 5:
            print "If the outbreak marker reaches 8, the game ends!"
        print
        print "Infection Rate: ", self.GameBoard.infection_rate_marker
        if self.GameBoard.one_quiet_night_marker != 0:
            print "One Quiet Night in effect: no cities infected this turn"
        elif self.GameBoard.infection_rate_marker < 3:
            print "Cities infected per Turn: 2"
        elif self.GameBoard.infection_rate_marker > 2:
            print "Cities infected per Turn: 3"
        elif self.GameBoard.infection_rate_marker > 5:
            print "Cities infected per Turn: 4"
        print
        print "Cubes remaining (Blue, Yellow, Black, Red):"
        print self.GameBoard.cubes_remaining
        print
        print "Cards of each color remaining (Blue, Yellow, Black, Red):"
        print self.GameBoard.card_colors_remaining
        print
        print "Cures Found:"
        if self.GameBoard.cures[0] == 0:
            print "Blue: Uncured"
        elif self.GameBoard.cures[0] == 1:
            print "Blue: Cured"
        elif self.GameBoard.cures[0] == 2:
            print "Blue: Eradicated"
        if self.GameBoard.cures[1] == 0:
            print "Yellow: Uncured"
        elif self.GameBoard.cures[1] == 1:
            print "Yellow: Cured"
        elif self.GameBoard.cures[1] == 2:
            print "Yellow: Eradicated"
        if self.GameBoard.cures[2] == 0:
            print "Black: Uncured"
        elif self.GameBoard.cures[2] == 1:
            print "Black: Cured"
        elif self.GameBoard.cures[2] == 2:
            print "Black: Eradicated"
        if self.GameBoard.cures[3] == 0:
            print "Red: Uncured"
        elif self.GameBoard.cures[3] == 1:
            print "Red: Cured"
        elif self.GameBoard.cures[3] == 2:
            print "Red: Eradicated"
        print
        print "Cities in the Intensify Pile (likely to be drawn again soon):"
        for i in self.GameBoard.intensify_list:
            print i
        print
        print "Cities in the Infect Discard Pile:"
        for i in self.GameBoard.infect_discard:
            print i
        print
        print "Cities in the Player Discard Pile:"
        for i in self.GameBoard.player_discard:
            print i
        print
        for i in self.Players:
            print i.player_info(self.GameBoard)
       
            
def allowable_actions(active_player, Pandemic):
    GameBoard = Pandemic.GameBoard
    location = GameBoard.cities[active_player.location]
    print "With this action, you can..."
    for key in location.city_connections.keys():
        print "Walk to", key
    if location.research_station > 0:
        if GameBoard.research_stations.count(-1) < 6:
            for city in GameBoard.research_stations:
                if city != -1:
                    print "Shuttle Fly to", city.name
    if len(active_player.hand) > 0:
        for i in xrange(len(active_player.hand)):
            if active_player.hand[i] in GameBoard.city_index:
                if active_player.hand[i] != location.name:
                    if active_player.hand[i] not in location.city_connections:
                        print "Fly directly to", active_player.hand[i]
            elif active_player.hand[i] in GameBoard.events:
                print "Use", active_player.hand[i]
        if active_player.location in active_player.hand:
            if location.research_station == 0:
                print "Build research station in", active_player.location
            else:
                print "Charter Fly to [any other city]"
        blues = 0
        yellows = 0
        blacks = 0
        reds = 0
        for i in xrange(len(active_player.hand)):
            if active_player.hand[i] in GameBoard.city_index:
                city = GameBoard.cities[active_player.hand[i]]
                if city.color == GameBoard.terms["blue"]:
                    blues += 1
                elif city.color == GameBoard.terms["yellow"]:
                    yellows += 1
                elif city.color == GameBoard.terms["black"]:
                    blacks += 1
                elif city.color == GameBoard.terms["red"]:
                    reds += 1
        if active_player.role == "Scientist":
            if blues > 3:
                print "Cure Blue Disease!"
            if yellows > 3:
                print "Cure Yellow Disease!"
            if blacks > 3:
                print "Cure Black Disease!"
            if reds > 3:
                print "Cure Red Disease!"
        else:
            if blues > 4:
                print "Cure Blue Disease!"
            if yellows > 4:
                print "Cure Yellow Disease!"
            if blacks > 4:
                print "Cure Black Disease!"
            if reds > 4:
                print "Cure Red Disease!"
        for i in Pandemic.Players:
            if i.location == active_player.location:
                if i.role == "Researcher":
                    print "Share any city card with the Researcher at your location."
                elif active_player.role == "Researcher":
                    print "Share any city card with the other player at your location."
                else:
                    if location.name in i.hand:
                        print "Take the city card for your location from another player."
                    elif location.name in active_player.hand:
                        print "Give the city card for your location to another player."
        if active_player.role == "Operations":
            a = "Operations Fly to any other city by discarding"
            b = " any city's card!"
            a= a + b
            print a
            a = "The discarded card and the destination do not"
            b = " need to be the same."
            a = a + b
            print a
    if active_player.role == "Dispatcher":
        print "Move any other player as if they were your piece!"
    elif active_player.role == "Contingency":
        if GameBoard.events in GameBoard.player_discard:
            print "Draw a used Event card from the Discard pile and attach it to your piece!"
    if location.disease_tokens > [0,0,0,0]:
        print "Treat disease at your location."
                

#This method is called at the end of every turn: it takes the infection rate
#as an argument, draws 2, 3, or 4 cards from the Infect Deck, and infects
#them, potentially causing Outbreaks.
def infection_stage(GameBoard, Players):
    #Clear the outbreak list before infecting, just in case.
    GameBoard.outbreak_list = []
    #Draw a card from the Infect Deck
    index = GameBoard.infect_deck.pop(0)
    GameBoard.infected_cities[3] = index
    #Infect the card's city and update gameBoard
    GameBoard.cities[index].infect(GameBoard, Players)
    #Discard the drawn card to the Infect Discard Pile
    GameBoard.infect_discard.append(index)
    #if the card is in the Intensify pile, remove it.
    if index in GameBoard.intensify_list:
        i = GameBoard.intensify_list.index(index)
        GameBoard.intensify_list.pop(i);
    #Clear the outbreak list again, because we aren't done yet.
    GameBoard.outbreak_list = []
    #Rinse and repeat at least once.
    index = GameBoard.infect_deck.pop(0)
    GameBoard.infected_cities[4] = index
    GameBoard.cities[index].infect(GameBoard, Players)
    GameBoard.infect_discard.append(index)
    GameBoard.outbreak_list = []
    #If the infection rate is 2 or more, infect one more city
    if GameBoard.infection_rate_marker > 2:
        index = GameBoard.infect_deck.pop(0)
        GameBoard.infected_cities[5] = index
        GameBoard.cities[index].infect(GameBoard, Players)
        GameBoard.infect_discard.append(index)
        GameBoard.outbreak_list = []
    #If the Infection Rate is 6 or more, infect a fourth city.
    if GameBoard.infection_rate_marker > 5:
        index = GameBoard.infect_deck.pop(0)
        GameBoard.infected_cities[6] = index
        GameBoard.cities[index].infect(GameBoard, Players)
        GameBoard.infect_discard.append(index)
        GameBoard.outbreak_list = []





#This method is called when an Epidemic card is drawn by a player.  More
#accurately, this method increments the Infection Rate marker by one, draws an
#Infect card from the bottom of the Infect Deck, infects that city three times,
#and then takes all the cards out of the Infection Discard pile, shuffles them,
#and puts them back ontop of the Infect Deck so they can be drawn again and
#really kick the player's teeth in.
def epidemic(GameBoard, Players):
    #Increment the Infection Rate Marker.  Everything just got tougher!
    GameBoard.infection_rate_marker += 1
    #Draw the bottom card from the Infect Deck.
    epidemic_city = GameBoard.infect_deck.pop()
    if (GameBoard.Pandemic.epidemic_drawn):
        GameBoard.infected_cities[1] = epidemic_city
    else:
        GameBoard.infected_cities[0] = epidemic_city        
    #And infect it three times, updating the game board each time.
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    #Then discard the card to the Infect Discard Pile
    GameBoard.infect_discard.append(epidemic_city)
    #Clear the Intensify list: while not technically part of the game rules,
    #tracking which cards went back onto the Infect Deck is an essential part
    #of winning the game.
    GameBoard.intensify = []
    #Then, loop through the entire Infect Discard Pile
    while (len(GameBoard.infect_discard)>0):
        #grab one card from it at random
        card = GameBoard.infect_discard.pop(
            np.random.random_integers(0,len(GameBoard.infect_discard)-1))
        #Add the card to the Intensify list so the AI will know it's coming up
        #very soon
        GameBoard.intensify.append(card)
        #and place the card ontop of the Infect Deck
        GameBoard.infect_deck.insert(0,card)
    #Shuffle the Intensify list so the order the cards were placed on the
    #Infect Deck is obscured.
    GameBoard.intensify = shuffle(GameBoard.intensify)
    #Note that an epidemic happened this turn
    GameBoard.epidemic_this_turn()
    #And finally, if One Quiet Night hasn't been played...
    if GameBoard.one_quiet_night_marker == 0:
        #Infect.
        infection_stage(GameBoard, Players)




#This method allows a player to start to move.  It takes as arguments the
#player being moved, the destination the player has in mind, and a possible
#additional argument of the number of steps to make (if the player does not
#wish to move all the way to a distant destination this turn and has other
#actions in mind), and the Dispatcher who may be using their action to pay
#for the movement instead of the player being moved.
def move_player(GameBoard, player, destination_name, *args):
    if len(args) == 0:
        #Without arguments, the method assumes the player wishes to get to their
        #destination as quickly as possible and uses all remaining actions to do
        #so until they get to their destination.
        while player.actions > 0 and player.location != destination_name:
            #Move the player one step towards their destination, getting pathing
            #info from get_path.
            origin = GameBoard.cities[player.location]
            #print origin, origin.name
            destination = GameBoard.cities[destination_name]
            #print destination, destination.name
            path = get_path(origin, destination, GameBoard)
            move_action(GameBoard, player, path)
    if len(args) == 1:
        #The first optional argument will always be the number of actions the
        #player wishes to spend on movement.
        steps = int(args[0])
        #for each action...
        for i in xrange(steps):
            #check to see if the player has enough remaining actions...
            if player.actions > 0 and player.location != destination_name:
                #and then move them using the info from get_path.
                origin = GameBoard.cities[player.location]
                #print origin, origin.name
                destination = GameBoard.cities[destination_name]
                #print destination, destination.name
                path = get_path(origin, destination, GameBoard)
                #print path
                move_action(GameBoard, player, path)
    #If there's more than one argument provided (with no error proofing, of
    #course!), then we assume it's a Dispatcher using his actions to move
    #another player!
    else:
        #Grab the number of actions the Dispatcher wants to spend...
        steps = int(args[0])
        #and the Dispatcher's player object, too, while we're at it.
        dispatcher = args[1]
        #Then, for each action indicated in Steps...
        for i in xrange(steps):
            #make sure the Dispatcher has enough actions and the player hasn't
            #arrived...
            if dispatcher.actions > 0 and player.location != destination_name:
                #and move the player if he does, adding the additional argument
                #of the dispatcher's player list to the move_action method call.
                origin = GameBoard.cities[player.location]
                destination = GameBoard.cities[destination_name]
                path = get_path(origin, destination, GameBoard)
                move_action(GameBoard, player, path, dispatcher)


#This method is what actually handles the walking part of movement.  It takes
#arguments of the player being moved, the player's destination, and, optionally,
#the dispatcher who will be paying for the movement with his Actions.
def move_action(GameBoard, player, destination, *args):
    #Get the destination city's name first thing.
    destination_name = destination.name
    #If there's no dispatcher paying for the movement...
    if len(args) == 0:
        #check (again) to see the player has the actions for this movement
        if player.actions > 0 and player.location != destination_name:
            #grab the player's current location
            location = GameBoard.cities[player.location]
            #look through the player's location's list of neighbors...
            if destination_name in location.city_connections:
                #Move the player there,
                player.location = destination_name
                #and consume one of the player's actions.
                player.actions += -1
    #If there is a dispatcher paying for the movement...
    else:
        #Get the kind soul's player list from *args- again, no error checking!
        dispatcher = args[0]
        #Verify (again) that the Dispatcher has the actions for this movement...
        if dispatcher.actions > 0 and player.location != destination_name:
            #save the player (not dispatcher) location.
            location = GameBoard.cities[player.location]
            #Check all of that locations' neighbors.
            if destination_name in location.city_connections:
                #Move the player there,
                player.location = destination_name
                #and consume one of the Dispatcher's actions.
                dispatcher.actions += - 1


#This method is Direct Flight, one of the more useful means of travel around the
#board.  This method takes as arguments the player, the index of the city the
#player wishes to fly to, and, optionally, the Dispatcher who is paying for the
#player's movement.
def direct_flight(GameBoard, player, destination_name, *args):
    #No dispatcher, so pay your own way...
    if len(args) == 0:
        #Action check!
        if player.actions > 0:
            #look through the list of cards that is the player's hand for the
            #destination city's card...
            if destination_name in player.hand:
                #If it is, note that a card of the city's color has been
                #discarded using the colorsRemaining list.
                color = GameBoard.cities[destination_name].color
                GameBoard.card_colors_remaining[color] += -1
                #Then discard the city card to the Player Discard pile
                index = player.hand.index(destination_name)
                GameBoard.player_discard.append(player.hand.pop(index))
                #Update the player's location to the destination
                player.location = destination_name
                #And consume one of the player's actions.
                player.actions += - 1
    #If there IS a dispatcher...
    else:
        #Grab his player list.
        dispatcher = args[0]
        #Check he has the actions...
        if dispatcher.actions > 0:
            #Loop through the dispatcher's hand
            if destination_name in dispatcher.hand:
                #These few lines are identical to the four above except that the
                #dispatcher discards the city card and loses the action
                color = GameBoard.cities[destination_name].color
                GameBoard.card_colors_remaining[color] += -1
                index = player.hand.index(destination_name)
                GameBoard.player_discard.append(player.hand.pop(index))
                player.location = destination_name
                player.actions += - 1


#This method allows players to discard a city's card while in that city to fly
#to any other city on the game board.  It takes as arguments the player, the
#destination city's index, and, optionally, the dispatcher who will be paying
#for the movement.
def charter_flight(GameBoard, player, destination_name, *args):
    #No dispatcher
    if len(args) == 0:
        #Action check
        if player.actions > 0:
            #Loop through the player's hand for the card of his current location
            if player.location in player.hand:
                #note that a card of that city's color has been discarded
                color = GameBoard.cities[player.location].color
                GameBoard.card_colors_remaining[color] += -1
                #Discard the card
                index = player.hand.index(player.location)
                GameBoard.player_discard.append(player.hand.pop(index))
                #Move the player to the new location
                player.location = destination_name
                #Consume one action.
                player.actions += -1
                
    #This section is identical to the one above, save that the Dispatcher
    #uses his action and discards the city card, not the player being moved.
    else:
        dispatcher = args[0]
        if dispatcher.actions > 0:
            #Loop through the player's hand for the card of his current location
            if player.location in dispatcher.hand:
                color = GameBoard.cities[player.location].color
                GameBoard.card_colors_remaining[color] += -1
                index = dispatcher.hand.index(player.location)
                GameBoard.player_discard.append(dispatcher.hand.pop(index))
                player.location = destination_name
                dispatcher.actions += -1


#This method allows players to fly from one city to another, so long as both
#cities have Research Stations in them.  It takes arguments of the player
#who will be moving, the destination city's index, and, optionally, the
#dispatcher who will be paying for the movement.
def shuttle_flight(GameBoard, player, destination_name, *args):
    #No dispatcher
    if len(args) == 0:
        #If the player's location has a research station, the destination has a
        #Research Station, and the player has actions remaining this turn...
        if GameBoard.research_stations.count(player.location) > 0:
            if GameBoard.research_stations.count(destination_name) > 0:
                 if player.actions > 0:
                    #Move the player to the destination city
                    player.location = destination_name
                    #And consume one action
                    player.actions += -1
                    return
    #If there is a dispatcher, do the above, but the Dispatcher pays for
    #the movement instead.
    else:
        dispatcher = args[0]
        if GameBoard.research_stations.count(player.location) > 0:
            if GameBoard.research_stations.count(destination_name) > 0:
                if dispatcher.actions > 0:
                    player.location = destination_name
                    dispatcher.actions += -1
                    return


#this method allows a Dispatcher to move one player to any other player on the
#board.  It takes as arguments the dispatcher's player list, the moving player's
#player list, and the destination of the flight.
def dispatch_flight(GameBoard, Players, dispatcher, player, destination_name):
    #If the dispatcher has enough actions...
    if dispatcher.actions > 0:
        #loop through the list of all players.
        for i in xrange(len(Players)):
            #if the destination index is also the location of a player,
            if destination_name == Players[i].location:
                #Consume one of the dispatcher's actions,
                dispatcher.actions += -1
                #and move the player to its new location.
                player.location = Players[i].location
                break


#This method allows Operations Experts to fly from any city with a Research
#Station to any other city on the map at the price of any one card.  It takes,
#as arguments, a player list, the index of the destination city, and the index
#of the card being discarded for this travel.
def operations_flight(GameBoard, player, destination_name, discard_index):
    #If the player has an action remaining, has not used this move this turn,
    #and is an Opeations Expert.
    if player.actions > 0 and player.stored == 0:
        if player.role == "Operations":
            if GameBoard.cities[player.location].research == 1:
                #Note the color of the card being discarded in ColorsRemaining
                color = GameBoard.cities[player.hand[discard_index]].color
                GameBoard.card_colors_remaining[color] += -1
                #Discard the card to the playerDiscard pile
                GameBoard.player_discard.append(player.hand.pop(discard_index))
                #move the Operations Expert to his new location
                player.location = destination_name
                #Consume one action
                player.actions += -1
                #and note that the Operations Expert used Operations Flight
                #this turn.
                player.stored = 1
            else:
                print "Need to be in a city with a Research Station to do this."
        else:
            print "Need to be an Operations Expert to do this."
    else:
        print "Not enough actions- or already did an Operations flight this turn!"




#This method allows a player to spend one action to give another player the
#city card of the city they are BOTH in, unless the giver is a Researcher; then
#she can give any city card she damn well pleases to.  It takes, as arguments,
#the player list of the giving player, the player list of the receiving player,
#and the index number of the card being given in the giver's hand.
def give_knowledge(giver, receiver, card_index):
    #If the giver and receiver are in the same city, the giver is a Researcher,
    #and the giver has at least one action left this turn...
    if (giver.location == receiver.location):
        if giver.role == "Researcher" and giver.actions > 0:
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver.hand.append(giver.hand.pop(card_index))
            #Consume one of the giver's actions
            giver.actions += -1
    #If the giver and receiver are in the same location and the giver can act,
    elif giver.location == receiver.location and giver.actions > 0:
        #and if the giver's location and the card are the same city...
        if giver.hand[card_index] == giver.location:
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver.hand.append(giver.hand.pop(card_index))
            #consume one action from the giver
            giver.actions = giver.actions - 1


#This method allows players to do the same as above, except the receiver spends
#the action instead of the giver.  This method takes arguments of the giver's
#player list, the receiver's player list, and the index of the card being taken
#This modifies no global variables- hooray!
def take_knowledge(giver, receiver, card_index):
    #If the giver is a Researcher, is in the same city as the Receiver,
    #and the receiver can act
    if (giver.location == receiver.location and receiver.actions > 0):
        if giver.role == "Researcher":
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver.hand.append(giver.hand.pop(card_index))
            #consume one of the receiver's actions
            receiver.actions = receiver.actions - 1
    #If the giver and receiver are in the same city, and the receiver can act
    elif giver.location == receiver.location and receiver.actions > 0:
        #...and if the card being given matches their location
        if giver.hand[card_index] == giver.location:
            #Do the same as above.
            receiver.hand.append(giver.hand.pop(card_index))
            receiver.actions = receiver.actions - 1


#This method allows players to Cure diseases by discarding five cards of the
#same color as the disease they are curing- or four cards, if the player is a
#Scientist.  This method takes, as arguments, a player list, and four or five
#args, each of which are the index location of one of the cards being discarded
def cure(GameBoard, player, *args):
    #If the player is a scientist, has an action, and is at a research station
    if player.role == "Scientist" and player.actions > 0:
        if GameBoard.cities[player.location].research == 1:
            #Create a list of the cities whose cards are being discarded...
            #these index values are each off by one.
            cities = [GameBoard.cities[args[0]], GameBoard.cities[args[1]],
                      GameBoard.cities[args[2]], GameBoard.cities[args[3]]]
            #loop through that list... this should probably be -1, not -2
            for i in xrange(len(cities)-1):
                #If one city's color does not match the next city's color...
                if cities[i].color != cities[i+1].color:
                    #Abort the cure; they're the wrong cards!
                    return
        #Otherwise, cure the disease!
        color = GameBoard.cities[args[0]].color
        GameBoard.cures[color] = GameBoard.terms["cured"]
        #Consume one action
        player.actions += -1
        #discard each card
        GameBoard.player_discard.append(player.hand.index(args[0]))
        GameBoard.player_discard.append(player.hand.index(args[1]))
        GameBoard.player_discard.append(player.hand.index(args[2]))
        GameBoard.player_discard.append(player.hand.index(args[3]))
        #and note that they've been discarded in ColorsRemaining
        GameBoard.card_colors.remaining[color] += -4


    #If the player is not a scientist, but is in a research station...
    elif player.actions > 0 and GameBoard.cities[player.location].research == 1:
        #Create a list of the cities whose cards are being discarded...
        #These index values are also off by one.
        cities = [GameBoard.cities[args[0]], GameBoard.cities[args[1]],
                  GameBoard.cities[args[2]], GameBoard.cities[args[3]],
                  GameBoard.cities[args[4]]]
        #Loop through that list
        for i in xrange(len(cities)-1):
                #If one city's color does not match the next city's color...
                if cities[i].color != cities[i+1].color:
                    #Abort the cure; they're the wrong cards!
                    return
        #Otherwise, cure the disease!
        color = GameBoard.cities[args[0]].color
        GameBoard.cures[color] = GameBoard.terms["cured"]
        #Consume one action
        player.actions += -1
        #discard each card
        GameBoard.player_discard.append(player.hand.index(args[0]))
        GameBoard.player_discard.append(player.hand.index(args[1]))
        GameBoard.player_discard.append(player.hand.index(args[2]))
        GameBoard.player_discard.append(player.hand.index(args[3]))
        GameBoard.player_discard.append(player.hand.index(args[4]))
        #and note that they've been discarded in ColorsRemaining
        GameBoard.card_colors.remaining[color] += -5

                  
#This method allows a Contingency Planner to take one Event card out of the
#Discard pile and add it to his Player List for later use.  It takes as
#arguments the Contingency Planner's player list, and the event card he wishes
#to draw.
def contingency(GameBoard, player, event_card):
    #If the player's role is Contingency planner, the player has no other
    #event card stored, the event card he wants is in the discard pile, and
    #the contingency planner has enough actions...
    if player.role == "Contingency" and player.stored == 0:
        if GameBoard.player_discard.count(event_card) > 0:
            if player.actions > 0:
                #Draw the card out of the discard pile and attach it to the
                #player's object
                index = GameBoard.player_discard.index(event_card)
                player.stored = GameBoard.player_discard.pop(index)
                #and consume one action.
                player.actions += -1



#Event Cards:

#This method is the Resilient Population event card.  It allows players to
#remove one city's Infect card from the Infect Discard pile, and remove it from
#the game so it cannot be drawn again.  It takes as arguments the player list
#of the player with the card, and the index of the city card to be removed.
def resilient_population(GameBoard, player, card_to_remove):
    #Remove the infect card from the discard pile and poof it into the e-ther.
    GameBoard.infect_discard.pop(card_to_remove)
    #If the player is a Contingency planner with the card stored...
    if (player.role == "Contingency"):
        if player.stored == "Resilient Population":
            player.stored = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index("Resilient Population")
        GameBoard.player_discard.append(player.hand.pop(card_index))
        


#This method allows players to use the Airlift card to instantly fly any player
#to any city of their choosing!  It takes as arguments the player list of the
#player with the card, the player list of the player doing the flying, and the
#city index of the destination city.
def airlift(GameBoard, player, target, destination_name):
    #Set the target player's location to the destination.
    target.location = destination_name
    #If the player with the card is a contingency planner who stored the card
    if player.role == "Contingency":
        if player.stored == "Airlift":
            #Poof it into the e-ther.
            player.stored = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index("Airlift")
        GameBoard.player_discard.append(player.hand.pop(card_index))


#This event card allows a player to instantly build a research station anywhere
#on the game map.  It takes as arguments the player list of the player with the
#card, and the index of the city to get the shiny new research station.
def gov_grant(GameBoard, player, city_name, *args):
#Check that there isn't ALREADY a research station at this location...
    city = GameBoard.cities[city_name]
    if (city.research == 1):
        return
    #if there are any additional arguments given...
    elif (len(args) > 0):
        #take the first one and delete the research station located in
        #that city.
        city_to_remove = GameBoard.cities[args[0]]
        city_to_remove.research = 0
        #And remove the above city from the list of research stations
        index = research_stations.index(args[0])
        GameBoard.research_stations[index] = -1
    #If no argument for research station removal is provided and there
    #are six research stations already built...
    elif (len(args) != 1 and GameBoard.research_stations.count(-1) == 0):
        return
    
    #Build the research station at the destination.
    index = GameBoard.research_stations.index(-1)
    GameBoard.research_stations[index] = city_name
    GameBoard.cities[city_name].research = 1
    
    #Discard the card
    GameBoard.player_discard.append(player.hand.pop(discard_index))
    #If the player's a Contingency planner playing the card from storage
    if player.role == "Contingency":
        if player.stored == "Government Grant":
            #VANISH it.
            player.stored = 0
    #otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index("Government Grant")
        GameBoard.player_discard.append(player.hand.pop(card_index))


#This method allows players to skip the Infect stage on one turn.  It can be
#used to prevent an Epidemic from Infecting, but not from Intensifying.  It
#takes as arguments the player list of the player with the card and the game
#board.
def one_quiet_night(GameBoard, player):
    #Set the OneQuietNightMarker to 1, skipping the Infect stage.
    GameBoard.one_quiet_night_marker = 1
    #COntingency Planner card removal
    if player.role == "Contingency":
        if player.stored == "One Quiet Night":
            player.stored = 0
    else:
        #place the card in the player discard pile
        card_index = player.hand.index("One Quiet Night")
        GameBoard.player_discard.append(player.hand.pop(card_index))


#This method allows players to use the Forecast card, rearranging the top six
#cards in the Infect Deck to their liking.  It takes, as arguments, the player
#list of the player with the card, and the game board.
def forecast(GameBoard, player):
    #Draw the top six cards of the Infection Deck and put them in a list.
    topSix = [GameBoard.infect_deck.pop(0), GameBoard.infect_deck.pop(0),
              GameBoard.infect_deck.pop(0), GameBoard.infect_deck.pop(0),
              GameBoard.infect_deck.pop(0), GameBoard.infect_deck.pop(0)]
    #loop through that list once
    for i in xrange (len(topSix)):
        #If any of the cities have three cubes of any color on them...
        c = GameBoard.cities[topSix[i]]
        if c.disease_tokens[GameBoard.terms["blue"]] == 3:
            #Put them ontop first, popping them out of the list.
            #This might cause errors as the list length gets shorter...
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["red"]] == 3:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["yellow"]] == 3:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["black"]] == 3:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
    #Loop through the list again.
    for i in xrange (len(topSix)):
        #If any of the cities have two cubes of any color on them...
        c = GameBoard.cities[topSix[i]]
        if c.disease_tokens[GameBoard.terms["blue"]] == 2:
            #Put them ontop first, popping them out of the list.
            #This might cause errors as the list length gets shorter...
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["red"]] == 2:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["yellow"]] == 2:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
        elif c.disease_tokens[GameBoard.terms["black"]] == 2:
            #Repeat for every other color.
            GameBoard.infect_deck.insert(0, topSix.pop(i))
    #Loop through again,
    for i in xrange (len(topSix)):
        #And put the rest ontop by popping them out of the list
            GameBoard.infect_deck.insert(0, topSix.pop(i))
    #This puts the cities back ontop in reverse order of the number of cubes
    #they have: heavily-infected cities are drawn last, lightly infected ones
    #are drawn first.

    #Same Contignecny planner stuff.
    if player.role == "Contingency":
        if player.stored == "Forecast":
            player.stored = 0
    else:
        #place the card in the player discard pile
        card_index = player.hand.index("Forecast")
        GameBoard.player_discard.append(player.hand.pop(card_index))


#This method forces a player to discard one card from their hand.  It takes as
#arguments the player list of the unfortunate soul who has to discard a card.
def discard(GameBoard, player):
    while (len(player.hand) > 7):
        event_in_hand = False
        #Check for events in the player's hand
        for card in active_player.hand:
            if Pandemic.GameBoard.events.count(card) > 0:
                event_in_hand = True
        if event_in_hand:
            print "Would you like to use an Event Card?"
            input_note = "If not, type the name of the card to discard: "
            chosen_card = raw_input(input_note)
            if chosen_card in player.hand:
                card_index = player.hand.index(chosen_card)
                GameBoard.player_discard.append(player.hand.pop(card_index))
                color = GameBoard.cities[chosen_card].color
                GameBoard.card_colors.remaining[color] += -1
            else:
                parse_action(Pandemic, active_player, input)
        else:
            chosen_card = raw_input("Type the name of the card to discard: ")
            if chosen_card in player.hand:
                card_index = player.hand.index(chosen_card)
                GameBoard.player_discard.append(player.hand.pop(card_index))
                color = GameBoard.cities[chosen_card].color
                GameBoard.card_colors.remaining[color] += -1


#This method does a bunch of different condition checks to ensure the rules are
#followed  It checks cures to see if the players have won, handles medic's free
#distribution of cures to infected cities, checks for eradicated diseases, and
#checks to see if the player it is passed needs to discard a card.  It takes as
#arguments the player list of the player whose turn it is.
def update_game(GameBoard, player):
    GameBoard.check_if_game_over(GameBoard)
    #If the player is a medic...
    if player.role == "Medic":
        #Loop through the list of diseases...
        for color in xrange(len(GameBoard.cures)):
            #If a disease has been cured,
            if GameBoard.cures[color] > GameBoard.terms["uncured"]:
                #store the number of disease cubes of that color which are at
                #the Medic's location.
                cubes = GameBoard.cities[player.location].disease_tokens[color]
                #Clear those cubes off the game board,
                GameBoard.cities[player.location].disease_tokens[color] = 0
                #and put them back into the bin for later use.
                GameBoard.cubes_remaining[color] += -cubes
    #Loop through the blocksRemaining list
    for i in xrange(len(GameBoard.cubes_remaining)):
        #If there are 24 cubes of a color in the list and that disease is cured
        if (GameBoard.cubes_remaining[i] == 24) and GameBoard.cures[i] > 0:
            #That disease is eradicated and cannot spread anymore!
            GameBoard.cures[i] = GameBoard.terms["eradicated"]
    #Check if the player's hand has more than seven cards...
    while len(player.hand) > 7:
        #And discard until it doesn't.
        print "You have too many cards in your hand!"
        discard(player)

def analyze_board(Pandemic, GameBoard, Player, depth, actions_left):
    if depth == 0:
        #Board value starts at 96- the total number of cubes
        board_value = 96
        #Reduce it by 1 for each cube on the board.
        board_value -= 24 - GameBoard.cubes_remaining[GameBoard.terms["blue"]]
        board_value -= 24 - GameBoard.cubes_remaining[GameBoard.terms["yellow"]]
        board_value -= 24 - GameBoard.cubes_remaining[GameBoard.terms["black"]]
        board_value -= 24 - GameBoard.cubes_remaining[GameBoard.terms["red"]]
        #Increase the board value by 10 for each cure.
        if GameBoard.cures[GameBoard.terms["blue"]] > GameBoard.terms["uncured"]:
            boardValue += 10
        if GameBoard.cures[GameBoard.terms["yellow"]] > GameBoard.terms["uncured"]:
            boardValue += 10
        if GameBoard.cures[GameBoard.terms["black"]] > GameBoard.terms["uncured"]:
            boardValue += 10
        if GameBoard.cures[GameBoard.terms["red"]] > GameBoard.terms["uncured"]:
            boardValue += 10
        #Increase the board value by 0.5 per city connection of each research
            #station
        for i in xrange(len(GameBoard.research_stations)):
            a = len(GameBoard.research_stations[i].city_connections)
            distance = 12
            station_name = GameBoard.research_stations[i].name
            station_index = GameBoard.city_index.index(station_name)
            #And by +0.5 more per city between each station and the next-closest
            #research station; the more spread out they are, the better.
            for j in xrange(len(GameBoard.research_stations)):
                if i != j:
                    station_2_name = GameBoard.research_stations[j].name
                    station_2_index = GameBoard.city_index.index(station_2_name)
                    if distance > GameBoard.distance[station_index, station_2_index]:
                        distance = GameBoard.distance[station_index, station_2_index]
            a += distance
            board_value += (int) (0.5 * a)
            
        
        #Determine the number of cards of the same color in each player's hand
        #and give +1 to the board state per player with 3 cards of the same
        #color card in their hand; +5 for 4, and +8 for 5; scientists are the
        #same, except with 1 card less for each value.
        player_list = Pandemic.Players
        for i in xrange(len(player_list)):
            hand = player_list[i].hand
            count = 0
            for j in xrange(len(hand)):
                if j < len(hand):
                    color_1 = GameBoard.cities[hand[j]].color
                    color_2 = GameBoard.cities[hand[j+1]].color
                    if color_1 == color_2:
                        count += 1
            if player_list[i].role == "Scientist":
                if count == 2:
                    board_value += 1
                elif count == 3:
                    board_value += 3
                elif count == 4:
                    board_value += 5
                    #If the player has enough cards for a cure and is in a city
                    #with a research station, they can cure next turn and should
                    #grant a bonus to that board state.
                    location = GameBoard.cities[player_list[i].location]
                    if location in GameBoard.research_stations:
                        board_value += 2
            else:
                if count == 3:
                    board_value += 1
                elif count == 4:
                    board_value += 3
                elif count == 5:
                    board_value += 5
                    location = GameBoard.cities[player_list[i].location]
                    if location in GameBoard.research_stations:
                        board_value += 2

    #Examine the GameBoard and check the hash of all gameboards to see if it's
        #already been seen.  if it has, return that board's value

    #If a win or lose condition, return its value
        
    
    #Generate a list of alternate board states based on each possible action
    #Generate the next_player based on actions_left
        #If next_player isn't the same player, reset actions_left to 1 for the
        #RNG god, or 4 for the next actual player
    #Generate a list of alternate board states for each of the above ones for
    #each card that could be drawn- two, three, or four infect cards, counting
    #order.  This is computationally insane.

    #For each alternate board state, get its value by calling this method on it
    #Combine the values of each board state to get the highest one.
        #If player is human, value(new state) = maximum of the board's values
        #If the player is the RNG, the value of the board is determined by
        #weighted chance
    #Store the gameboard in the hashmap
    #Return value of new state

    #This will generate 10^49 different board states every turn, assuming each
        #turn is as simple as the very first one.  Heuristics are the only
        #way to go, and they're beyond me.

def action_check(player, GameBoard):
    location = GameBoard.cities[player.location]
    hand = player.hand
    #For each player, possible actions include:
    #1: Walk to each neighboring city from the one it is in (avg 4)
    #2: direct flight to each city in the player's hand (avg 4)
    #3: if this city's card is in their hand (1 in 5 chance, on average)
        #3A: Build a research station here
        #3B: charter flight to each other city on the map (47 options)
    #4: if there is a research station here (1 in 24 chance on average)
        #4a: shuttle flight to each other research station (up to 6)
        #4b: if Operations, operations flight to each other city, discarding
            #each card in hand for each (47 other cities, up to 7 cards in hand,
            #so 329)
        #4c: if cards in hand, cure disease
    #5: If Dispatcher, for each Player:
        #5a: walk to each neighboring city from the one its in (avg 4 per player,
            #so avg 12)
        #5B: dispatcher flight to each other player (avg 6)
    #6: if in same place as any other player (1/24 chance)
        #6a: if you have the city card for the city you're in: (1/5 chance)
            #6aa: give card to other player
        #6b: if they have the city card for the city you're in:
            #6ba: take card from other player
        #6c: if you are a researcher
            #6ca: give each card in your hand to other player (up to 7)
        #6d: if they are a researcher
            #6da: take each card in their hand (up to 7)
    #7: Treat disease (up to 4)
    #8: if contingency, draw card from the discard pile (up to 5).
    #In total, this means that the very first player on the very first turn
        #of the game has 839,808 different first turns



def start():
    player_count = True
    while player_count:
        players = int(raw_input("How many players? (2, 3, or 4) "))
        if players > 1 or players < 5:
            player_count = False
        else:
            print "Not valid number of players."
    difficulty_boolean = True
    while difficulty_boolean:
        difficulty = int(raw_input("How many Epidemics? (4, 5, or 6) "))
        if difficulty >3 and difficulty < 7:
            difficulty_boolean = False
        else:
            print "Not valid number of Epidemics."
    Game = Pandemic(players, difficulty)
    Game.draw_board()
    play(Game)

def start(players, difficulty):
    Game = Pandemic(players, difficulty)
    Game.draw_board()
    play(Game)

start(4,6)
