import numpy as np
import operator
#Notes: this project will require a neural network- or carefully programmed
#weights- for each Role's AI to learn and adapt.  I'm not sure where to start
#with that...  players will need to be aware of the number of cards of each
#color remaining in the deck, in all players' hands, and in the discard pile,
#and be aware of when they've hit their limit.



#7 role cards, 48 city cards, 6 epidemics, 5 events, 48 infection cards, 24x4
#disease cubes, 48 nodes

#Death to magic numbers!  This is also the standardized index that every list
#uses to store the colors, so list[RED] will take you to Red.
BLUE = 1
YELLOW = 2
BLACK = 3
RED = 4

#No magic numbers here!
UNCURED = 0
CURED = 1
ERADICATED = 2

#Role Cards!
CONTINGENCY = 0 #Finished
DISPATCHER = 1 #finished
MEDIC = 2 #finished
OPERATIONS = 3 #finished
QUARANTINE = 4 #finished
RESEARCHER = 5 #finished
SCIENTIST = 6 #finished

#Player terms- eliminating Magic Numbers one variable at a time!
ROLE = 0
LOCATION = 1
STORED = 2
ACTIONS = 3
HAND = 4   #This marks the index location of the list of cards in a player's
#hand.

#City Cards and index info
EPIDEMIC = -1 #Finished
ATLANTA = 0
WASHINGTON = 1
SANFRANCISCO = 2
CHICAGO = 3
MONTREAL = 4
NEWYORK = 5
LONDON = 6
MADRID = 7
PARIS = 8
ESSEN = 9
MILAN = 10
STPETERSBURG = 11
LOSANGELES = 12
MEXICOCITY = 13
MIAMI = 14
BOGOTA = 15
LIMA = 16
SANTIAGO = 17
BUENOSAIRES = 18
SAOPAULO = 19
LAGOS = 20
KINSASHA = 21
JOHANNESBURG = 22
KHARTOUM = 23
ALGIERS = 24
CAIRO = 25
ISTANBUL = 26
MOSCOW = 27
BAGHDAD = 28
RIYADH = 29
TEHRAN = 30
KARACHI = 31
MUMBAI = 32
DELHI = 33
CHENNAI = 34
KOLKATA = 35
BANGKOK = 36
JAKARTA = 37
SYDNEY = 38
HOCHIMINHCITY = 39
MANILA = 40
HONGKONG = 41
TAIPEI = 42
OSAKA = 43
TOKYO = 44
SEOUL = 45
SHANGHAI = 46
BEIJING = 47
GOVGRANT = 48 #finished
AIRLIFT = 49 #finished
FORECAST = 50 #finished
ONEQUIETNIGHT = 51 #Finished
RESILIENTPOP = 52 #finished

#City terms:
COLOR = 0
BLOCKS = 2
RESEARCH = 5
NEIGHBORS = 6 #Marks the index location of the list of neighboring cities.
CITYINDEX = 0
NEXTSTEP = 1
STEPS = 2
NEIGHBORING = 1

#City name =    [Color, Disease tokens (Blue, Yellow, Black, Red),
#                   Research Station,
#                   Connected Cities by index and steps)
Atlanta =       [BLUE,   0,0,0,0, 1,
                 [[ATLANTA, ATLANTA, 0],
                  [CHICAGO, CHICAGO, 1],
                  [WASHINGTON, WASHINGTON, 1],
                  [MIAMI, MIAMI, 1]]]
Washington =    [BLUE,   0,0,0,0, 0,
                 [[WASHINGTON, WASHINGTON, 0],
                  [ATLANTA, ATLANTA, 1],
                  [MONTREAL, MONTREAL, 1],
                  [NEWYORK, NEWYORK, 1]]]
SanFransisco =  [BLUE,   0,0,0,0, 0,
                 [[SANFRANCISCO, SANFRANCISCO, 0],
                  [TOKYO, TOKYO, 1],
                  [MANILA, MANILA, 1],
                  [LOSANGELES, LOSANGELES, 1],
                  [CHICAGO, CHICAGO, 1]]]
Chicago =       [BLUE,   0,0,0,0, 0,
                 [[CHICAGO, CHICAGO, 0],
                  [SANFRANCISCO, SANFRANCISCO, 1],
                  [LOSANGELES, LOSANGELES, 1],
                  [MEXICOCITY, MEXICOCITY, 1],
                  [ATLANTA, ATLANTA, 1],
                  [MONTREAL, MONTREAL, 1]]]
Montreal =      [BLUE,   0,0,0,0, 0,
                 [[MONTREAL, MONTREAL, 0],
                  [CHICAGO, CHICAGO, 1],
                  [WASHINGTON, WASHINGTON, 1],
                  [NEWYORK, NEWYORK, 1]]]
NewYork =       [BLUE,   0,0,0,0, 0,
                 [[NEWYORK, NEWYORK, 0],
                  [MONTREAL, MONTREAL, 1],
                  [WASHINGTON, WASHINGTON, 1],
                  [LONDON, LONDON, 1],
                  [MADRID, MADRID, 1]]]
London =        [BLUE,   0,0,0,0, 0,
                 [[LONDON, LONDON, 0],
                  [NEWYORK, NEWYORK, 1],
                  [MADRID, MADRID, 1],
                  [PARIS, PARIS, 1],
                  [ESSEN, ESSEN, 1]]]
Madrid =        [BLUE,   0,0,0,0, 0,
                 [[MADRID, MADRID, 0],
                  [NEWYORK, NEWYORK, 1],
                  [LONDON, LONDON, 1],
                  [SAOPAULO, SAOPAULO, 1],
                  [ALGIERS, ALGIERS, 1],
                  [PARIS, PARIS, 1]]]
Paris =         [BLUE,   0,0,0,0, 0,
                 [[PARIS, PARIS, 0],
                  [MADRID, MADRID, 1],
                  [LONDON, LONDON, 1],
                  [ESSEN, ESSEN, 1],
                  [MILAN, MILAN, 1],
                  [ALGIERS, ALGIERS, 1]]]
Essen =         [BLUE,   0,0,0,0, 0,
                 [[ESSEN, ESSEN, 0],
                  [LONDON, LONDON, 1],
                  [PARIS, PARIS, 1],
                  [MILAN, MILAN, 1],
                  [STPETERSBURG, STPETERSBURG, 1]]]
Milan =         [BLUE,   0,0,0,0, 0,
                 [[MILAN, MILAN, 0],
                  [ESSEN, ESSEN, 1],
                  [PARIS, PARIS, 1],
                  [ISTANBUL, ISTANBUL, 1]]]
StPetersburg =  [BLUE,   0,0,0,0, 0,
                 [[STPETERSBURG, STPETERSBURG, 0],
                  [ESSEN, ESSEN, 1],
                  [ISTANBUL, ISTANBUL, 1],
                  [MOSCOW, MOSCOW, 1]]]
LosAngeles =    [YELLOW, 0,0,0,0, 0,
                 [[LOSANGELES, LOSANGELES, 0],
                  [SANFRANCISCO, SANFRANCISCO, 1],
                  [CHICAGO, CHICAGO, 1],
                  [MEXICOCITY, MEXICOCITY, 1],
                  [SYDNEY, SYDNEY, 1]]]
MexicoCity =    [YELLOW, 0,0,0,0, 0,
                 [[MEXICOCITY, MEXICOCITY, 0],
                  [LOSANGELES, LOSANGELES, 1],
                  [CHICAGO, CHICAGO, 1],
                  [MIAMI, MIAMI, 1],
                  [LIMA, LIMA, 1],
                  [BOGOTA, BOGOTA, 1]]]
Miami =         [YELLOW, 0,0,0,0, 0,
                 [[MIAMI, MIAMI, 0],
                  [MEXICOCITY, MEXICOCITY, 1],
                  [BOGOTA, BOGOTA, 1],
                  [ATLANTA, ATLANTA, 1],
                  [WASHINGTON, WASHINGTON, 1]]]
Bogota =        [YELLOW, 0,0,0,0, 0,
                 [[BOGOTA, BOGOTA, 0],
                  [MEXICOCITY, MEXICOCITY, 1],
                  [LIMA, LIMA, 1],
                  [BUENOSAIRES, BUENOSAIRES, 1],
                  [SAOPAULO, SAOPAULO, 1],
                  [MIAMI, MIAMI, 1]]]
Lima =          [YELLOW, 0,0,0,0, 0,
                 [[LIMA, LIMA, 0],
                  [MEXICOCITY, MEXICOCITY, 1],
                  [BOGOTA, BOGOTA, 1],
                  [SANTIAGO, SANTIAGO, 1]]]
