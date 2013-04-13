import numpy as np
import operator
import collections

class GameBoard(object):
    terms = {"uncured": 0, "cured": 1, "eradicated": 2, "blue": 0, "yellow": 1,
             "black": 2, "red": 3}
    roles = ["Contingency", "Dispatcher", "Medic", "Operations",
             "Quarantine", "Researcher", "Scientist"]
    events = {"Epidemic": -1, "Government Grant": 48, "Airlift": 49,
              "Forecast": 50, "One Quiet Night": 51, "Resilient Population": 52}    
    def __init__(self):
        self.reset_game()
        

    def reset_game(self):
        """
        Reset all of the game attributes to their starting values
        """
        self.game_over = False
        self.cities = collections.OrderedDict(
            {"Atlanta": Atlanta("Atlanta"),
             "Washington": Washington("Washington"),
             "San Francisco": SanFrancisco("San Francisco"),
             "Chicago": Chicago("Chicago"),
             "Montreal": Montreal("Montreal"), "New York": NewYork("New York"),
             "London": London("London"), "Madrid": Madrid("Madrid"),
             "Paris": Paris("Paris"), "Essen": Essen("Essen"),
             "Milan": Milan("Milan"),
             "St. Petersburg": StPetersburg( "St. Petersburg"),
             "Los Angeles": LosAngeles("Los Angeles"),
             "Mexico City": MexicoCity("Mexico City"), "Miami": Miami("Miami"),
             "Bogota": Bogota("Bogota"), "Lima": Lima("Lima"),
             "Santiago": Santiago("Santiago"),
             "Buenos Aires": BuenosAires("Buenos Aires"),
             "Sao Paulo": SaoPaulo("Sao Paulo"), "Lagos": Lagos("Lagos"),
             "Kinsasha": Kinsasha("Kinsasha"),
             "Johannesburg": Johannesburg("Johannesburg"),
             "Khartoum": Khartoum("Khartoum"), "Algiers": Algiers("Algiers"),
             "Cairo": Cairo("Cairo"), "Istanbul": Istanbul("Istanbul"),
             "Moscow": Moscow("Moscow"), "Baghdad": Baghdad("Baghdad"),
             "Riyadh": Riyadh("Riyadh"), "Tehran": Tehran("Tehran"),
             "Karachi": Karachi("Karachi"), "Mumbai": Mumbai("Mumbai"),
             "Delhi": Delhi("Delhi"), "Chennai": Chennai("Chennai"),
             "Kolkata": Kolkata("Kolkata"), "Bangkok": Bangkok("Bangkok"),
             "Jakarta": Jakarta("Jakarta"), "Sydney": Sydney("Sydney"),
             "Ho Chi Minh City": HoChiMinhCity("Ho Chi Minh City"),
             "Manila": Manila("Manila"), "Hong Kong": HongKong("Hong Kong"),
             "Taipei": Taipei("Taipei"), "Osaka": Osaka("Osaka"),
             "Tokyo": Tokyo("Tokyo"), "Seoul": Seoul("Seoul"),
             "Shanghai": Shanghai("Shanghai"), "Beijing": Beijing("Beijing")})

        self.player_deck = ["Atlanta", "Washington", "San Francisco",
                            "Chicago", "Montreal", "New York", "London",
                            "Madrid", "Paris", "Essen", "Milan",
                            "St. Petersburg", "Los Angeles", "Mexico City",
                            "Miami", "Bogota", "Lima", "Santiago",
                            "Buenos Aires", "Sao Paulo", "Lagos",
                            "Kinsasha", "Johannesburg", "Khartoum",
                            "Algiers", "Cairo", "Istanbul", "Moscow",
                            "Baghdad", "Riyadh", "Tehran", "Karachi",
                            "Mumbai", "Delhi", "Chennai", "Kolkata",
                            "Bangkok", "Jakarta", "Sydney",
                            "Ho Chi Minh City", "Manila", "Hong Kong",
                            "Taipei", "Osaka", "Tokyo", "Seoul", "Shanghai",
                            "Beijing", "Government Grant", "Airlift",
                            "Forecast", "One Quiet Night",
                            "Resilient Population"]
        self.infect_deck = ["Atlanta", "Washington", "San Francisco",
                            "Chicago", "Montreal", "New York", "London",
                            "Madrid", "Paris", "Essen", "Milan",
                            "St. Petersburg", "Los Angeles", "Mexico City",
                            "Miami", "Bogota", "Lima", "Santiago",
                            "Buenos Aires", "Sao Paulo", "Lagos",
                            "Kinsasha", "Johannesburg", "Khartoum",
                            "Algiers", "Cairo", "Istanbul", "Moscow",
                            "Baghdad", "Riyadh", "Tehran", "Karachi",
                            "Mumbai", "Delhi", "Chennai", "Kolkata",
                            "Bangkok", "Jakarta", "Sydney",
                            "Ho Chi Minh City", "Manila", "Hong Kong",
                            "Taipei", "Osaka", "Tokyo", "Seoul", "Shanghai",
                            "Beijing"]
        self.research_stations = [self.cities["Atlanta"],
                                  -1, -1, -1, -1, -1, -1]
        self.outbreak_marker = 0
        self.infection_rate_marker = 0
        self.one_quiet_night_marker = 0
        self.cubes_remaining = [24, 24, 24, 24]
        self.color_cards_remaining = [12, 12, 12, 12]
        self.epidemic_this_turn = 0
        self.cures = [0,0,0,0]
        self.intensify_list = []
        self.infect_discard = []
        self.player_discard = []
        self.reason_over = ""
        


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
        self.risk_assessment = 0

    #This method just prints the city's information in an easy-to-read fashion.
    def print_city(self):
        self.numbers_to_colors = {0: "Blue", 1: "Yellow", 2: "Black", 3: "Red"}
        print "Name:            ", self.name
        print "Color:           ", self.numbers_to_colors[self.color]
        print "Blue Cubes:      ", self.disease_tokens[0]
        print "Yellow Cubes:    ", self.disease_tokens[1]
        print "Black Cubes:     ", self.disease_tokens[2]
        print "Red Cubes:       ", self.disease_tokens[3]
        print "Risk Assessment: ", self.risk_assessment
        if self.research_station == 1:
            print "Research Station? Built"
        else:
            print "Research Station? Not Built"
        print "Connected Cities:", self.city_connections

    #This method determines the likelihood of an outbreak and risk factor for
    #each individual city.  It is called, updating the city's risk_assessment,
    #every time the city is infected. AI should look at board and determine how
    #many cubes of each color could be placed based on outbreaks and similar
    def assess_risk(self, GameBoard):
        #Reset risk assessment to zero.
        self.risk_assessment = 0
        #Iterate through the colors of its diseases.
        for color in xrange(4):
            #If it has any infection cubes
            if (self.disease_tokens[color] > 0):
                #increment it's risk assessment by one per cube.
                self.risk_assessment += self.disease_tokens[color]
                #If the city has three cubes of one color and could outbreak,
                if self.disease_tokens[color] == 3:
                    #Increment it's risk assessment by one more.
                    self.risk_assessment += 1
                    #Check to see if an outbreak would end the game
                    if GameBoard.cubes_remaining[color] + 1 - len(self.city_connections) < 0:
                        #Panic and freak out.
                        self.risk_assessment += 10
                    #And look through all of its neighbors.
                    for neighbors in self.city_connections.keys():
                        #Grab the neighbor being looked at by the loop
                        self.neighbor = GameBoard.cities[neighbors]
                        #If it's a neighbor and not the city itself...
                        if self.city_connections[neighbors] != 0:
                            #Increment the city's risk assessment by 1 for each
                            #neighbor it has
                            self.risk_assessment += 1
                            #Then look at each neighbor's infection cubes.
                            #If they have 3 cubes of the same color...
                            if (self.neighbor.disease_tokens[color] == 3):
                                #Increment the city's risk by two more.
                                self.risk_assessment += 2
                            #If the neighbor only has two cubes...
                            elif (self.neighbor.disease_tokens[color] == 2):
                                #increment the city's risk by one more
                                self.risk_assessment += 1
        #If the city is in the infect_discard pile
        if GameBoard.infect_discard.count(self.name) == 1:
            #decrease its risk by one, as it can't be drawn again 'til the next
            #epidemic.
            self.risk_assessment += -1
        #If it's in the intensify pile instead...
        elif GameBoard.intensify_list.count(self.name) == 1:
            #boost it even more as it's likely to be drawn soon.
            self.risk_assessment += 2
        #If it's not in either location, it's in the main deck, after all the
        #cards in the Intensify pile.
        else:
            #Halve the intensify pile's size to determine how many turns until
            #the card could be drawn...
            self.reduction = len(GameBoard.intensify_list) / 2
            #and reduce its risk by that amount.
            self.risk_assessment += -self.reduction
        #Can't have negative risk, that could be screwy.
        if self.risk_assessment < 0:
            self.risk_assessment = 0
                
    #The active player builds a research station in this city.
    #Self is the city, player is the player building the research
    #station, discard_index is the index of the card being discarded in
    #the player's hand, GameBoard is GameBoard, and *args is the city
    #which needs to have its research station removed to make room for
    #the new one.
    def research(self, player, discard_index, GameBoard, *args):
        #Check that there isn't ALREADY a research station at this location...
        if (self.research == 1):
            return
        #if there are any additional arguments given...
        elif (len(args) > 0):
            #take the first one and delete the research station located in
            #that city.
            args[0].research = 0
            #And remove the above city from the list of research stations
            index = research_stations.index(args[0])
            GameBoard.research_stations[index] = -1
        #If no argument for research station removal is provided and there
        #are six research stations already built...
        elif (len(args) != 1 and research_stations.count(-1) == 0):
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
        color = player.hand[discard_index].color
        GameBoard.card_colors_remaining[color] += -1
        #Discard the card
        player_discard_pile.append(player.hand.pop(discard_index))


    #The active player treats one color in this city.  Self is self, player
    #is the player treating the disease, GameBoard is Game Board, and color
    #is the color of the disease being treated.
    def treat(self, player, GameBoard, color):
        #If there are no disease cubes of the chosen color, waste the action
        if self.disease_tokens[color] < 1:
            return
        #If the disease is already cured, or the player is a medic
        elif GameBoard.cures[color] > GameBoard.terms["uncured"]:
            #Grab the number of cubes of the chosen color off the city
            cubes = self.disease_tokens[color]
            #Return them to the cubes_remaining pool
            GameBoard.cubes_remaining[color] += cubes
            #and wipe them off the city
            self.disease_tokens[color] = 0
            player.actions += -1
            self.assess_risk(GameBoard)
        #If the player is a medic...
        elif  player.role == "Medic":
            #Grab the number of cubes of the chosen color off the city
            cubes = self.disease_tokens[color]
            #Return them to the cubes_remaining pool
            GameBoard.cubes_remaining[color] += cubes
            #and wipe them off the city
            self.disease_tokens[color] = 0
            player.actions += -1
            self.assess_risk(GameBoard)
        #If the player is not a medic and the disease isn't cured
        else:
            #remove one cube and place it back in the cubes_remaining pool
            self.disease_tokens[color] += -1
            GameBoard.cubes_remaining[color] += 1
            player.actions += -1
            self.assess_risk(GameBoard)

            
    #The game itself infects the city.  *args are, optionally, the color
    #of the disease being added.
    def infect(self, GameBoard, Players, *args):
        #Grab the color to add, if there are any args.
        if (len(args)>0):
            color = args[0]
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
        print "Outbreak at", self.name
        for city_name, distance in self.city_connections.iteritems():
            if distance == 1:
                city = GameBoard.cities[city_name]
                city.infect(GameBoard, Players, self.color)