Santiago =      [YELLOW, 0,0,0,0, 0,
                 [[SANTIAGO, SANTIAGO, 0],
                  [LIMA, LIMA, 1]]]
BuenosAires =   [YELLOW, 0,0,0,0, 0,
                 [[BUENOSAIRES, BUENOSAIRES, 0],
                  [BOGOTA, BOGOTA, 1],
                  [SAOPAULO, SAOPAULO, 1]]]
SaoPaulo =      [YELLOW, 0,0,0,0, 0,
                 [[SAOPAULO, SAOPAULO, 0],
                  [BOGOTA, BOGOTA, 1],
                  [BUENOSAIRES, BUENOSAIRES, 1],
                  [MADRID, MADRID, 1],
                  [LAGOS, LAGOS, 1]]]
Lagos =         [YELLOW, 0,0,0,0, 0,
                 [[LAGOS, LAGOS, 0],
                  [SAOPAULO, SAOPAULO, 1],
                  [KINSASHA, KINSASHA, 1],
                  [KHARTOUM, KHARTOUM, 1]]]
Kinsasha =      [YELLOW, 0,0,0,0, 0,
                 [[KINSASHA, KINSASHA, 0],
                  [LAGOS, LAGOS, 1],
                  [KHARTOUM, KHARTOUM, 1],
                  [JOHANNESBURG, JOHANNESBURG, 1]]]
Johannesburg =  [YELLOW, 0,0,0,0, 0,
                 [[JOHANNESBURG, JOHANNESBURG, 0],
                  [KHARTOUM, KHARTOUM, 1],
                  [KINSASHA, KINSASHA, 1]]]
Khartoum =      [YELLOW, 0,0,0,0, 0,
                 [[KHARTOUM, KHARTOUM, 0],
                  [LAGOS, LAGOS, 1],
                  [KINSASHA, KINSASHA, 1],
                  [JOHANNESBURG, JOHANNESBURG, 1],
                  [CAIRO, CAIRO, 1]]]
Algiers =       [BLACK,  0,0,0,0, 0,
                 [[ALGIERS, ALGIERS, 0],
                  [MADRID, MADRID, 1],
                  [PARIS, PARIS, 1],
                  [ISTANBUL, ISTANBUL, 1],
                  [CAIRO, CAIRO, 1]]]
Cairo =         [BLACK,  0,0,0,0, 0,
                 [[CAIRO, CAIRO, 0],
                  [ALGIERS, ALGIERS, 1],
                  [KHARTOUM, KHARTOUM, 1],
                  [ISTANBUL, ISTANBUL, 1],
                  [BAGHDAD, BAGHDAD, 1],
                  [RIYADH, RIYADH, 1]]]
Istanbul =      [BLACK,  0,0,0,0, 0,
                 [[ISTANBUL, ISTANBUL, 0],
                  [MILAN, MILAN, 1],
                  [ALGIERS, ALGIERS, 1],
                  [CAIRO, CAIRO, 1],
                  [BAGHDAD, BAGHDAD, 1],
                  [MOSCOW, MOSCOW, 1],
                  [STPETERSBURG, STPETERSBURG, 1]]]
Moscow =        [BLACK,  0,0,0,0, 0,
                 [[MOSCOW, MOSCOW, 0],
                  [STPETERSBURG, STPETERSBURG, 1],
                  [ISTANBUL, ISTANBUL, 1],
                  [TEHRAN, TEHRAN, 1]]]
Baghdad =       [BLACK,  0,0,0,0, 0,
                 [[BAGHDAD, BAGHDAD, 0],
                  [ISTANBUL, ISTANBUL, 1],
                  [CAIRO, CAIRO, 1],
                  [RIYADH, RIYADH, 1],
                  [KARACHI, KARACHI, 1],
                  [TEHRAN, TEHRAN, 1]]]
Riyadh =        [BLACK,  0,0,0,0, 0,
                 [[RIYADH, RIYADH, 0],
                  [CAIRO, CAIRO, 1],
                  [BAGHDAD, BAGHDAD, 1],
                  [KARACHI, KARACHI, 1]]]
Tehran =        [BLACK,  0,0,0,0, 0,
                 [[TEHRAN, TEHRAN, 0],
                  [MOSCOW, MOSCOW, 1],
                  [BAGHDAD, BAGHDAD, 1],
                  [KARACHI, KARACHI, 1],
                  [DELHI, DELHI, 1]]]
Karachi =       [BLACK,  0,0,0,0, 0,
                 [[KARACHI, KARACHI, 0],
                  [BAGHDAD, BAGHDAD, 1],
                  [RIYADH, RIYADH, 1],
                  [MUMBAI, MUMBAI, 1],
                  [DELHI, DELHI, 1],
                  [TEHRAN, TEHRAN, 1]]]
Mumbai =        [BLACK,  0,0,0,0, 0,
                 [[MUMBAI, MUMBAI, 0],
                  [KARACHI, KARACHI, 1],
                  [DELHI, DELHI, 1],
                  [CHENNAI, CHENNAI, 1]]]
Delhi =         [BLACK,  0,0,0,0, 0,
                 [[DELHI, DELHI, 0],
                  [TEHRAN, TEHRAN, 1],
                  [KARACHI, KARACHI, 1],
                  [MUMBAI, MUMBAI, 1],
                  [CHENNAI, CHENNAI, 1],
                  [KOLKATA, KOLKATA, 1]]]
Chennai =       [BLACK,  0,0,0,0, 0,
                 [[CHENNAI, CHENNAI, 0],
                  [MUMBAI, MUMBAI, 1],
                  [DELHI, DELHI, 1],
                  [KOLKATA, KOLKATA, 1],
                  [BANGKOK, BANGKOK, 1],
                  [JAKARTA, JAKARTA, 1]]]
Kolkata =       [BLACK,  0,0,0,0, 0,
                 [[KOLKATA, KOLKATA, 0],
                  [DELHI, DELHI, 1],
                  [CHENNAI, CHENNAI, 1],
                  [BANGKOK, BANGKOK, 1],
                  [HONGKONG, HONGKONG, 1]]]
Bangkok =       [RED,    0,0,0,0, 0,
                 [[BANGKOK, BANGKOK, 0],
                  [KOLKATA, KOLKATA, 1],
                  [CHENNAI, CHENNAI, 1],
                  [JAKARTA, JAKARTA, 1],
                  [HOCHIMINHCITY, HOCHIMINHCITY, 1],
                  [HONGKONG, HONGKONG, 1]]]
Jakarta =       [RED,    0,0,0,0, 0,
                 [[JAKARTA, JAKARTA, 0],
                  [CHENNAI, CHENNAI, 1],
                  [SYDNEY, SYDNEY, 1],
                  [HOCHIMINHCITY, HOCHIMINHCITY, 1],
                  [HONGKONG, HONGKONG, 1],
                  [KOLKATA, KOLKATA, 1]]]
Sydney =        [RED,    0,0,0,0, 0,
                 [[SYDNEY, SYDNEY, 0],
                  [JAKARTA, JAKARTA, 1],
                  [MANILA, MANILA, 1],
                  [LOSANGELES, LOSANGELES, 1]]]
HoChiMinhCity = [RED,    0,0,0,0, 0,
                 [[HOCHIMINHCITY, HOCHIMINHCITY, 0],
                  [BANGKOK, BANGKOK, 1],
                  [JAKARTA, JAKARTA, 1],
                  [MANILA, MANILA, 1],
                  [HONGKONG, HONGKONG, 1]]]
Manila =        [RED,    0,0,0,0, 0,
                 [[MANILA, MANILA, 0],
                  [HOCHIMINHCITY, HOCHIMINHCITY, 1],
                  [SYDNEY, SYDNEY, 1],
                  [SANFRANCISCO, SANFRANCISCO, 1],
                  [TAIPEI, TAIPEI, 1],
                  [HONGKONG, HONGKONG, 1]]]
HongKong =      [RED,    0,0,0,0, 0,
                 [[HONGKONG, HONGKONG, 0],
                  [KOLKATA, KOLKATA, 1],
                  [BANGKOK, BANGKOK, 1],
                  [HOCHIMINHCITY, HOCHIMINHCITY, 1],
                  [MANILA, MANILA, 1],
                  [TAIPEI, TAIPEI, 1],
                  [SHANGHAI, SHANGHAI, 1]]]
Taipei =        [RED,    0,0,0,0, 0,
                 [[TAIPEI, TAIPEI, 0],
                  [HONGKONG, HONGKONG, 1],
                  [MANILA, MANILA, 1],
                  [OSAKA, OSAKA, 1],
                  [SHANGHAI, SHANGHAI, 1]]]
Osaka =         [RED,    0,0,0,0, 0,
                 [[OSAKA, OSAKA, 0],
                  [TOKYO, TOKYO, 1],
                  [TAIPEI, TAIPEI, 1]]]
Tokyo =         [RED,    0,0,0,0, 0,
                 [[TOKYO, TOKYO, 0],
                  [SEOUL, SEOUL, 1],
                  [SHANGHAI, SHANGHAI, 1],
                  [OSAKA, OSAKA, 1],
                  [SANFRANCISCO, SANFRANCISCO, 1]]]
Seoul =         [RED,    0,0,0,0, 0,
                 [[SEOUL, SEOUL, 0],
                  [BEIJING, BEIJING, 1],
                  [SHANGHAI, SHANGHAI, 1],
                  [TOKYO, TOKYO, 1]]]
Shanghai =      [RED,    0,0,0,0, 0,
                 [[SHANGHAI, SHANGHAI, 0],
                  [BEIJING, BEIJING, 1],
                  [SEOUL, SEOUL, 1],
                  [TOKYO, TOKYO, 1],
                  [TAIPEI, TAIPEI, 1],
                  [HONGKONG, HONGKONG, 1]]]
Beijing =       [RED,    0,0,0,0, 0,
                 [[BEIJING, BEIJING, 0],
                  [SEOUL, SEOUL, 1],
                  [SHANGHAI, SHANGHAI, 1]]]
Epidemic = EPIDEMIC

roleCards = [CONTINGENCY, DISPATCHER, MEDIC, OPERATIONS, QUARANTINE,
             RESEARCHER, SCIENTIST]
gameBoard = [Atlanta, Washington, SanFransisco, Chicago, Montreal, NewYork,
             London, Madrid, Paris, Essen, Milan, StPetersburg, LosAngeles,
             MexicoCity, Miami, Bogota, Lima, Santiago, BuenosAires, SaoPaulo,
             Lagos, Kinsasha, Johannesburg, Khartoum, Algiers, Cairo, Istanbul,
             Moscow, Baghdad, Riyadh, Tehran, Karachi, Mumbai, Delhi, Chennai,
             Kolkata, Bangkok, Jakarta, Sydney, HoChiMinhCity, Manila,
             HongKong, Taipei, Osaka, Tokyo, Seoul, Shanghai, Beijing]
playDeck = [ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK,
            LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES,
            MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO,
            LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL,
            MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI, DELHI, CHENNAI,
            KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG,
            TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING, GOVGRANT, AIRLIFT,
            FORECAST, ONEQUIETNIGHT, RESILIENTPOP]
infectDeck = [ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK,
              LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES,
              MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO,
              LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO,
              ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI,
              DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY,
              MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING]
thingy = [0,0]
cityDistance = thingy[0]
previousStep = thingy[1]

gameOver = 0

researchStations = [ATLANTA, -1, -1, -1, -1, -1]
outbreakMarker = 0
infectionRateMarker = 0
OneQuietNightMarker = 0
cures = [-1, UNCURED, UNCURED, UNCURED, UNCURED]
blocksRemaining = [-1, 24, 24, 24, 24]
colorsRemaining = [-1, 12, 12, 12, 12]
epidemicThisTurn = 0

players = []
infectDiscard = []
intensify = []
playerDiscard = []
outbreakList = []


#This method examines a city to see if it neighbors another city.  it takes as
#arguments of the home city's index, and the destination city's index.  It
#modifies no variables.
def check_neighbors(home, destination):
    #Save the home city's actual city info.
    home = gameBoard[home]
    #loop through the home city's neighbors
    for i in xrange(len(home[NEIGHBORS])):
        #If the destination index is one of the neighbors
        if destination == home[NEIGHBORS][i][0] and i != 0:
            #return true
            return 1
    #Return false if true is never returned.
    return 0


#This method creates a 2d array of distances.  It is detailed below the method.
def create_distances():
    distance = np.zeros(shape = (len(gameBoard),len(gameBoard)))
    previous = np.zeros(shape = (len(gameBoard),len(gameBoard)))
    for home in xrange(len(gameBoard)):
        for destination in xrange(len(gameBoard)):
            if home == destination:
                distance[home,destination] = 0
                previous[home,destination] = destination
            elif check_neighbors(home, destination) == 1:
                distance[home,destination] = 1
                previous[home,destination] = home
            else:
                distance[home, destination] = 48
                previous[home, destination] = -1
    for intermediary in xrange(len(gameBoard)):
        for home in xrange(len(gameBoard)):
            for destination in xrange(len(gameBoard)):
                d1 = distance[home, intermediary]
                d2 = distance[intermediary, destination]
                d3 = distance[home, destination]
                if d1 + d2 < d3:
                    d3 = d1 + d2
                    distance[home, destination] = d3
                    previous[home, destination] = intermediary
    return [distance, previous]

def get_path(home, destination):
    if home == destination or check_neighbors(home, destination) == 1:
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
        shuffledList.append(givenList.pop(np.random.random_integers(0,len(
            givenList)-1)))
    #Then return the formerly-blank list
    return shuffledList


#This method is caled every time a City needs to be infected.  It takes as
#arguments the index of the city being infected, and, optionally, the color of
#disease the city is being infected with.  It modifies global variables
#gameBoard and blocksRemaining.
def infect(city, *args):
    for i in xrange(len(players)):
        #If any of the players are a Quarantine specialist
        if (player[i][ROLE] == QUARANTINE):                                    
            #find the city they are in
            location = player[i][LOCATION]
            #If they're in the city being infected...
            if (gameBoard[location] == city):
                #it's quarantined and cannot be infected.
                return city                                                    
            for j in xrange(len(gameBoard[location][NEIGHBORS])):
                #Then loop through the city's neighbors
                #if the city being infected is one of them...
                if (city == gameboard[player[i][LOCATION]][NEIGHBORS][j]
                    [CITYINDEX] and gameboard[player[i][LOCATION]][NEIGHBORS][j]
                    [STEPS] == NEIGHBORING):
                    #it's quarantined and cannot be infected.
                    return city
                
        if (player[i][ROLE] == MEDIC and cures[city[COLOR]] > 0):
            #If there's a medic in the city and the disease being added is
            #already cured, skip it.
            return city
    #if a specific color disease should be added (such as with Outbreaks)
    if len(args) == 1:
        if (cures[args[0]] < ERADICATED):
            #increment disease token of passed-on color by 1.
            city[args[0]] += 1
            #Disease tokens are capped at 3 per city
            if (city[args[0]] > 3):
                city[args[0]] = 3
                #If the city hasn't outbroken already from this infect card...
                if (outbreakList.count(city) == 0):
                    #It will now!
                    outbreak(city)
            else:
                #Otherwise, remove one disease token from the pool
                blocksRemaining[args[0]] -= 1
                if (blocksRemaining[args[0]] == 0):
                    #if no disease tokens of that color remain, the game ends.
                    gameOver()
                    
    #Otherwise, use the city's color
    else:
        color = city[COLOR]
        if (cures[color] < ERADICATED):
            city[color] += 1
            #increment disease token of correct color by 1.
            if (city[color] > 3):
                #Disease tokens are capped at 3 per city
                city[color] = 3
                if (outbreakList.count(city) == 0):
                    #If the city hasn't outbroken already from this infect card...
                    outbreak(city)
                    #It will now!
            else:
                blocksRemaining[color] -= 1
                #Otherwise, remove one disease token from the pool
                if (blocksRemaining[color] == -1):
                    gameOver()
                    #if no disease tokens of that color remain, the game ends.
    return city
    #Pass the city back so gameBoard can update.