class Atlanta(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Washington": 0,
                                 "Atlanta": 1,
                                 "Montreal": 1,
                                 "New York": 1}
class SanFrancisco(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"San Francisco": 0,
                                 "Tokyo": 1,
                                 "Manila": 1,
                                 "Los Angeles": 1,
                                 "Chicago": 1}
class Chicago(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Chicago": 0,
                                 "San Francisco": 1,
                                 "Mexico City": 1,
                                 "Atlanta": 1,
                                 "Los Angeles": 1,
                                 "Montreal": 1}
class Montreal(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Montreal": 0,
                                 "Chicago": 1,
                                 "Washington": 1,
                                 "New York": 1}
class NewYork(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"New York": 0,
                                 "Montreal": 1,
                                 "Washington": 1,
                                 "London": 1,
                                 "Madrid": 1}
class London(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"London": 0,
                                 "New York": 1,
                                 "Madrid": 1,
                                 "Paris": 1,
                                 "Essen": 1}
class Madrid(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Madrid": 0,
                                 "New York": 1,
                                 "London": 1,
                                 "Sao Paulo": 1,
                                 "Algiers": 1,
                                 "Paris": 1}
class Paris(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Essen": 0,
                                 "London": 1,
                                 "Paris": 1,
                                 "Milan": 1,
                                 "St. Petersburg": 1}