#This method makes the game a thing!  It takes as arguments the number of
#playes, and the number of Epidemic cards to use- the difficulty.  It modifies
#EVERY global variable, defining many of them.
def create_game(players, difficulty):
    global roleCards
    #These cards are randomly given to players, assigning them roles for the
    #game.
    roleCards = shuffle([CONTINGENCY, DISPATCHER, MEDIC, OPERATIONS,
                         QUARANTINE, RESEARCHER, SCIENTIST])
    global gameBoard
    #This lists all the city objects in the game, indexed by location.
    gameBoard = [Atlanta, Washington, SanFransisco, Chicago, Montreal, NewYork,
                 London, Madrid, Paris, Essen, Milan, StPetersburg, LosAngeles,
                 MexicoCity, Miami, Bogota, Lima, Santiago, BuenosAires,
                 SaoPaulo, Lagos, Kinsasha, Johannesburg, Khartoum, Algiers,
                 Cairo, Istanbul, Moscow, Baghdad, Riyadh, Tehran, Karachi,
                 Mumbai, Delhi, Chennai, Kolkata, Bangkok, Jakarta, Sydney,
                 HoChiMinhCity, Manila, HongKong, Taipei, Osaka, Tokyo, Seoul,
                 Shanghai, Beijing]
    global playDeck
    #This lists all the player cards in the game- they are actually Int values
    #that serve either as indexes for gameBoard's cities, or as placeholders
    #for Event cards
    playDeck = shuffle([ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL,
                        NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN,
                        STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA,
                        LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS, KINSASHA,
                        JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL,
                        MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI,
                        DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY,
                        HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO,
                        SEOUL, SHANGHAI, BEIJING, GOVGRANT, AIRLIFT, FORECAST,
                        ONEQUIETNIGHT, RESILIENTPOP])
    global infectDeck
    #This lists all of the Infect cards in the gamethey are actually Int values
    #that serve as indexes for gameBoard's cities.
    infectDeck = shuffle([ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL,
                          NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN,
                          STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA,
                          LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS,
                          KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO,
                          ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI,
                          MUMBAI, DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA,
                          SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI,
                          OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING])
    #This creates the distances and pathing between cities on the gameboard.
    thingy = create_distances()
    cityDistance = thingy[0]
    previousStep = thingy[1]

    global gameOver
    gameOver = 0

    #Each of these global variables track some aspect of the game
    global researchStations
    researchStations = [ATLANTA, -1, -1, -1, -1, -1]
    global outbreakMarker
    outbreakMarker = 0
    global infectionRateMarker
    infectionRateMarker = 0
    global OneQuietNightMarker
    OneQuietNightMarker = 0
    global cures
    cures = [-1, UNCURED, UNCURED, UNCURED, UNCURED]
    global blocksRemaining
    blocksRemaining = [-1, 24, 24, 24, 24]
    global colorsRemaining
    colorsRemaining = [-1, 12, 12, 12, 12]
    global epidemicThisTurn
    epidemicThisTurn = 0

    #This for loop infects three cities with 3 cubes, three with 2 and 3 with 1
    #as part of the board's initial setup.  The cards are discarded to the
    #infectDiscard pile.
    for i in xrange(9):
        card = infectDeck.pop(0)
        if i < 3:
            gameBoard[card] = infect(gameBoard[card])
            gameBoard[card] = infect(gameBoard[card])
            gameBoard[card] = infect(gameBoard[card])
        elif i > 2 and i < 6:
            gameBoard[card] = infect(gameBoard[card])
            gameBoard[card] = infect(gameBoard[card])
        else:
            gameBoard[card] = infect(gameBoard[card])
        infectDiscard.append(card)

    #This generates the players, places them in the Players array, and gives
    #them cards for their hand.
    if (players == 2):
        #player = [Role, Location, stored card, actions remaining, cards in
        #          hand]
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2]
        for i in xrange(4):
            player1[HAND].append(playDeck.pop(0))
            player2[HAND].append(playDeck.pop(0))
    elif (players == 3):
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player3 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2, player3]
        for i in xrange(3):
            player1[HAND].append(playDeck.pop(0))
            player2[HAND].append(playDeck.pop(0))
            player3[HAND].append(playDeck.pop(0))
    elif (players == 4):
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player3 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player4 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2, player3, player4]
        for i in xrange(2):
            player1[HAND].append(playDeck.pop(0))
            player2[HAND].append(playDeck.pop(0))
            player3[HAND].append(playDeck.pop(0))
            player4[HAND].append(playDeck.pop(0))

    #This long and annoying section cuts the remaining player cards into small
    #piles, adds Epidemic cards to them, and shuffles them individually before
    #recombining them to create the PlayerDeck.  This puts a little breathing
    #room between each Epidemic.  Usually.
    cut1 = []
    cut2 = []
    cut3 = []
    cut4 = []
    if (difficulty == 4):
        for i in xrange(11):
            cut1.append(playDeck.pop(0))
            cut2.append(playDeck.pop(0))
            cut3.append(playDeck.pop(0))
            cut4.append(playDeck.pop(0))
        cut1.append(Epidemic)
        cut2.append(Epidemic)
        cut3.append(Epidemic)
        cut4.append(Epidemic)
        if players != 3:
            cut1.append(playDeck.pop(0))
        playDeck = shuffle(cut1) + shuffle(cut2) + shuffle(cut3)
        playDeck += shuffle(cut4)
    elif (difficulty == 5):
        cut5 = []
        for i in xrange(8):
            cut1.append(playDeck.pop(0))
            cut2.append(playDeck.pop(0))
            cut3.append(playDeck.pop(0))
            cut4.append(playDeck.pop(0))
            cut5.append(playDeck.pop(0))
        cut1.append(playDeck.pop(0))
        cut2.append(playDeck.pop(0))
        cut3.append(playDeck.pop(0))
        cut4.append(playDeck.pop(0))
        cut5.append(playDeck.pop(0))
        if players == 3:
            cut5.append(playDeck.pop(0))
        cut1.append(Epidemic)
        cut2.append(Epidemic)
        cut3.append(Epidemic)
        cut4.append(Epidemic)
        cut5.append(Epidemic)
        playDeck = shuffle(cut1) + shuffle(cut2) + shuffle(cut3)
        playDeck += shuffle(cut4) + shuffle(cut5)
    elif (difficulty == 6):
        cut5 = []
        cut6 = []
        for i in xrange(7):
            cut1.append(playDeck.pop(0))
            cut2.append(playDeck.pop(0))
            cut3.append(playDeck.pop(0))
            cut4.append(playDeck.pop(0))
            cut5.append(playDeck.pop(0))
            cut6.append(playDeck.pop(0))
        cut1.append(playDeck.pop(0))
        cut2.append(playDeck.pop(0))
        if players == 3:
            cut3.append(playDeck.pop(0))
        cut1.append(Epidemic)
        cut2.append(Epidemic)
        cut3.append(Epidemic)
        cut4.append(Epidemic)
        cut5.append(Epidemic)
        cut6.append(Epidemic)
        playDeck = shuffle(cut1) + shuffle(cut2) + shuffle(cut3)
        playDeck += shuffle(cut4) + shuffle(cut5) + shuffle(cut6)
        
    epidemicLikelihood = len(playDeck) / difficulty  #Odds that an epidemic
    #will be drawn next turn; starts at full, goes down by 1 for each turn
    #until an epidemic is drawn
    turn = len(playDeck)/2  #Each turn, two cards are drawn.
    #this notes how many turns there are in which to win the game.


#This method is called at the end of every turn: it takes the infection rate
#   as an argument, draws 2, 3, or 4 cards from the Infect Deck, and infects
#   them, potentially causing Outbreaks.  This modifies the global variables
#   gameBoard, infectDeck, infectDiscard, and outbreakList.
def infection_stage(infectionRate):
    global outbreakList
    global infectDeck
    global infectDiscard
    global gameBoard
    #Clear the outbreak list before infecting, just in case.
    outbreakList = []
    #Draw a card from the Infect Deck
    index = infectDeck.pop(0)
    #Infect the card's city and update gameBoard
    gameBoard[index] = infect(gameBoard[index])
    #Discard the drawn card to the Infect Discard Pile
    infectDiscard.append(index)
    #Clear the outbreak list again, because we aren't done yet.
    outbreakList = []
    #Rinse and repeat at least once.
    index = infectDeck.pop(0)
    gameBoard[index] = infect(gameBoard[index])
    infectDiscard.append(index)
    outbreakList = []
    #If the infection rate is 2 or more, infect one more city
    if infectionRate > 2:
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
        outbreakList = []
    #If the Infection Rate is 6 or more, infect a fourth city.
    if infectionRate > 5:
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
        outbreakList = []


#This method is called when a city has more than three disease cubes of the
#   same color on it, causing an Outbreak.  It takes as an argument the
#   outbreaking city.  It calls infect on each of the city's neighbors, passing
#   an additional argument of the outbreaking city's color so the correct
#   disease cubes will be placed on each neighboring city.  This modifies the
#   global variables outbreakList and gameBoard, and potentially modifies
#   gameOver.
def outbreak(city):
    global outbreakList
    global outbreakMarker
    #add the city to the Outbreak List so it cannot Outbreak twice from one
    #Infect card.
    outbreakList.append(city)
    #Increment the outbreak Marker global variable
    outbreakMarker += 1
    #If the outbreak marker reaches 8, the game ends.
    if outbreakMarker == 8:
        gameOver()
    else:
        #otherwise, loop through each of the outbreaking city's neighbors...
        for i in xrange(len(city[NEIGHBORS:])):
            #make sure they're actually neighbors (sloppy coding, I know)
            if(city[NEIGHBORS][i][STEPS] == NEIGHBORING):
                #and infect them with the outbreaking city's color of disease
                gameBoard[city[NEIGHBORS
                               ][i][CITYINDEX]] = infect(city[NEIGHBORS][i]
                                                                [CITYINDEX],
                                                                city[COLOR])


#This method is called when an Epidemic card is drawn by a player.  It takes no
#   arguments (from anyone), and does what it wants.  More accurately, this
#   method increments the Infection Rate marker by one, draws an Infect card
#   from the bottom of the Infect Deck, infects that city three times, and then
#   takes all the cards out of the Infection Discard pile, shuffles them, and
#   puts them back ontop of the Infect Deck so they can be drawn again and
#   really kick the player's teeth in.  This modifies the following Global
#   Variables: gameBoard, infectionRateMarker, InfectDeck, InfectDiscard,
#   Intensify, and EpidemicThisTurn.
def epidemic():
    global infectionRateMarker
    global infectDeck
    global gameBoard
    global intensify
    #Note that an epidemic happened this turn
    epidemicThisTurn = 1
    #Increment the Infection Rate Marker.  Everything just got tougher!
    infectionRateMarker += 1
    #Draw the bottom card from the Infect Deck.
    index = infectDeck.pop()
    #Grab the city that card indicates from the Game Board
    epidemicCard = gameBoard[index]
    #And infect it three times, updating the game board each time.
    gameBoard[index] = infect(epidemicCard)
    gameBoard[index] = infect(epidemicCard)
    gameBoard[index] = infect(epidemicCard)
    #Then discard the card to the Infect Discard Pile
    infectDiscard.append(index)
    #Clear the Intensify list: while not technically part of the game rules,
        #tracking which cards went back onto the Infect Deck is an essential
        #part of winning the game.  Obviously, no peeking.
    intensify = []
    #Then, loop through the entire Infect Discard Pile
    while (len(infectDiscard)>0):
        #grab one card from it at random
        card = infectDiscard.pop(np.random.random_integers(0,len(infectDiscard)
                                                           -1))
        #Add the card to the Intensify list so the AI will know it's coming up
            #very soon
        intensify.append(card)
        #and place the card ontop of the Infect Deck
        infectDeck.insert(0,index)
    #Shuffle the Intensify list so the order the cards were placed on the
        #Infect Deck is obscured.
    intensify = shuffle(intensify)
    #And finally, if One Quiet Night hasn't been played...
    if OneQuietNightMarker == 0:
        #Infect.
        infecton_stage(infectionRateMarker)


#This method is called whenever a player uses the Treat action.  It takes as
    #arguments the player's Player list, and the color of disease the player
    #is treating.  If the disease has been cured OR the player is a Medic,
    #this method cures all disease cubes of the chosen color at the player's
    #current location.  If the disease has not been cured AND the player is not
    #a medic, it removes only one of the disease cubes of the chosen color.
    #This method modifies the global variables gameBoard and blocksRemaining,
    #as well as the (non-global) player's Player list
def treat(player, color): #Not sure how to break this If statement up...
    #Check to see if the Player has an Action remaining, and if either the
        #player is a Medic XOR the disease has been cured.
    if (player[ROLE] == MEDIC or cures[color] == CURED):
        if(player[ROLE] != MEDIC or cures[color] != CURED):
            if player[ACTIONS] > 0:
                #If the above is true, the player must spend an action Treating.
                player[ACTIONS] = player[ACTIONS] - 1
                #store the number of disease cubes of that color which are at
                #the player's location.
                cubes = gameBoard[player[LOCATION]][color]
                #Clear those cubes off the game board,
                gameBoard[player[LOCATION]][color] = 0
                #and put them back into the bin for later use.
                blocksRemaining[color] = blocksRemaining[color] + cubes
    #Otherwise, if the player has an action left
    elif (player[ACTIONS] > 0):
        #Remove one cube of the chosen color from the player's location
        gameBoard[player[LOCATION]][color] = gameBoard[player[LOCATION]
                                                       ][color] - 1
        
        #add it back into the blocks Remaining pool
        blocksRemaining[color] = blocksRemaining[color] + 1
        #and reduce the player's actions remaining by one.
        player[ACTIONS] = player[ACTIONS] - 1


#This method allows a player to start to move.  It takes as arguments the
#player being moved, the destination the player has in mind, and a possible
#additional argument of the number of steps to make (if the player does not
#wish to move all the way to a distant destination this turn and has other
#actions in mind), and the Dispatcher who may be using their action to pay
#for the movement instead of the player being moved.  It modifies no global
#variables- Hooray!
def move_player(player, destinationIndex, *args):
    if len(args) == 0:
        #Without arguments, the method assumes the player wishes to get to their
        #destination as quickly as possible and uses all remaining actions to do
        #so until they get to their destination.
        while player[ACTIONS] > 0 and player[LOCATION] != destinationIndex:
            #Move the player one step towards their destination, getting pathing
            #info from get_path.
            move_action(player, get_path(player[LOCATION], destinationIndex))
    if len(args) == 1:
        #The first optional argument will always be the number of actions the
        #player wishes to spend on movement.
        steps = args[0]
        #for each action...
        for i in xrange(steps):
            #check to see if the player has enough remaining actions...
            if player[ACTIONS] > 0:
                #and then move them using the info from get_path.
                move_action(player, get_path(player[LOCATION], destinationIndex))
    #If there's more than one argument provided (with no error proofing, of
    #course!), then we assume it's a Dispatcher using his actions to move
    #another player!
    else:
        #Grab the number of actions the Dispatcher wants to spend...
        steps = args[0]
        #and the Dispatcher's player list, too, while we're at it.
        dispatcher = args[1]
        #Then, for each action indicated in Steps...
        for i in xrange(steps):
            #make sure the Dispatcher has enough actions and the player hasn't
            #arrived...
            if dispatcher[ACTIONS] > 0 and player[LOCATION] != destinationIndex:
                #and move the player if he does, adding the additional argument
                #of the dispatcher's player list to the move_action method call.
                move_action(player, get_path(player[LOCATION], destinationIndex)
                           , dispatcher)


#This method is what actually handles the walking part of movement.  It takes
#arguments of the player being moved, the player's destination, and, optionally,
#the dispatcher who will be paying for the movement with his Actions.  This
#method modifies no global variables- hooray!  However, it does modify up to
#two Player Lists.
def move_action(player, destinationIndex, *args):
    #If there's no dispatcher paying for the movement...
    if len(args) == 0:
        #check (again) to see the player has the actions for this movement
        if player[ACTIONS] > 0:
            #grab the player's current location
            location = gameBoard[player[LOCATION]]
            #look through the player's location's list of neighbors...
            for i in xrange(len(location[NEIGHBORS])):
                #if the destination index is one of them...
                if (location[NEIGHBORS
                             ][i][CITYINDEX] == destinationIndex and location[
                                 NEIGHBORS][i][STEPS] == NEIGHBORING):
                    #Move the player there,
                    player[LOCATION] = destinationIndex
                    #and consume one of the player's actions.
                    player[ACTIONS] = player[ACTIONS] - 1
    #If there is a dispatcher paying for the movement...
    else:
        #Get the kind soul's player list from *args- again, no error checking!
        dispatcher = args[0]
        #Verify (again) that the Dispatcher has the actions for this movement...
        if dispatcher[ACTIONS] > 0:
            #save the player (not dispatcher) location.
            location = gameBoard[player[LOCATION]]
            #Check all of that locations' neighbors.
            for i in xrange(len(location[NEIGHBORS])):
                #If the player's destination is one of them,
                if (location[NEIGHBORS
                             ][i][CITYINDEX] == destinationIndex and location[
                                 NEIGHBORS][i][STEPS] == NEIGHBORING):
                    #Move the player there,
                    player[LOCATION] = destinationIndex
                    #and consume one of the Dispatcher's actions.
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1