class Milan(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["blue"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"St. Petersburg": 0,
                                 "Essen": 1,
                                 "Istanbul": 1,
                                 "Moscow": 1}

class LosAngeles(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Los Angeles": 0,
                                 "San Francisco": 1,
                                 "Mexico City": 1,
                                 "Chicago": 1,
                                 "Sydney": 1}

class MexicoCity(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Mexico City": 0,
                                 "Los Angeles": 1,
                                 "Chicago": 1,
                                 "Miami": 1,
                                 "Lima": 1,
                                 "Bogota": 1}
class Miami(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Miami": 0,
                                 "Mexico City": 1,
                                 "Bogota": 1,
                                 "Atlanta": 1,
                                 "Washington": 1}
class Bogota(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Bogota": 0,
                                 "Mexico City": 1,
                                 "Lima": 1,
                                 "Buenos Aires": 1,
                                 "Sao Paulo": 1,
                                 "Miami": 1}
class Lima(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Lima": 0,
                                 "Mexico City": 1,
                                 "Bogota": 1,
                                 "Santiago": 1}
class Santiago(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Santiago": 0,
                                 "Lima": 1}
class BuenosAires(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Buenos Aires": 0,
                                 "Bogota": 1,
                                 "Sao Paulo": 1}
class SaoPaulo(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Sao Paulo": 0,
                                 "Bogota": 1,
                                 "Buenos Aires": 1,
                                 "Madrid": 1,
                                 "Lagos": 1}
class Lagos(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Lagos": 0,
                                 "Sao Paulo": 1,
                                 "Kinsasha": 1,
                                 "Khartoum": 1}

class Kinsasha(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Johannesburg": 0,
                                 "Khartoum": 1,
                                 "Kinsasha": 1}
class Khartoum(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["yellow"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Istanbul": 0,
                                 "Milan": 1,
                                 "Algiers": 1,
                                 "Cairo": 1,
                                 "Baghdad": 1,
                                 "Moscow": 1,
                                 "St. Petersburg": 1}

class Moscow(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Moscow": 0,
                                 "St. Petersburg": 1,
                                 "Istanbul": 1,
                                 "Tehran": 1}

class Baghdad(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["black"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Kolkata": 0,
                                 "Delhi": 1,
                                 "Chennai": 1,
                                 "Bangkok": 1,
                                 "Hong Kong": 1}
class Bangkok(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Bangkok": 0,
                                 "Kolkata": 1,
                                 "Chennai": 1,
                                 "Jakarta": 1,
                                 "Ho Chi Minh City": 1,
                                 "Hong Kong": 1}
class Jakarta(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Jakarta": 0,
                                 "Chennai": 1,
                                 "Sydney": 1,
                                 "Kolkata": 1,
                                 "Ho Chi Minh City": 1,
                                 "Hong Kong": 1}
class Sydney(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Sydney": 0,
                                 "Jakarta": 1,
                                 "Manila": 1,
                                 "Los Angeles": 1}

class HoChiMinhCity(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Ho Chi Minh City": 0,
                                 "Bangkok": 1,
                                 "Jakarta": 1,
                                 "Manila": 1,
                                 "Hong Kong": 1}
class Manila(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Manila": 0,
                                 "Ho Chi Minh City": 1,
                                 "Sydney": 1,
                                 "San Francisco": 1,
                                 "Taipei": 1,
                                 "Hong Kong": 1}
class HongKong(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Hong Kong": 0,
                                 "Ho Chi Minh City": 1,
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Taipei": 0,
                                 "Hong Kong": 1,
                                 "Osaka": 1,
                                 "Manila": 1,
                                 "Shanghai": 1}
class Osaka(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Osaka": 0,
                                 "Tokyo": 1,
                                 "Taipei": 1}
class Tokyo(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Tokyo": 0,
                                 "Seoul": 1,
                                 "Osaka": 1,
                                 "San Francisco": 1,
                                 "Shanghai": 1}
class Seoul(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
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
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Shanghai": 0,
                                 "Beijing": 1,
                                 "Seoul": 1,
                                 "Tokyo": 1,
                                 "Taipei": 1,
                                 "Hong Kong": 1}
class Beijing(City):
    def __init__(self, name):
        self.name = name
        self.color = GameBoard.terms["red"]
        self.disease_tokens = [0,0,0,0]
        self.risk_assessment = 0
        self.research_station = 0
        self.city_connections = {"Beijing": 0,
                                 "Seoul": 1,
                                 "Shanghai": 1}

class Player(object):
    def __init__(self, role):
        self.location = "Atlanta"
        self.role = role
        self.actions = 4
        self.stored_card = 0
        self.hand = []

#This method creates a 2d array of distances.  It is detailed below the method.
def create_distances(cities):
    distance = np.zeros(shape = (len(cities),len(cities)))
    previous = np.zeros(shape = (len(cities),len(cities)))
    for home in xrange(len(cities)):
        for destination in xrange(len(cities)):
            if home == destination:
                distance[home,destination] = 0
                previous[home,destination] = destination
            elif destination in home.city_connections:
                distance[home,destination] = 1
                previous[home,destination] = home
            else:
                distance[home, destination] = 48
                previous[home, destination] = -1
    for intermediary in xrange(len(cities)):
        for home in xrange(len(cities)):
            for destination in xrange(len(cities)):
                d1 = distance[home, intermediary]
                d2 = distance[intermediary, destination]
                d3 = distance[home, destination]
                if d1 + d2 < d3:
                    d3 = d1 + d2
                    distance[home, destination] = d3
                    previous[home, destination] = intermediary
    return [distance, previous]

def get_path(home, destination):
    if home == destination or destination in home.city_connections:
        return destination
    else:
        get_path(home, previousStep[home, destination])

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
    def __init__(self, player_count, difficulty):
        self.create_game(player_count, difficulty)
    def create_game(self, player_count, difficulty):
        self.GameBoard = GameBoard()
        self.GameBoard.player_deck = shuffle(self.GameBoard.player_deck)
        self.GameBoard.infect_deck = shuffle(self.GameBoard.infect_deck)
        self.GameBoard.roles = shuffle(self.GameBoard.roles)
        self.p1 = Player(self.GameBoard.roles.pop())
        self.p1.hand.append(self.GameBoard.player_deck.pop())
        self.p1.hand.append(self.GameBoard.player_deck.pop())
        self.p2 = Player(self.GameBoard.roles.pop())
        self.p2.hand.append(self.GameBoard.player_deck.pop())
        self.p2.hand.append(self.GameBoard.player_deck.pop())
        self.Players = [self.p1, self.p2]
        if player_count == 2:
            self.p1.hand.append(self.GameBoard.player_deck.pop())
            self.p1.hand.append(self.GameBoard.player_deck.pop())
            self.p2.hand.append(self.GameBoard.player_deck.pop())
            self.p2.hand.append(self.GameBoard.player_deck.pop())
        elif player_count == 3:
            self.p1.hand.append(self.GameBoard.player_deck.pop())
            self.p2.hand.append(self.GameBoard.player_deck.pop())
            self.p3 = Player(self.GameBoard.roles.pop())
            self.p3.hand.append(self.GameBoard.player_deck.pop())
            self.p3.hand.append(self.GameBoard.player_deck.pop())
            self.p3.hand.append(self.GameBoard.player_deck.pop())
            self.Players.append(self.p3)
        elif player_count == 4:
            self.p3 = Player(self.GameBoard.roles.pop())
            self.p3.hand.append(self.GameBoard.player_deck.pop())
            self.p3.hand.append(self.GameBoard.player_deck.pop())
            self.Players.append(self.p3)
            self.p4 = Player(self.GameBoard.roles.pop())
            self.p4.hand.append(self.GameBoard.player_deck.pop())
            self.p4.hand.append(self.GameBoard.player_deck.pop())
            self.Players.append(self.p4)

        #Generate the game's player deck: split it into as many smaller piles
        #as there are Epidemic cards (the Difficulty), add one Epidemic to each,
        #shuffle them, and then stack them together to create the player deck.
        self.cut1 = []
        self.cut2 = []
        self.cut3 = []
        self.cut4 = []
        if (difficulty == 4):
            for i in xrange(11):
                self.cut1.append(self.GameBoard.player_deck.pop(0))
                self.cut2.append(self.GameBoard.player_deck.pop(0))
                self.cut3.append(self.GameBoard.player_deck.pop(0))
                self.cut4.append(self.GameBoard.player_deck.pop(0))
            if player_count != 3:
                self.cut1.append(self.GameBoard.player_deck.pop(0))
            self.cut1.append(self.GameBoard.events["Epidemic"])
            self.cut2.append(self.GameBoard.events["Epidemic"])
            self.cut3.append(self.GameBoard.events["Epidemic"])
            self.cut4.append(self.GameBoard.events["Epidemic"])
            self.GameBoard.player_deck = shuffle(self.cut1)
            self.GameBoard.player_deck.append(shuffle(self.cut2))
            self.GameBoard.player_deck.append(shuffle(self.cut3))
            self.GameBoard.player_deck.append(shuffle(self.cut4))
        elif (difficulty == 5):
            self.cut5 = []
            for i in xrange(8):
                self.cut1.append(self.GameBoard.player_deck.pop(0))
                self.cut2.append(self.GameBoard.player_deck.pop(0))
                self.cut3.append(self.GameBoard.player_deck.pop(0))
                self.cut4.append(self.GameBoard.player_deck.pop(0))
                self.cut5.append(self.GameBoard.player_deck.pop(0))
            self.cut1.append(self.GameBoard.player_deck.pop(0))
            self.cut2.append(self.GameBoard.player_deck.pop(0))
            self.cut3.append(self.GameBoard.player_deck.pop(0))
            self.cut4.append(self.GameBoard.player_deck.pop(0))
            if player_count == 3:
                self.cut5.append(self.GameBoard.player_deck.pop(0))
            self.cut1.append(self.GameBoard.events["Epidemic"])
            self.cut2.append(self.GameBoard.events["Epidemic"])
            self.cut3.append(self.GameBoard.events["Epidemic"])
            self.cut4.append(self.GameBoard.events["Epidemic"])
            self.cut5.append(self.GameBoard.events["Epidemic"])
            self.GameBoard.player_deck = shuffle(self.cut1)
            self.GameBoard.player_deck.append(shuffle(self.cut2))
            self.GameBoard.player_deck.append(shuffle(self.cut3))
            self.GameBoard.player_deck.append(shuffle(self.cut4))
            self.GameBoard.player_deck.append(shuffle(self.cut5))
        elif (difficulty == 6):
            self.cut5 = []
            self.cut6 = []
            for i in xrange(7):
                self.cut1.append(self.GameBoard.player_deck.pop(0))
                self.cut2.append(self.GameBoard.player_deck.pop(0))
                self.cut3.append(self.GameBoard.player_deck.pop(0))
                self.cut4.append(self.GameBoard.player_deck.pop(0))
                self.cut5.append(self.GameBoard.player_deck.pop(0))
                self.cut6.append(self.GameBoard.player_deck.pop(0))
            self.cut1.append(self.GameBoard.player_deck.pop(0))
            self.cut2.append(self.GameBoard.player_deck.pop(0))
            if player_count == 3:
                self.cut3.append(self.GameBoard.player_deck.pop(0))
            self.cut1.append(self.GameBoard.events["Epidemic"])
            self.cut2.append(self.GameBoard.events["Epidemic"])
            self.cut3.append(self.GameBoard.events["Epidemic"])
            self.cut4.append(self.GameBoard.events["Epidemic"])
            self.cut5.append(self.GameBoard.events["Epidemic"])
            self.cut6.append(self.GameBoard.events["Epidemic"])
            self.GameBoard.player_deck = shuffle(self.cut1)
            self.GameBoard.player_deck.append(shuffle(self.cut2))
            self.GameBoard.player_deck.append(shuffle(self.cut3))
            self.GameBoard.player_deck.append(shuffle(self.cut4))
            self.GameBoard.player_deck.append(shuffle(self.cut5))
            self.GameBoard.player_deck.append(shuffle(self.cut6))

            
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
            elif i > 2 and i < 6:
                self.city.infect(self.GameBoard, self.Players)
                self.city.infect(self.GameBoard, self.Players)
            else:
                self.city.infect(self.GameBoard, self.Players)
           



#This method is called at the end of every turn: it takes the infection rate
#as an argument, draws 2, 3, or 4 cards from the Infect Deck, and infects
#them, potentially causing Outbreaks.
def infection_stage(GameBoard, Players):
    #Clear the outbreak list before infecting, just in case.
    GameBoard.outbreak_list = []
    #Draw a card from the Infect Deck
    index = GameBoard.infect_deck.pop(0)
    #Infect the card's city and update gameBoard
    GameBoard.cities[index].infect(GameBoard, Players)
    #Discard the drawn card to the Infect Discard Pile
    GameBoard.infect_discard.append(index)
    #Clear the outbreak list again, because we aren't done yet.
    GameBoard.outbreak_list = []
    #Rinse and repeat at least once.
    index = GameBoard.infect_deck.pop(0)
    GameBoard.cities[index].infect(GameBoard, Players)
    GameBoard.infect_discard.append(index)
    GameBoard.outbreak_list = []
    #If the infection rate is 2 or more, infect one more city
    if GameBoard.infection_rate > 2:
        index = GameBoard.infect_deck.pop(0)
        GameBoard.cities[index].infect(GameBoard, Players)
        GameBoard.infect_discard.append(index)
        GameBoard.outbreak_list = []
    #If the Infection Rate is 6 or more, infect a fourth city.
    if GameBoard.infection_rate > 5:
        index = GameBoard.infect_deck.pop(0)
        GameBoard.cities[index].infect(GameBoard, Players)
        GameBoard.infect_discard.append(index)
        GameBoard.outbreak_list = []





#This method is called when an Epidemic card is drawn by a player.  It takes no
#   arguments (from anyone), and does what it wants.  More accurately, this
#   method increments the Infection Rate marker by one, draws an Infect card
#   from the bottom of the Infect Deck, infects that city three times, and then
#   takes all the cards out of the Infection Discard pile, shuffles them, and
#   puts them back ontop of the Infect Deck so they can be drawn again and
#   really kick the player's teeth in.  This modifies the following Global
#   Variables: gameBoard, infectionRateMarker, InfectDeck, InfectDiscard,
#   Intensify, and EpidemicThisTurn.
def epidemic(GameBoard, Players):
    #Note that an epidemic happened this turn
    GameBoard.epidemic_this_turn = 1
    #Increment the Infection Rate Marker.  Everything just got tougher!
    GameBoard.infection_rate_marker += 1
    #Draw the bottom card from the Infect Deck.
    epidemic_city = GameBoard.infect_deck.pop()
    #And infect it three times, updating the game board each time.
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    GameBoard.cities[epidemic_city].infect(GameBoard, Players)
    #Then discard the card to the Infect Discard Pile
    GameBoard.infect_discard.append(epidemic_city)
    #Clear the Intensify list: while not technically part of the game rules,
    #tracking which cards went back onto the Infect Deck is an essential part
    #of winning the game.  Obviously, no peeking.
    GameBoard.intensify = []
    #Then, loop through the entire Infect Discard Pile
    while (len(GameBoard.infect_discard)>0):
        #grab one card from it at random
        card = GameBoard.infect_discard.pop(
            np.random.random_integers(0,len(infectDiscard)-1))
        #Add the card to the Intensify list so the AI will know it's coming up
        #very soon
        GameBoard.intensify.append(card)
        #and place the card ontop of the Infect Deck
        GameBoard.infect_deck.insert(0,card)
    #Shuffle the Intensify list so the order the cards were placed on the
    #Infect Deck is obscured.
    GameBoard.intensify = shuffle(GameBoard.intensify)
    #And finally, if One Quiet Night hasn't been played...
    if GameBoard.one_quiet_night_marker == 0:
        #Infect.
        infecton_stage(GameBoard, Players)




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
            destination = GameBoard.cities[destination_name]
            move_action(player, get_path(origin, destination))
    if len(args) == 1:
        #The first optional argument will always be the number of actions the
        #player wishes to spend on movement.
        steps = args[0]
        #for each action...
        for i in xrange(steps):
            #check to see if the player has enough remaining actions...
            if player.actions > 0:
                #and then move them using the info from get_path.
                origin = GameBoard.cities[player.location]
                destination = GameBoard.cities[destination_name]
                move_action(player, get_path(origin, destination))
    #If there's more than one argument provided (with no error proofing, of
    #course!), then we assume it's a Dispatcher using his actions to move
    #another player!
    else:
        #Grab the number of actions the Dispatcher wants to spend...
        steps = args[0]
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
                move_action(player, get_path(origin, destination), dispatcher)


#This method is what actually handles the walking part of movement.  It takes
#arguments of the player being moved, the player's destination, and, optionally,
#the dispatcher who will be paying for the movement with his Actions.  This
#method modifies no global variables- hooray!  However, it does modify up to
#two Player Lists.
def move_action(GameBoard, player, destination_name, *args):
    #If there's no dispatcher paying for the movement...
    if len(args) == 0:
        #check (again) to see the player has the actions for this movement
        if player.actions > 0:
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
        if dispatcher.actions > 0:
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
                player.action += - 1
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
                player.action += - 1


#This method allows players to discard a city's card while in that city to fly
#to any other city on the game board.  It takes as arguments the player, the
#destination city's index, and, optionally, the dispatcher who will be paying
#for the movement.
def charter_flight(GameBoard, player, destinationIndex, *args):
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
                color = GameBoard.cities[player.hand[discardIndex]].color
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




#This method allows a player to spend one action to give another player the
#city card of the city they are BOTH in, unless the giver is a Researcher; then
#she can give any city card she damn well pleases to.  It takes, as arguments,
#the player list of the giving player, the player list of the receiving player,
#and the index number of the card being given in the giver's hand.
def give_knowledge(GameBoard, giver, receiver, card_index):
    #If the giver and receiver are in the same city, the giver is a Researcher,
    #and the giver has at least one action left this turn...
    if (giver.location == receiver.location):
        if giver.role == "Researcher" and giver.actions > 0:
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver.hand.append(giver.hand.pop(card_index))
            #Consume one of the giver's actions
            giver.actions += -1
            #And make sure the receiver has seven or fewer cards in his hand.
            hand_limit(receiver)
    #If the giver and receiver are in the same location and the giver can act,
    elif giver.location == receiver.location and giver.actions > 0:
        #and if the giver's location and the card are the same city...
        if giver.hand[card_index] == giver.location:
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver.hand.append(giver.hand.pop(card_index))
            #consume one action from the giver
            giver.actions = giver.actions - 1
            #and make sure the receiver has seven or fewer cards in his hand.
            hand_limit(receiver)


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
            #and make sure he's got seven or fewer cards in his hand
            hand_limit(receiver)
    #If the giver and receiver are in the same city, and the receiver can act
    elif giver.location == receiver.location and receiver.actions > 0:
        #...and if the card being given matches their location
        if giver.hand[card_index] == giver.location:
            #Do the same as above.
            receiver.hand.append(giver.hand.pop(card_index))
            receiver.actions = receiver.actions - 1
            hand_limit(receiver)


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
                index = player_discard.index(event_card)
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
        if player.stored == GameBoard.events["Resilient Population"]:
            player.stored = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index(GameBoard.events["Resilient Population"])
        GameBoard.player_discard.append(player.hand.pop(cardIndex))
        


#This method allows players to use the Airlift card to instantly fly any player
#to any city of their choosing!  It takes as arguments the player list of the
#player with the card, the player list of the player doing the flying, and the
#city index of the destination city.
def airlift(GameBoard, player, target, destination_name):
    #Set the target player's location to the destination.
    target.location = destination_name
    #If the player with the card is a contingency planner who stored the card
    if player.role == "Contingency":
        if player.stored == GameBoard.events["Airlift"]:
            #Poof it into the e-ther.
            player.stored = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index(GameBoard.events["Airlift"])
        GameBoard.player_discard.append(player.hand.pop(cardIndex))


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
    elif (len(args) != 1 and research_stations.count(-1) == 0):
        return
    
    #Build the research station at the destination.
    index = GameBoard.research_stations.index(-1)
    GameBoard.research_stations[index] = city_name
    GameBoard.cities[city_name].research = 1
    
    #Discard the card
    GameBoard.player_discard.append(player.hand.pop(discard_index))
    #If the player's a Contingency planner playing the card from storage
    if player.role == "Contingency":
        if player.stored == GameBoard.events["Government Grant"]:
            #VANISH it.
            player.stored = 0
    #otherwise...
    else:
        #place the card in the player discard pile
        card_index = player.hand.index(GameBoard.events["Government Grant"])
        GameBoard.player_discard.append(player.hand.pop(cardIndex))


#This method allows players to skip the Infect stage on one turn.  It can be
#used to prevent an Epidemic from Infecting, but not from Intensifying.  It
#takes as arguments the player list of the player with the card and the game
#board.
def one_quiet_night(GameBoard, player):
    #Set the OneQuietNightMarker to 1, skipping the Infect stage.
    GameBoard.one_quiet_night_marker = 1
    #COntingency Planner card removal
    if player.role == "Contingency":
        if player.stored == GameBoard.events["One Quiet Night"]:
            player.stored = 0
    else:
        #place the card in the player discard pile
        card_index = player.hand.index(GameBoard.events["One Quiet Night"])
        GameBoard.player_discard.append(player.hand.pop(cardIndex))


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
        if player.stored == GameBoard.events["Forecast"]:
            player.stored = 0
    else:
        #place the card in the player discard pile
        card_index = player.hand.index(GameBoard.events["Forecast"])
        GameBoard.player_discard.append(player.hand.pop(cardIndex))


#This method forces a player to discard one card from their hand.  It takes as
#arguments the player list of the unfortunate soul who has to discard a card.
#It modifies the global variable playerDiscard.
def discard(GameBoard, player):
    #The AI has to choose which card to discard and I have no idea how to code
    #that yet.  Event cards should be used instead of discarded, too...
    #For now, randomness.
    chosenCard = np.random.random_int(0, len(player.hand)-1)
    #Place the discarded card in the player discard pile.  Hey, this one works!
    GameBoard.player_discard.append(player.hand.pop(chosenCard))


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
        discard(player)

    

Game = Pandemic(3, 4)
index = 0
for city_tuple in Game.GameBoard.cities.iteritems():
    city = Game.GameBoard.cities[city_tuple[0]]
    city.print_city()
    print
        