#This method is Direct Flight, one of the more useful means of travel around the
#board.  This method takes as arguments the player, the index of the city the
#player wishes to fly to, and, optionally, the Dispatcher who is paying for the
#player's movement.  It modifiesthe global variables of PlayerDiscard and
#colorsRemaining, as a city card must be discarded for a Direct Flight.
def direct_flight(player, destinationIndex, *args):
    #No dispatcher, so pay your own way...
    if len(args) == 0:
        #Action check!
        if player[ACTIONS] > 0:
            #look through the list of cards that is the player's hand...
            for i in xrange(len(player[HAND])):
                #and check to see if one of these cards is the destination city.
                if destinationIndex == player[HAND][i]:
                    #If it is, note that a card of the city's color has been
                    #discarded using the colorsRemaining list.
                    colorsRemaining[gameBoard[player[HAND][i]][COLOR]] += -1
                    #Then discard the city card to the Player Discard pile
                    playerDiscard.append(player[HAND].pop(i))
                    #Update the player's location to the destination
                    player[LOCATION] = destinationIndex
                    #And consume one of the player's actions.
                    player[ACTIONS] = player[ACTIONS] - 1
                    break
    #If there IS a dispatcher...
    else:
        #Grab his player list.
        dispatcher = args[0]
        #Check he has the actions...
        if dispatcher[ACTIONS] > 0:
            #Loop through the dispatcher's hand
            for i in xrange(len(dispatcher[HAND])):
                #and see if he has the card matching the destination index.
                if destinationIndex == dispatcher[HAND][i]:
                    #These four lines are identical to the four above except
                    #that the dispatcher discards the city card and loses the
                    #action.
                    colorsRemaining[
                        gameBoard[dispatcher[HAND][i]][COLOR]] += -1
                    playerDiscard.append(dispatcher[HAND].pop(i))
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1
                    break


#This method allows players to discard a city's card while in that city to fly
#to any other city on the game board.  It takes as arguments the player, the
#destination city's index, and, optionally, the dispatcher who will be paying
#for the movement.It modifies the global variables of PlayerDiscard and
#colorsRemaining, as a city card must be discarded for a Charter Flight.
def charter_flight(player, destinationIndex, *args):
    #No dispatcher
    if len(args) == 0:
        #Action check
        if player[ACTIONS] > 0:
            #Loop through the player's hand
            for i in xrange(len(player[HAND])):
                #if the player has the city card for his current location...
                if player[LOCATION] == player[HAND][i]:
                    #note that a card of that city's color has been discarded
                    colorsRemaining[
                        gameBoard[player[HAND][i]][COLOR]] += -1
                    #Discard the card
                    playerDiscard.append(player[HAND].pop(i))
                    #Move the player to the new location
                    player[LOCATION] = destinationIndex
                    #Consume one action.
                    player[ACTIONS] = player[ACTIONS] - 1
                    #Missing a Break statement.
    #This section is identical to the one above, save that the Dispatcher
    #uses his action and discards the city card, not the player being moved.
    else:
        dispatcher = args[0]
        if dispatcher[ACTIONS] > 0:
            for i in xrange(len(dispatcher[HAND])):
                if player[LOCATION] == dispatcher[HAND][i]:
                    colorsRemaining[
                        gameBoard[dispatcher[HAND][i]][COLOR]] += -1
                    playerDiscard.append(dispatcher[HAND].pop(i))
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1
                    break;


#This method allows players to fly from one city to another, so long as both
#cities have Research Stations in them.  It takes arguments of the player
#who will be moving, the destination city's index, and, optionally, the
#dispatcher who will be paying for the movement.  It modifies no global
#variables- hooray!
def shuttle_flight(player, destinationIndex, *args):
    #No dispatcher
    if len(args) == 0:
        #If the player's location has a research station, the destination has a
        #Research Station, and the player has actions remaining this turn...
        if gameBoard[player[LOCATION]][RESEARCH] == 1:
            if gameBoard[destinationIndex][RESEARCH] == 1:
                 if player[ACTIONS] > 0:
                    #Move the player to the destination city
                    player[LOCATION] = destinationIndex
                    #And consume one action
                    player[ACTIONS] = player[ACTIONS] - 1
    #If there is a dispatcher, do the above, but the Dispatcher pays for
    #the movement instead.
    else:
        dispatcher = args[0]
        if gameBoard[player[LOCATION]][RESEARCH] == 1:
            if gameBoard[destinationIndex][RESEARCH] == 1:
                if dispatcher[ACTIONS] > 0:
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1


#this method allows a Dispatcher to move one player to any other player on the
#board.  It takes as arguments the dispatcher's player list, the moving player's
#player list, and the destination of the flight.  It modifies no global
#variables- hooray!
def dispatch_flight(dispatcher, player, destinationIndex):
    #If the dispatcher has enough actions...
    if dispatcher[ACTIONS] > 0:
        #loop through the list of all players.
        for i in xrange(len(players)):
            #if the destination index is also the location of a player,
            if destinationIndex == players[i][LOCATION]:
                #Consume one of the dispatcher's actions,
                dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1
                #and move the player to its new location.
                player[LOCATION] = players[i][LOCATION]          


#This method allows Operations Experts to fly from any city with a Research
#Station to any other city on the map at the price of any one card.  It takes,
#as arguments, a player list, the index of the destination city, and the index
#of the card being discarded for this travel.  It modifies the global variable
#playerDiscard and ColorsRemaining.
def operations_flight(player, destinationIndex, discardIndex):
    #If the player has an action remaining, has not used this move this turn,
    #and is an Opeations Expert.
    if player[ACTIONS] > 0 and player[STORED] == 0:
        if player[ROLE] == OPERATIONS:
            if gameBoard[player[LOCATION]][RESEARCH] == 1:
                #Note the color of the card being discarded in ColorsRemaining
                colorsRemaining[
                    gameBoard[player[HAND][discardIndex]][COLOR]] += -1
                #Discard the card to the playerDiscard pile
                playerDiscard.append(player[HAND].pop(discardIndex))
                #move the Operations Expert to his new location
                player[LOCATION] = destinationIndex
                #Consume one action
                player[ACTIONS] = player[ACTIONS] - 1
                #and note that the Operations Expert used Operations Flight
                #this turn.
                player[STORED] = 1


#This method allows players to build new Research Stations by discarding the
#card of the city they are both in and building the station in.  It takes, as
#arguments, the player's player list, and an optional argument of which
#pre-existing research station to remove if there are too many on the board.
#This method modifies the global variables gameBoard, researchStations,
#playerDiscard, and colorsRemaining.
def build_research(player, *args):
    #Check that there isn't ALREADY a research station at this location...
    if (gameBoard[player[LOCATION]][RESEARCH] == 1):
        return
    #if there are any arguments given...
    elif (len(args) > 0):
        #take the first one and delete the research station located at that
        #gameBoard index. Again, no error checking!
        gameBoard[args[0]][RESEARCH] = 0
        #And remove the above city from the list of research stations
        #This is in error- it should be -1, not 0.
        researchStations[researchStations.index(args[0])] = 0
    #If the player is an Operations Expert and has one or more action remaining
    if (player[ROLE] == OPERATIONS and player[ACTIONS] > 0):
        #Plop down the research station at his location
        gameBoard[player[LOCATION]][RESEARCH] = 1
        #Add the research station to the first open spot on the list
        researchStations[researchStations.index(-1)] = player[LOCATION]
        #eat an action
        player[ACTIONS] = player[ACTIONS] - 1
        #And force the player to discard one card- currently, at random, though
        #it should be a card of his choosing.  Will modify to use a second arg
        #for the index of the card to be discarded.  ERROR!
        discard(player)
    #if the player is NOT an operations expert, but has actions remaining,
    elif (player[ACTIONS] > 0):
        #Loop through the player's hand
        for i in xrange(len(player[HAND])):
            #if the player has the city card for his current location
            if player[LOCATION] == player[HAND][i]:
                #Build the research station there
                gameBoard[player[LOCATION]][RESEARCH] = 1
                #Note the color of the discarded city card in colorsRemaining
                colorsRemaining[gameBoard[player[LOCATION]][COLOR]] += -1
                #Discard the card
                playerDiscard.append(player[HAND].pop(i))
                #update the researchStations list with the new city's info
                researchStations[researchStations.index(-1)] = player[LOCATION]
                #and consume one action.
                player[ACTIONS] = player[ACTIONS] - 1


#This method allows a player to spend one action to give another player the
#city card of the city they are BOTH in, unless the giver is a Researcher; then
#she can give any city card she damn well pleases to.  It takes, as arguments,
#the player list of the giving player, the player list of the receiving player,
#and the index number of the card being given in the giver's hand.  It modifies
#no global variables- hooray!
def give_knowledge(giver, receiver, cardIndex):
    #If the giver and receiver are in the same city, the giver is a Researcher,
    #and the giver has at least one action left this turn...
    if (giver[LOCATION] == receiver[LOCATION] and giver[ROLE] == RESEARCHER):
        if (giver[ACTIONS] > 0):
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver[HAND].append(giver[HAND].pop(cardIndex))
            #Consume one of the giver's actions
            giver[ACTIONS] = giver[ACTIONS] - 1
            #And make sure the receiver has seven or fewer cards in his hand.
            handLimit(receiver)
    #If the giver and receiver are in the same location and the giver can act,
    elif giver[LOCATION] == receiver[LOCATION] and giver[ACTIONS] > 0:
        #and if the giver's location and the card are the same city...
        if giver[HAND][cardIndex] == giver[LOCATION]:
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver[HAND].append(giver[HAND].pop(cardIndex))
            #consume one action from the giver
            giver[ACTIONS] = giver[ACTIONS] - 1
            #and make sure the receiver has seven or fewer cards in his hand.
            handLimit(receiver)


#This method allows players to do the same as above, except the receiver spends
#the action instead of the giver.  This method takes arguments of the giver's
#player list, the receiver's player list, and the index of the card being taken
#This modifies no global variables- hooray!
def take_knowledge(giver, receiver, cardIndex):
    #If the giver is a Researcher, is in the same city as the Receiver,
    #and the receiver can act
    if (giver[LOCATION] == receiver[LOCATION] and giver[ROLE] == RESEARCHER):
        if (receiver[ACTIONS] > 0):
            #add the card to the Receiver's hand by popping it out of the hand
            #of the giver
            receiver[HAND].append(giver[HAND].pop(cardIndex))
            #consume one of the receiver's actions
            receiver[ACTIONS] = receiver[ACTIONS] - 1
            #and make sure he's got seven or fewer cards in his hand
            handLimit(receiver)
    #If the giver and receiver are in the same city, and the receiver can act
    elif giver[LOCATION] == receiver[LOCATION] and receiver[ACTIONS] > 0:
        #...and if the card being given matches their location
        if giver[HAND][cardIndex] == giver[LOCATION]:
            #Do the same as above.
            receiver[HAND].append(giver[HAND].pop(cardIndex))
            receiver[ACTIONS] = receiver[ACTIONS] - 1
            handLimit(receiver)


#This method allows players to Cure diseases by discarding five cards of the
#same color as the disease they are curing- or four cards, if the player is a
#Scientist.  This method takes, as arguments, a player list, and four or five
#args, each of which are the index location of one of the cards being discarded
#This method modifies the global variables of playerDiscard, and Cures.
def cure(player, *args):
    #If the player is a scientist, has an action, and is at a research station
    if player[ROLE] == SCIENTIST and player[ACTIONS] > 0:
        if gameBoard[player[LOCATION]][RESEARCH] == 1:
            #Create a list of the cities whose cards are being discarded...
            #these index values are each off by one.
            cities = [gameBoard[args[0]], gameBoard[args[1]],
                      gameBoard[args[2]], gameBoard[args[3]]]
            #loop through that list... this should probably be -1, not -2
            for i in xrange(len(cities)-2):
                #If one city's color does not match the next city's color...
                if cities[i][COLOR] != cities[i+1][COLOR]:
                    #Abort the cure; they're the wrong cards!
                    return
        #Otherwise, cure the disease!
        cures[cities[0][COLOR]] = CURED
        #Consume one action
        player[ACTIONS] = player[ACTIONS] - 1
        #discard each card
        playerDiscard.append(player[HAND][args[0]])
        #and note that they've been discarded in ColorsRemaining
        colorsRemaining[gameBoard[player[HAND][args[0]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[1]])
        colorsRemaining[gameBoard[player[HAND][args[1]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[2]])
        colorsRemaining[gameBoard[player[HAND][args[2]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[3]])
        colorsRemaining[gameBoard[player[HAND][args[3]]][COLOR]] += -1

    #If the player is not a scientist, but is in a research station...
    elif player[ACTIONS] > 0 and gameBoard[player[LOCATION]][RESEARCH] == 1:
        #Create a list of the cities whose cards are being discarded...
        #These index values are also off by one.
        cities = [gameBoard[args[1]], gameBoard[args[2]], gameBoard[args[3]],
                  gameBoard[args[4]], gameBoard[args[5]]]
        #Loop through that list
        for i in xrange(len(cities)-2):
            #Verify the cities are all the same color
            if cities[i][COLOR] != cities[i+1][COLOR]:
                #Abort if they aren't.
                return
        #Cure if they are!
        cures[cities[0][COLOR]] = CURED
        #Consume one action
        player[ACTIONS] = player[ACTIONS] - 1
        #discard each card
        playerDiscard.append(player[HAND][args[0]])
        #and note that they've been discarded in ColorsRemaining
        colorsRemaining[gameBoard[player[HAND][args[0]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[1]])
        colorsRemaining[gameBoard[player[HAND][args[1]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[2]])
        colorsRemaining[gameBoard[player[HAND][args[2]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[3]])
        colorsRemaining[gameBoard[player[HAND][args[3]]][COLOR]] += -1
        playerDiscard.append(player[HAND][args[4]])
        colorsRemaining[gameBoard[player[HAND][args[4]]][COLOR]] += -1

#This method allows a Contingency Planner to take one Event card out of the
#Discard pile and add it to his Player List for later use.  It takes as
#arguments the Contingency Planner's player list, and the event card he wishes
#to draw.  It modifies the global variables playerDiscard and ColorsRemaining.
def contingency(player, eventCard):
    #If the player's role is Contingency planner, the player has no other
    #event card stored, the event card he wants is in the discard pile, and
    #the contingency planner has enough actions...
    if player[ROLE] == CONTINGENCY and player[STORED] == 0:
        if playerDiscard.count(eventCard) > 0 and player[ACTIONS] > 0:
            #Draw the card out of the discard pile and attach it to the player
            #list
            player[STORED] = playerDiscard.pop(playerDiscard.index(eventCard))
            #and consume one action.
            player[ACTIONS] = player[ACTIONS] - 1



#Event Cards:

#This method is the Resilient Population event card.  It allows players to
#remove one city's Infect card from the Infect Discard pile, and remove it from
#the game so it cannot be drawn again.  It takes as arguments the player list
#of the player with the card, and the index of the city card to be reoved.  It
#modifies the global variables playerDiscard, and infectDiscard.
def resilient_population(player, card):
    #Remove the infect card from the discard pile and poof it into the e-ther.
    infectDiscard.pop(card)
    #If the player is a COntingency planner with the card stored...
    if player[ROLE] == CONTINGENCY and player[STORED] == RESILIENTPOP:
        #poof the card from storage and reset it to empty.
        player[STORED] = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        playerDiscard.append(
            player[HAND].pop(player[HAND].index(RESILIENTPOP)))
        


#This method allows players to use the Airlift card to instantly fly any player
#to any city of their choosing!  It takes as arguments the player list of the
#player with the card, the player list of the player doing the flying, and the
#city index of the destination city.  It modifies the global variable
#playerDiscard.
def airlift(player, target, destination):
    #Set the target player's location to the destination.
    target[LOCATION] = destination
    #If the player with the card is a contingency planner who stored the card
    if player[ROLE] == CONTINGENCY and player[STORED] == AIRLIFT:
        #Poof it into the e-ther.
        player[STORED] = 0
    #Otherwise...
    else:
        #place the card in the player discard pile
        playerDiscard.append(
            player[HAND].pop(player[HAND].index(AIRLIFT)))


#This event card allows a player to instantly build a research station anywhere
#on the game map.  It takes as arguments the player list of the player with the
#card, and the index of the city to get the shiny new research station.  It
#modifies the global variables of gameBoard and playerDiscard.
def gov_grant(player, city):
    #Add the research station to the destination city
    gameBoard[city][RESEARCH] = 1
    #if there's space left...
    if researchStations.count(-1) > 0:
        #Set the first available slot to the city's index.
        researchStations[researchStations.index(-1)] = city
        #ERROR!  If there are already six research stations, this should
        #require an *args of the city index of the station that will be removed
    #If the player's a Contingency planner playing the card from storage
    if player[ROLE] == CONTINGENCY and player[STORED] == GOVGRANT:
        #VANISH it.
        player[STORED] = 0
    #otherwise...
    else:
        #place the card in the player discard pile
        playerDiscard.append(
            player[HAND].pop(player[HAND].index(GOVGRANT)))


#This method allows players to skip the Infect stage on one turn.  It can be
#used to prevent an Epidemic from Infecting, but not from Intensifying.  It
#takes as arguments the player list of the player with the card, and modifies
#the global variable OneQuietNightMarker.
def one_quiet_night(player):
    #Set the OneQuietNightMarker to 1, skipping the Infect stage.
    OneQuietNightMarker = 1
    #COntingency Planner card removal
    if player[ROLE] == CONTINGENCY and player[STORED] == ONEQUIETNIGHT:
        player[STORED] = 0
    else:
        #place the card in the player discard pile
        playerDiscard.append(
            player[HAND].pop(player[HAND].index(ONEQUIETNIGHT)))


#This method allows players to use the Forecast card, rearranging the top six
#cards in the Infect Deck to their liking.  It takes, as arguments, the player
#list of the player with the card.
def forecast(player):
    #Draw the top six cards of the Infection Deck and put them in a list.
    topSix = [infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0),
              infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0)]
    #loop through that list once
    for i in xrange (len(topSix)):
        #If any of the cities have three cubes of any color on them...
        c = gameBoard[topSix[i]]
        if c[BLUE] == 3 or c[BLACK] == 3 or c[RED] == 3 or c[YELLOW] == 3:
            #Put them ontop first, popping them out of the list.
            #This might cause errors as the list length gets shorter...
            infectDeck.insert(0, topSix.pop(i))
    #Loop through the list again.
    for i in xrange (len(topSix)):
        #If any of the cities have two cubes of any color on them...
        c = gameBoard[topSix[i]]
        if c[BLUE] == 2 or c[BLACK] == 2 or c[RED] == 2 or c[YELLOW] == 2:
            #Put them on next, , popping them out of the list.
            #This might cause errors as the list length gets shorter...
            infectDeck.insert(0, topSix.pop(i))
    #Loop through again,
    for i in xrange (len(topSix)):
        #And put the rest ontop by popping them out of the list
        infectDeck.insert(0, topSix.pop(i))
    #This puts the cities back ontop in reverse order of the number of cubes
    #they have: heavily-infected cities are drawn last, lightly infected ones
    #are drawn first.

    #Same COntignecny planner stuff.
    if player[ROLE] == CONTINGENCY and player[STORED] == FORECAST:
        player[STORED] = 0
    else:
        #place the card in the player discard pile
        playerDiscard.append(
            player[HAND].pop(player[HAND].index(FORECAST)))


#This method forces a player to discard one card from their hand.  It takes as
#arguments the player list of the unfortunate soul who has to discard a card.
#It modifies the global variable playerDiscard.
def discard(player):    #The AI has to choose which card to discard and I have
    #no idea how to code that yet.  Event cards, too...  For now, randomness.
    chosenCard = np.random.random_int(0, len(player[HAND])-1)
    #the below is commented out code that would check if the discarded card is
    #an Event card, and play it if it were.
    #if (player[HAND][chosenCard] == GOVGRANT or player[HAND][chosenCard]
    #== ONEQUIETNIGHT or player[HAND][chosenCard] == AIRLIFT or
    #player[HAND][chosenCard] == FORECAST or player[HAND][chosenCard]
    #== RESILIENTPOP):
        #Play the event card instead of discarding it.
    #else:
    
    #Place the discarded card in the player discard pile.  Hey, this one works!
    playerDiscard.append(player[HAND].pop(chosenCard))


#This method does a bunch of different condition checks to ensure the rules are
#followed  It checks cures to see if the players have won, handles medic's free
#distribution of cures to infected cities, checks for eradicated diseases, and
#checks to see if the player it is passed needs to discard a card.  It takes as
#arguments the player list of the player whose turn it is.  It modifies the
#global variables gameOver, cures, gameBoard, and blocksRemaining.
def update_game(player):
    #If all four diseases are Cured or Eradicated...  (not sure how to shorten)
    if cures[BLUE] > 0 and cures[YELLOW] > 0 and cures[BLACK] > 0:
        if cures[RED] > 0:
            #The players win!
            #A very generous estimate says 1/3rd of games end this way.
            #Probably more like 1/5th or worse.
            gameOver = 1
    #If the player is a medic...
    if player[ROLE] == MEDIC:
        #Loop through the list of diseases...
        for color in xrange(len(cures)):
            #If a disease has been cured,
            if cures[color+1] == CURED:
                #store the number of disease cubes of that color which are at
                #the Medic's location.
                cubes = gameBoard[player[LOCATION]][color+1]
                #Clear those cubes off the game board,
                gameBoard[player[LOCATION]][color+1] = 0
                #and put them back into the bin for later use.
                blocksRemaining[color+1] = blocksRemaining[color+1] + cubes
    #Loop through the blocksRemaining list
    for i in xrange(len(blocksRemaining)):
        #If there are 24 cubes of a color in the list and that disease is cured
        if blocksRemaining[i] == 24 and cures[i] > 0:
            #That disease is eradicated and cannot spread anymore!
            cures[i] = ERADICATED
    #Check if the player's hand has more than seven cards...
    while len(player[HAND]) > 7:
        #And discard until it doesn't.
        discard(player)


#This method is the mechanics of a player's turn.  It will most likely become
#a while loop or something else once the AI is finished.  It takes a player's
#Player List as its only argument.
def player_turn(player):
    #Have the AI compile a risk assessment of the board
    riskAssessment = examine_board()
    #While the player has actions remaining...
    while player[ACTIONS] > 0 and gameOver == 0:
          
        #insert code for choosing an action here!

        #Refresh the game board after each action
        update_game(player)
    #If the player is Operations Expert
    if player[ROLE] == OPERATIONS:
        #Reset their stored value so they can take an operations flight later
        player[STORED] = 0
    #The player then draws a card
    card = playDeck.pop(0)
    #if it's an Epidemic...
    if card == EPIDEMIC:
        #Epidemic time!
        epidemic()
    #If not...
    else:
        #put the card in the player's hand
        player[HAND].append(card)
    #and draw another card, repeating the last few lines.
    card = playDeck.pop(0)                                    
    if card == EPIDEMIC:
        epidemic()
    else:
        player[HAND].append(card)
    #Update the board again- medic cures in case of Epidemics, and hand limit
    update_game(player)
    #if it's not One Quiet Night or an epidemic happened this turn
    if OneQuietNightMarker == 0 or epidemicThisTurn != 0:
        #call the infection_stage method and infect!
        infection_stage(infectionRateMarker)
    #If it is, or there was...
    else:
        #It isn't anymore, or the epidemic is cleared.
        OneQuietNightMarker = 0
        epidemicThisTurn = 0
    #update the board one last time, for medic cures.
    update_game(player)
    #Decrement the likelihood of another epidemic- information for the AI
    epidemicLikelihood = epidemicLikelihood - 1


#THis method ends the game.  It modifies the global variable gameOver.
def gameOver():
    gameOver = 1 



#this method is the beginnings of the AI for this game.  It creates a risk
#assessment of the board, examining each city and calculating how bad it could
#get should that city get infected.  It modifies no global variables- hooray!

#weights:
#Cubes remaining can be covered by examining blocksRemaining and comparing to
#the initial count of 24.  AI should look at board and determine how many cubes
#of each color could be placed based on outbreaks and similar
def examine_board():
    #Create a new empty risk assessment array.
    riskAssessment = []
    global gameBoard
    #Loop through the entire game board
    for i in xrange(len(gameBoard)):
        #populate the array with zeroes.
        riskAssessment.append(0)
        #Grab the city being examined by the loop
        city = gameBoard[i]
        #And iterate through the colors of its diseases.
        for color in xrange(4):
            #If it has any infection cubes
            if (city[color] <0):
                #increment it's risk assessment by one per cube.
                riskAssessment[i] = riskAssessment[i] + city[color]
                #If the city has three cubes of one color and coulkd outbreak,
                if city[color] == 3:
                    #Increment it's risk assessment by one more.
                    riskAssessment[i] += 1
                    #And look through all of its neighbors.
                    for neighbors in xrange(len(city[NEIGHBORS])):
                        #Grab the neighbor being looked at by the loop
                        neighbor = gameBoard[city[NEIGHBORS]][neighbors][0]
                        #If it's not the first 'neighbor' (the city itself)
                        if neighbors != 0:
                            #Increment the city's risk assessment by 1 for each
                            #neighbor it has
                            riskAssessment[i] += 1
                            #Then look at each neighbor's infection cubes.
                            for color2 in xrange(4):
                                #If they have 3 cubes of any one color...
                                if (neighbor[color2] == 3):
                                    #Increment the city's risk by one more.
                                    riskAssessment[i] += 1
                    #If the city being examined isn't in the infectDiscard pile
                    if infectDiscard.count(i) == 0:
                        #Increment it's risk by one more
                        riskAssessment[i] += 1
    #Testing print statement.  Whoopsie.
    print riskAssessment
    #Return the risk assessment list after all cities have been examined.
    return riskAssessment
                        


#Test the game mechanics by creating a game.  So far it works!
game = create_game(2,4)
print examine_board()
