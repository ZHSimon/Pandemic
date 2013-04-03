

import numpy as np
import operator
#Notes: this project will require a neural network- or carefully programmed weights- for each Role's AI to learn and adapt.  I'm not sure where to start with that...
#players will need to be aware of the number of cards of each color remaining in the deck, in all players' hands, and in the discard pile, and be aware of when they've hit their limit.



#7 role cards, 48 city cards, 6 epidemics, 5 events, 48 infection cards, 24x4 disease cubes, 48 nodes

#Death to magic numbers!  This is also the standardized index that every list uses to store the colors, so list[RED] will take you to Red.
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
pOffset = 4   #This marks the index location of the list of cards in a player's hand.  I'd rename it, but it's too widely used right now.

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
FORECAST = 50 #Currently puts cards back such that heavily-infected cities are drawn last.
ONEQUIETNIGHT = 51 #Finished
RESILIENTPOP = 52 #finished

#City terms:
COLOR = 0
BLOCKS = 2
RESEARCH = 5
cOffset = 6 #Marks the index location of the first neighboring city.
CITYINDEX = 0
NEXTSTEP = 1
STEPS = 2
NEIGHBORING = 1

#City name =    [Color, Disease tokens (Blue, Yellow, Black, Red), Research Station, Connected Cities by index and steps)
Atlanta =       [BLUE,   0,0,0,0, 1, [[ATLANTA, ATLANTA, 0], [CHICAGO, CHICAGO, 1], [WASHINGTON, WASHINGTON, 1], [MIAMI, MIAMI, 1]]]
Washington =    [BLUE,   0,0,0,0, 0, [[WASHINGTON, WASHINGTON, 0], [ATLANTA, ATLANTA, 1], [MONTREAL, MONTREAL, 1], [NEWYORK, NEWYORK, 1]]]
SanFransisco =  [BLUE,   0,0,0,0, 0, [[SANFRANCISCO, SANFRANCISCO, 0], [TOKYO, TOKYO, 1], [MANILA, MANILA, 1], [LOSANGELES, LOSANGELES, 1], [CHICAGO, CHICAGO, 1]]]
Chicago =       [BLUE,   0,0,0,0, 0, [[CHICAGO, CHICAGO, 0], [SANFRANCISCO, SANFRANCISCO, 1], [LOSANGELES, LOSANGELES, 1], [MEXICOCITY, MEXICOCITY, 1], [ATLANTA, ATLANTA, 1], [MONTREAL, MONTREAL, 1]]]
Montreal =      [BLUE,   0,0,0,0, 0, [[MONTREAL, MONTREAL, 0], [CHICAGO, CHICAGO, 1], [WASHINGTON, WASHINGTON, 1], [NEWYORK, NEWYORK, 1]]]
NewYork =       [BLUE,   0,0,0,0, 0, [[NEWYORK, NEWYORK, 0], [MONTREAL, MONTREAL, 1], [WASHINGTON, WASHINGTON, 1], [LONDON, LONDON, 1], [MADRID, MADRID, 1]]]
London =        [BLUE,   0,0,0,0, 0, [[LONDON, LONDON, 0], [NEWYORK, NEWYORK, 1], [MADRID, MADRID, 1], [PARIS, PARIS, 1], [ESSEN, ESSEN, 1]]]
Madrid =        [BLUE,   0,0,0,0, 0, [[MADRID, MADRID, 0], [NEWYORK, NEWYORK, 1], [LONDON, LONDON, 1], [SAOPAULO, SAOPAULO, 1], [ALGIERS, ALGIERS, 1], [PARIS, PARIS, 1]]]
Paris =         [BLUE,   0,0,0,0, 0, [[PARIS, PARIS, 0], [MADRID, MADRID, 1], [LONDON, LONDON, 1], [ESSEN, ESSEN, 1], [MILAN, MILAN, 1], [ALGIERS, ALGIERS, 1]]]
Essen =         [BLUE,   0,0,0,0, 0, [[ESSEN, ESSEN, 0], [LONDON, LONDON, 1], [PARIS, PARIS, 1], [MILAN, MILAN, 1], [STPETERSBURG, STPETERSBURG, 1]]]
Milan =         [BLUE,   0,0,0,0, 0, [[MILAN, MILAN, 0], [ESSEN, ESSEN, 1], [PARIS, PARIS, 1], [ISTANBUL, ISTANBUL, 1]]]
StPetersburg =  [BLUE,   0,0,0,0, 0, [[STPETERSBURG, STPETERSBURG, 0], [ESSEN, ESSEN, 1], [ISTANBUL, ISTANBUL, 1], [MOSCOW, MOSCOW, 1]]]
LosAngeles =    [YELLOW, 0,0,0,0, 0, [[LOSANGELES, LOSANGELES, 0], [SANFRANCISCO, SANFRANCISCO, 1], [CHICAGO, CHICAGO, 1], [MEXICOCITY, MEXICOCITY, 1], [SYDNEY, SYDNEY, 1]]]
MexicoCity =    [YELLOW, 0,0,0,0, 0, [[MEXICOCITY, MEXICOCITY, 0], [LOSANGELES, LOSANGELES, 1], [CHICAGO, CHICAGO, 1], [MIAMI, MIAMI, 1], [LIMA, LIMA, 1], [BOGOTA, BOGOTA, 1]]]
Miami =         [YELLOW, 0,0,0,0, 0, [[MIAMI, MIAMI, 0], [MEXICOCITY, MEXICOCITY, 1], [BOGOTA, BOGOTA, 1], [ATLANTA, ATLANTA, 1], [WASHINGTON, WASHINGTON, 1]]]
Bogota =        [YELLOW, 0,0,0,0, 0, [[BOGOTA, BOGOTA, 0], [MEXICOCITY, MEXICOCITY, 1], [LIMA, LIMA, 1], [BUENOSAIRES, BUENOSAIRES, 1], [SAOPAULO, SAOPAULO, 1], [MIAMI, MIAMI, 1]]]
Lima =          [YELLOW, 0,0,0,0, 0, [[LIMA, LIMA, 0], [MEXICOCITY, MEXICOCITY, 1], [BOGOTA, BOGOTA, 1], [SANTIAGO, SANTIAGO, 1]]]
Santiago =      [YELLOW, 0,0,0,0, 0, [[SANTIAGO, SANTIAGO, 0], [LIMA, LIMA, 1]]]
BuenosAires =   [YELLOW, 0,0,0,0, 0, [[BUENOSAIRES, BUENOSAIRES, 0], [BOGOTA, BOGOTA, 1], [SAOPAULO, SAOPAULO, 1]]]
SaoPaulo =      [YELLOW, 0,0,0,0, 0, [[SAOPAULO, SAOPAULO, 0], [BOGOTA, BOGOTA, 1], [BUENOSAIRES, BUENOSAIRES, 1], [MADRID, MADRID, 1], [LAGOS, LAGOS, 1]]]
Lagos =         [YELLOW, 0,0,0,0, 0, [[LAGOS, LAGOS, 0], [SAOPAULO, SAOPAULO, 1], [KINSASHA, KINSASHA, 1], [KHARTOUM, KHARTOUM, 1]]]
Kinsasha =      [YELLOW, 0,0,0,0, 0, [[KINSASHA, KINSASHA, 0], [LAGOS, LAGOS, 1], [KHARTOUM, KHARTOUM, 1], [JOHANNESBURG, JOHANNESBURG, 1]]]
Johannesburg =  [YELLOW, 0,0,0,0, 0, [[JOHANNESBURG, JOHANNESBURG, 0], [KHARTOUM, KHARTOUM, 1], [KINSASHA, KINSASHA, 1]]]
Khartoum =      [YELLOW, 0,0,0,0, 0, [[KHARTOUM, KHARTOUM, 0], [LAGOS, LAGOS, 1], [KINSASHA, KINSASHA, 1], [JOHANNESBURG, JOHANNESBURG, 1], [CAIRO, CAIRO, 1]]]
Algiers =       [BLACK,  0,0,0,0, 0, [[ALGIERS, ALGIERS, 0], [MADRID, MADRID, 1], [PARIS, PARIS, 1], [ISTANBUL, ISTANBUL, 1], [CAIRO, CAIRO, 1]]]
Cairo =         [BLACK,  0,0,0,0, 0, [[CAIRO, CAIRO, 0], [ALGIERS, ALGIERS, 1], [KHARTOUM, KHARTOUM, 1], [ISTANBUL, ISTANBUL, 1], [BAGHDAD, BAGHDAD, 1], [RIYADH, RIYADH, 1]]]
Istanbul =      [BLACK,  0,0,0,0, 0, [[ISTANBUL, ISTANBUL, 0], [MILAN, MILAN, 1], [ALGIERS, ALGIERS, 1], [CAIRO, CAIRO, 1], [BAGHDAD, BAGHDAD, 1], [MOSCOW, MOSCOW, 1], [STPETERSBURG, STPETERSBURG, 1]]]
Moscow =        [BLACK,  0,0,0,0, 0, [[MOSCOW, MOSCOW, 0], [STPETERSBURG, STPETERSBURG, 1], [ISTANBUL, ISTANBUL, 1], [TEHRAN, TEHRAN, 1]]]
Baghdad =       [BLACK,  0,0,0,0, 0, [[BAGHDAD, BAGHDAD, 0], [ISTANBUL, ISTANBUL, 1], [CAIRO, CAIRO, 1], [RIYADH, RIYADH, 1], [KARACHI, KARACHI, 1], [TEHRAN, TEHRAN, 1]]]
Riyadh =        [BLACK,  0,0,0,0, 0, [[RIYADH, RIYADH, 0], [CAIRO, CAIRO, 1], [BAGHDAD, BAGHDAD, 1], [KARACHI, KARACHI, 1]]]
Tehran =        [BLACK,  0,0,0,0, 0, [[TEHRAN, TEHRAN, 0], [MOSCOW, MOSCOW, 1], [BAGHDAD, BAGHDAD, 1], [KARACHI, KARACHI, 1], [DELHI, DELHI, 1]]]
Karachi =       [BLACK,  0,0,0,0, 0, [[KARACHI, KARACHI, 0], [BAGHDAD, BAGHDAD, 1], [RIYADH, RIYADH, 1], [MUMBAI, MUMBAI, 1], [DELHI, DELHI, 1], [TEHRAN, TEHRAN, 1]]]
Mumbai =        [BLACK,  0,0,0,0, 0, [[MUMBAI, MUMBAI, 0], [KARACHI, KARACHI, 1], [DELHI, DELHI, 1], [CHENNAI, CHENNAI, 1]]]
Delhi =         [BLACK,  0,0,0,0, 0, [[DELHI, DELHI, 0], [TEHRAN, TEHRAN, 1], [KARACHI, KARACHI, 1], [MUMBAI, MUMBAI, 1], [CHENNAI, CHENNAI, 1], [KOLKATA, KOLKATA, 1]]]
Chennai =       [BLACK,  0,0,0,0, 0, [[CHENNAI, CHENNAI, 0], [MUMBAI, MUMBAI, 1], [DELHI, DELHI, 1], [KOLKATA, KOLKATA, 1], [BANGKOK, BANGKOK, 1], [JAKARTA, JAKARTA, 1]]]
Kolkata =       [BLACK,  0,0,0,0, 0, [[KOLKATA, KOLKATA, 0], [DELHI, DELHI, 1], [CHENNAI, CHENNAI, 1], [BANGKOK, BANGKOK, 1], [HONGKONG, HONGKONG, 1]]]
Bangkok =       [RED,    0,0,0,0, 0, [[BANGKOK, BANGKOK, 0], [KOLKATA, KOLKATA, 1], [CHENNAI, CHENNAI, 1], [JAKARTA, JAKARTA, 1], [HOCHIMINHCITY, HOCHIMINHCITY, 1], [HONGKONG, HONGKONG, 1]]]
Jakarta =       [RED,    0,0,0,0, 0, [[JAKARTA, JAKARTA, 0], [CHENNAI, CHENNAI, 1], [SYDNEY, SYDNEY, 1], [HOCHIMINHCITY, HOCHIMINHCITY, 1], [HONGKONG, HONGKONG, 1], [KOLKATA, KOLKATA, 1]]]
Sydney =        [RED,    0,0,0,0, 0, [[SYDNEY, SYDNEY, 0], [JAKARTA, JAKARTA, 1], [MANILA, MANILA, 1], [LOSANGELES, LOSANGELES, 1]]]
HoChiMinhCity = [RED,    0,0,0,0, 0, [[HOCHIMINHCITY, HOCHIMINHCITY, 0], [BANGKOK, BANGKOK, 1], [JAKARTA, JAKARTA, 1], [MANILA, MANILA, 1], [HONGKONG, HONGKONG, 1]]]
Manila =        [RED,    0,0,0,0, 0, [[MANILA, MANILA, 0], [HOCHIMINHCITY, HOCHIMINHCITY, 1], [SYDNEY, SYDNEY, 1], [SANFRANCISCO, SANFRANCISCO, 1], [TAIPEI, TAIPEI, 1], [HONGKONG, HONGKONG, 1]]]
HongKong =      [RED,    0,0,0,0, 0, [[HONGKONG, HONGKONG, 0], [KOLKATA, KOLKATA, 1], [BANGKOK, BANGKOK, 1], [HOCHIMINHCITY, HOCHIMINHCITY, 1], [MANILA, MANILA, 1], [TAIPEI, TAIPEI, 1], [SHANGHAI, SHANGHAI, 1]]]
Taipei =        [RED,    0,0,0,0, 0, [[TAIPEI, TAIPEI, 0], [HONGKONG, HONGKONG, 1], [MANILA, MANILA, 1], [OSAKA, OSAKA, 1], [SHANGHAI, SHANGHAI, 1]]]
Osaka =         [RED,    0,0,0,0, 0, [[OSAKA, OSAKA, 0], [TOKYO, TOKYO, 1], [TAIPEI, TAIPEI, 1]]]
Tokyo =         [RED,    0,0,0,0, 0, [[TOKYO, TOKYO, 0], [SEOUL, SEOUL, 1], [SHANGHAI, SHANGHAI, 1], [OSAKA, OSAKA, 1], [SANFRANCISCO, SANFRANCISCO, 1]]]
Seoul =         [RED,    0,0,0,0, 0, [[SEOUL, SEOUL, 0], [BEIJING, BEIJING, 1], [SHANGHAI, SHANGHAI, 1], [TOKYO, TOKYO, 1]]]
Shanghai =      [RED,    0,0,0,0, 0, [[SHANGHAI, SHANGHAI, 0], [BEIJING, BEIJING, 1], [SEOUL, SEOUL, 1], [TOKYO, TOKYO, 1], [TAIPEI, TAIPEI, 1], [HONGKONG, HONGKONG, 1]]]
Beijing =       [RED,    0,0,0,0, 0, [[BEIJING, BEIJING, 0], [SEOUL, SEOUL, 1], [SHANGHAI, SHANGHAI, 1]]]
Epidemic = EPIDEMIC

roleCards = [CONTINGENCY, DISPATCHER, MEDIC, OPERATIONS, QUARANTINE, RESEARCHER, SCIENTIST]
gameBoard = [Atlanta, Washington, SanFransisco, Chicago, Montreal, NewYork, London, Madrid, Paris, Essen, Milan, StPetersburg, LosAngeles, MexicoCity, Miami, Bogota, Lima, Santiago, BuenosAires, SaoPaulo, Lagos, Kinsasha, Johannesburg, Khartoum, Algiers, Cairo, Istanbul, Moscow, Baghdad, Riyadh, Tehran, Karachi, Mumbai, Delhi, Chennai, Kolkata, Bangkok, Jakarta, Sydney, HoChiMinhCity, Manila, HongKong, Taipei, Osaka, Tokyo, Seoul, Shanghai, Beijing]
playDeck = [ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI, DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING, GOVGRANT, AIRLIFT, FORECAST, ONEQUIETNIGHT, RESILIENTPOP]
infectDeck = [ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI, DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING]
thingy = [0,0]
cityDistance = thingy[0]
previousStep = thingy[1]

gameOver = 0

researchStations = [ATLANTA, -1, -1, -1, -1, -1]
outbreakMarker = 0
infectionRateMarker = 0
oneQuietNightMarker = 0
cures = [-1, UNCURED, UNCURED, UNCURED, UNCURED]
blocksRemaining = [-1, 24, 24, 24, 24]
colorsRemaining = [-1, 12, 12, 12, 12]

players = []
infectDiscard = []
intensify = []
playerDiscard = []
outbreakList = []



def checkNeighbors(home, destination):
    home = gameBoard[home]
    for i in xrange(len(home[cOffset])):
        if destination == home[cOffset][i][0] and i != 0:
            return 1
    return 0



def createDistances():
    distance = np.zeros(shape = (len(gameBoard),len(gameBoard)))
    previous = np.zeros(shape = (len(gameBoard),len(gameBoard)))
    for home in xrange(len(gameBoard)):
        for destination in xrange(len(gameBoard)):
            if home == destination:
                distance[home,destination] = 0
                previous[home,destination] = destination
            elif checkNeighbors(home, destination) == 1:
                distance[home,destination] = 1
                previous[home,destination] = home
            else:
                distance[home, destination] = 48
                previous[home, destination] = -1
    for intermediary in xrange(len(gameBoard)):
        for home in xrange(len(gameBoard)):
            for destination in xrange(len(gameBoard)):
                if distance[home, intermediary] + distance[intermediary, destination] < distance[home, destination]:
                    distance[home, destination] = distance[home, intermediary] + distance[intermediary, destination]
                    previous[home, destination] = intermediary
    return [distance, previous]

def getPath(home, destination):
    if home == destination or checkNeighbors(home, destination) == 1:
        return destination
    else:
        getPath(home, previousStep[home, destination])

#distance grid:
#J is the source city, I is the intermediary, K is the destination.
#i goes from 1 to 48, j goes from 1 to 48; this is x and y in a grid.
#The i,j coordinates are the shortest known distances (currently) from i to j
#initialize the matrix such that i to i is 0, i to a neighbor (rip these from the current city info) is 1, and i to everything else is 9 (I think that's the max pathing distance from any one node to another)
#if the distance from i to j is less than infinity, then check to see J's path to every other city (k goes from 1 to 48), and if the distance from J to I + I to K is less than the current distance from J to k
#set the dist of J to K to be that sum.
#set prev(j,k)=i.

#SECOND 2d array, this one storing an intermediary; initialize it such that I to I = i, i to j (if they're neighbors) = i, and everything else is undefined and will be defined later.


#to find distance, use one 2d array; to find direction, use two 2d arrays- one to store the distance, one to store the previous location between i and k
#prev(j,k) returns one step on the way from j to k.  if j=k, return k; if k neighbors j, then return k.  If neither, call this function on (i, prev(i,k).  Recursively call until one of the two initial conditions are met.



def shuffle(givenList):
    shuffledList = []
    while (len(givenList)>0):
        shuffledList.append(givenList.pop(np.random.random_integers(0,len(givenList)-1)))
    return shuffledList



def infect(city, *args):
    for i in xrange(len(players)): 
        if (player[i][ROLE] == QUARANTINE):                                    #If any of the players are a Quarantine specialist
            location = player[i][LOCATION]                                     #find the city they are in
            if (gameBoard[location] == city):                                  #If they're in the city being infected...
                return city                                                    #it's quarantined and cannot be infected.
            for j in xrange(len(gameBoard[location][cOffset])):                #Then loop through the city's neighbors
                if (city == gameboard[player[i][LOCATION]][cOffset][j][CITYINDEX] and gameboard[player[i][LOCATION]][cOffset][j][STEPS] == NEIGHBORING): #if the city being infected is one of them...
                    return city                                                #it's quarantined and cannot be infected.
        if (player[i][ROLE] == MEDIC and cures[city[COLOR]] > 0):
            return city
    if len(args) == 1:
        if (cures[args[0]] < ERADICATED):
            city[args[0]] = city[args[0]] + 1                                  #increment disease token of passed-on color by 1.
            if (city[args[0]] > 3):                                            #Disease tokens are capped at 3 per city
                city[args[0]] = 3
                if (outbreakList.count(city) == 0):                            #If the city hasn't outbroken already from this infect card...
                    outbreak(city)                                             #It will now!
            else:
                blocksRemaining[args[0]] = blocksRemaining[city[COLOR]] - 1    #Otherwise, remove one disease token from the pool
                if (blocksRemaining[args[0]] == 0):
                    gameOver()                                                 #if no disease tokens of that color remain, the game ends.
        
    else:
        color = city[COLOR]
        if (cures[color] < ERADICATED):
            city[color] = city[color] + 1                                      #increment disease token of correct color by 1.
            if (city[color] > 3):                                              #Disease tokens are capped at 3 per city
                city[color] = 3
                if (outbreakList.count(city) == 0):                            #If the city hasn't outbroken already from this infect card...
                    outbreak(city)                                             #It will now!
            else:
                blocksRemaining[color] = blocksRemaining[color] - 1            #Otherwise, remove one disease token from the pool
                if (blocksRemaining[color] == -1):
                    gameOver()                                                 #if no disease tokens of that color remain, the game ends.
    return city                                                                #Pass the city back so gameBoard can update.



def createGame(players, difficulty):   
    roleCards = shuffle([CONTINGENCY, DISPATCHER, MEDIC, OPERATIONS, QUARANTINE, RESEARCHER, SCIENTIST])
    gameBoard = [Atlanta, Washington, SanFransisco, Chicago, Montreal, NewYork, London, Madrid, Paris, Essen, Milan, StPetersburg, LosAngeles, MexicoCity, Miami, Bogota, Lima, Santiago, BuenosAires, SaoPaulo, Lagos, Kinsasha, Johannesburg, Khartoum, Algiers, Cairo, Istanbul, Moscow, Baghdad, Riyadh, Tehran, Karachi, Mumbai, Delhi, Chennai, Kolkata, Bangkok, Jakarta, Sydney, HoChiMinhCity, Manila, HongKong, Taipei, Osaka, Tokyo, Seoul, Shanghai, Beijing]
    playDeck = shuffle([ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI, DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING, GOVGRANT, AIRLIFT, FORECAST, ONEQUIETNIGHT, RESILIENTPOP])
    infectDeck = shuffle([ATLANTA, WASHINGTON, SANFRANCISCO, CHICAGO, MONTREAL, NEWYORK, LONDON, MADRID, PARIS, ESSEN, MILAN, STPETERSBURG, LOSANGELES, MEXICOCITY, MIAMI, BOGOTA, LIMA, SANTIAGO, BUENOSAIRES, SAOPAULO, LAGOS, KINSASHA, JOHANNESBURG, KHARTOUM, ALGIERS, CAIRO, ISTANBUL, MOSCOW, BAGHDAD, RIYADH, TEHRAN, KARACHI, MUMBAI, DELHI, CHENNAI, KOLKATA, BANGKOK, JAKARTA, SYDNEY, HOCHIMINHCITY, MANILA, HONGKONG, TAIPEI, OSAKA, TOKYO, SEOUL, SHANGHAI, BEIJING])
    thingy = createDistances()
    cityDistance = thingy[0]
    previousStep = thingy[1]

    gameOver = 0

    researchStations = [ATLANTA, -1, -1, -1, -1, -1]
    outbreakMarker = 0
    infectionRateMarker = 0
    oneQuietNightMarker = 0
    cures = [-1, UNCURED, UNCURED, UNCURED, UNCURED]
    blocksRemaining = [-1, 24, 24, 24, 24]
    colorsRemaining = [-1, 12, 12, 12, 12]

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

    if (players == 2):
        #player = [Role, Location, stored card, actions remaining, cards in hand]
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2]
        for i in xrange(4):
            player1[pOffset].append(playDeck.pop(0))
            player2[pOffset].append(playDeck.pop(0))
    elif (players == 3):
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player3 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2, player3]
        for i in xrange(3):
            player1[pOffset].append(playDeck.pop(0))
            player2[pOffset].append(playDeck.pop(0))
            player3[pOffset].append(playDeck.pop(0))
    elif (players == 4):
        player1 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player2 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player3 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        player4 = [roleCards.pop(0), ATLANTA, 0, 4, []]
        players = [player1, player2, player3, player4]
        for i in xrange(2):
            player1[pOffset].append(playDeck.pop(0))
            player2[pOffset].append(playDeck.pop(0))
            player3[pOffset].append(playDeck.pop(0))
            player4[pOffset].append(playDeck.pop(0))
    
    if (difficulty == 4):
        playDeckCut1 = (playDeck[:12]).insert(0,Epidemic)
        playDeckCut1 = shuffle(playDeckCut1)
        playDeckCut2 = (playDeck[13:23]).insert(0,Epidemic)
        playDeckCut2 = shuffle(playDeckCut2)
        playDeckCut3 = (playDeck[24:34]).insert(0,Epidemic)
        playDeckCut3 = shuffle(playDeckCut3)
        playDeckCut4 = (playDeck[35:45]).insert(0,Epidemic)
        playDeckCut4 = shuffle(playDeckCut4)
        playDeck = playDeckCut1 + playDeckCut2 + playDeckCut3 + playDeckCut4
    elif (difficulty == 5):
        playDeckCut1 = (playDeck[:9]).insert(0,Epidemic)
        playDeckCut1 = shuffle(playDeckCut1)
        playDeckCut2 = (playDeck[10:18]).insert(0,Epidemic)
        playDeckCut2 = shuffle(playDeckCut2)
        playDeckCut3 = (playDeck[19:27]).insert(0,Epidemic)
        playDeckCut3 = shuffle(playDeckCut3)
        playDeckCut4 = (playDeck[28:36]).insert(0,Epidemic)
        playDeckCut4 = shuffle(playDeckCut4)
        playDeckCut5 = (playDeck[37:45]).insert(0,Epidemic)
        playDeckCut5 = shuffle(playDeckCut5)
        playDeck = playDeckCut1 + playDeckCut2 + playDeckCut3 + playDeckCut4 + playDeckCut5
    elif (difficulty == 6):
        playDeckCut1 = (playDeck[:8]).insert(0,Epidemic)
        playDeckCut1 = shuffle(playDeckCut1)
        playDeckCut2 = (playDeck[9:15]).insert(0,Epidemic)
        playDeckCut2 = shuffle(playDeckCut2)
        playDeckCut3 = (playDeck[16:23]).insert(0,Epidemic)
        playDeckCut3 = shuffle(playDeckCut3)
        playDeckCut4 = (playDeck[24:30]).insert(0,Epidemic)
        playDeckCut4 = shuffle(playDeckCut4)
        playDeckCut5 = (playDeck[31:38]).insert(0,Epidemic)
        playDeckCut5 = shuffle(playDeckCut5)
        playDeckCut6 = (playDeck[39:45]).insert(0,Epidemic)
        playDeckCut6 = shuffle(playDeckCut6)
        playDeck = playDeckCut1 + playDeckCut2 + playDeckCut3 + playDeckCut4 + playDeckCut5 + playDeckCut6
        
    epidemicLikelihood = len(playDeck) / difficulty  #Odds that an epidemic will be drawn next turn; starts at full, goes down by 1 for each turn until an epidemic is drawn
    turn = len(playDeck)/2 #There are a maximum of 22 turns in any one game of Pandemic.
    print turn



def infectionStage(infectionRate):
    outbreakList = []
    index = infectDeck.pop(0)
    gameBoard[index] = infect(gameBoard[index])
    infectDiscard.append(index)
    outbreakList = []
    if infectionRate < 3:
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
    elif infectionRate > 2 and infectionRate < 5:
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
        outbreakList = []
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
    else:
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
        outbreakList = []
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)
        outbreakList = []
        index = infectDeck.pop(0)
        gameBoard[index] = infect(gameBoard[index])
        infectDiscard.append(index)



def outbreak(city):
    outbreakList.append(city)
    outbreakMarker += 1
    if outbreakMarker == 8:
        gameOver()
    else:
        for i in xrange(city[cOffset:]):
            if(city[cOffset][i][STEPS] == NEIGHBORING):
                gameBoard[city[cOffset][i][CITYINDEX]] = infect(city[cOffset][i][CITYINDEX], city[COLOR])



def epidemic():
    infectionRateMarker = infectionRateMarker + 1
    index = infectDeck.pop()
    epidemicCard = gameBoard[index]
    gameBoard[index] = infect(epidemicCard)
    gameBoard[index] = infect(epidemicCard)
    gameBoard[index] = infect(epidemicCard)
    infectDiscard.append(index)
    intensify = []
    while (len(infectDiscard)>0):                                                  
        card = infectDiscard.pop(np.random.random_integers(0,len(infectDiscard)-1))              #grabs a random card out of the infection discard pile,
        intensify.append(card)                                                                   #notes that it's been put back ontop so the AI players can be aware of it,
        infectDeck.insert(0,index)                                                               #and places it ontop of the infect deck, effectively shuffling it.
    intensify = shuffle(intensify)                                                               #Shuffle the intensify stack- otherwise the AI will know the order of the cards on the infect deck!



def treat(player, color):
    if (player[ROLE] == MEDIC or cures[color] == CURED) and (player[ROLE] != MEDIC or cures[color] != CURED) and player[ACTIONS] > 0:
        player[ACTIONS] = player[ACTIONS] - 1
        for i in xrange(gameBoard[player[LOCATION]][color]):
            gameBoard[player[LOCATION]][color] = gameBoard[player[LOCATION]][color] - 1
            blocksRemaining[color] = blocksRemaining[color] + 1
    else:
        gameBoard[player[LOCATION]][color] = gameBoard[player[LOCATION]][color] - 1
        blocksRemaining[color] = blocksRemaining[color] + 1
        player[ACTIONS] = player[ACTIONS] - 1



def movePlayer(player, destinationIndex, *args):
    if len(args) == 0:
        while player[ACTIONS] > 0:
            moveAction(player, getPath(player[LOCATION], destinationIndex))
    if len(args) == 1:
        steps = args[0]
        for i in xrange(steps):
            if player[ACTIONS] > 0:
                moveAction(player, getPath(player[LOCATION], destinationIndex))
    else:
        steps = args[0]
        dispatcher = args[1]
        for i in xrange(steps):
            if dispatcher[ACTIONS] > 0:
                moveAction(player, getPath(player[LOCATION], destinationIndex), dispatcher)



def moveAction(player, destinationIndex, *args):
    if len(args) == 0:
        if player[ACTIONS] > 0:
            location = gameBoard[player[LOCATION]]
            for i in xrange(len(location[cOffset])):
                if (location[cOffset][i][CITYINDEX] == destinationIndex and location[cOffset][i][STEPS] == NEIGHBORING):
                    player[LOCATION] = destinationIndex
                    player[ACTIONS] = player[ACTIONS] - 1
    else:            
        dispatcher = args[0]
        if dispatcher[ACTIONS] > 0:
            location = gameBoard[player[LOCATION]]
            for i in xrange(len(location[cOffset])):
                if (location[cOffset][i][CITYINDEX] == destinationIndex and location[cOffset][i][STEPS] == NEIGHBORING):
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1



def directFlight(player, destinationIndex, *args):
    if len(args) == 0:
        if player[ACTIONS] > 0:
            for i in xrange(len(player[pOffset])):
                if destinationIndex == player[pOffset][i]:
                    colorsRemaining[gameBoard[player[pOffset][i]][COLOR]] = colorsRemaining[gameBoard[player[pOffset][i]][COLOR]] -1
                    playerDiscard.append(player[pOffset].pop(i))
                    player[LOCATION] = destinationIndex
                    player[ACTIONS] = player[ACTIONS] - 1
    else:
        dispatcher = args[0]
        if dispatcher[ACTIONS] > 0:
            for i in xrange(len(player[pOffset])):
                if destinationIndex == dispatcher[pOffset][i]:
                    colorsRemaining[gameBoard[dispatcher[pOffset][i]][COLOR]] = colorsRemaining[gameBoard[dispatcher[pOffset][i]][COLOR]] -1
                    playerDiscard.append(dispatcher[pOffset].pop(i))
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1



def charterFlight(player, destinationIndex, *args):
    if len(args) == 0:
        if player[ACTIONS] > 0:
            for i in xrange(len(player[pOffset])):
                if player[LOCATION] == player[pOffset][i]:
                    colorsRemaining[gameBoard[player[pOffset][i]][COLOR]] = colorsRemaining[gameBoard[player[pOffset][i]][COLOR]] -1
                    playerDiscard.append(player[pOffset].pop(i))
                    player[LOCATION] = destinationIndex
                    player[ACTIONS] = player[ACTIONS] - 1
    else:
        dispatcher = args[0]
        if dispatcher[ACTIONS] > 0:
            for i in xrange(len(dispatcher[pOffset])):
                if player[LOCATION] == dispatcher[pOffset][i]:
                    colorsRemaining[gameBoard[dispatcher[pOffset][i]][COLOR]] = colorsRemaining[gameBoard[dispatcher[pOffset][i]][COLOR]] -1
                    playerDiscard.append(dispatcher[pOffset].pop(i))
                    player[LOCATION] = destinationIndex
                    dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1
                    break;



def shuttleFlight(player, destinationIndex, *args):
    if len(args) == 0:
        if gameBoard[player[LOCATION]][RESEARCH] == 1 and gameBoard[destinationIndex][RESEARCH] == 1 and player[ACTIONS] > 0:
            player[LOCATION] = destinationIndex
            player[ACTIONS] = player[ACTIONS] - 1
    else:
        dispatcher = args[0]
        if gameBoard[player[LOCATION]][RESEARCH] == 1 and gameBoard[destinationIndex][RESEARCH] == 1 and dispatcher[ACTIONS] > 0:
            player[LOCATION] = destinationIndex
            dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1



def dispatchFlight(dispatcher, player, destinationIndex):
    if dispatcher[ACTIONS] > 0:
        for i in xrange(len(players)):
            if destinationIndex == players[i][LOCATION]:
                dispatcher[ACTIONS] = dispatcher[ACTIONS] - 1
                player[LOCATION] = players[i][LOCATION]          



def contingency(player, eventCard):
    if player[ROLE] == CONTINGENCY and player[STORED] == 0 and playerDiscard.count(eventCard) > 0 and player[ACTIONS] > 0:
        player[STORED] = playerDiscard.pop(playerDiscard.index(eventCard))
        player[ACTIONS] = player[ACTIONS] - 1



def operationsFlight(player, destinationIndex, discardIndex):
    if player[ACTIONS] > 0 and player[STORED] == 0 and player[ROLE] == OPERATIONS:
        colorsRemaining[gameBoard[player[pOffset][discardIndex]][COLOR]] = colorsRemaining[gameBoard[player[pOffset][discardIndex]][COLOR]] -1
        playerDiscard.append(player[pOffset].pop(discardIndex))
        player[LOCATION] = destinationIndex
        player[ACTIONS] = player[ACTIONS] - 1
        player[STORED] = 1



def buildResearch(player, *args):
    if (gameBoard[player[LOCATION]][RESEARCH] == 1):
        return
    elif (len(args) > 0):
        gameBoard[args[0]][RESEARCH] = 0
        researchStations[researchStations.index(args[0])] = 0
    if (player[ROLE] == OPERATIONS and player[ACTIONS] > 0):
        gameBoard[player[LOCATION]][RESEARCH] = 1
        researchStations[researchStations.index(-1)] = player[LOCATION]
        player[ACTIONS] = player[ACTIONS] - 1
        discard(player)
    elif (player[ACTIONS] > 0):
        for i in xrange(len(player[pOffset])):
            if player[LOCATION] == player[pOffset][i]:
                gameBoard[player[LOCATION]][RESEARCH] = 1
                colorsRemaining[gameBoard[player[LOCATION]][COLOR]] = colorsRemaining[gameBoard[player[LOCATION]][COLOR]] -1
                playerDiscard.append(player[pOffset].pop(i))
                researchStations[researchStations.index(-1)] = player[LOCATION]
                player[ACTIONS] = player[ACTIONS] - 1



def giveKnowledge(giver, receiver, cardIndex):
    if (giver[LOCATION] == receiver[LOCATION] and giver[ROLE] == RESEARCHER and giver[ACTIONS] > 0):
        receiver[pOffset].append(giver[pOffset].pop(cardIndex))
        giver[ACTIONS] = giver[ACTIONS] - 1
        handLimit(receiver)
    elif giver[LOCATION] == receiver[LOCATION] and giver[ACTIONS] > 0:
        if giver[pOffset][cardIndex] == giver[LOCATION]:
            receiver[pOffset].append(giver[pOffset].pop(cardIndex))
            giver[ACTIONS] = giver[ACTIONS] - 1
            handLimit(receiver)



def takeKnowledge(giver, receiver, cardIndex):
    if (giver[LOCATION] == receiver[LOCATION] and giver[ROLE] == RESEARCHER and receiver[ACTIONS] > 0):
        receiver[pOffset].append(giver[pOffset].pop(cardIndex))
        receiver[ACTIONS] = receiver[ACTIONS] - 1
        handLimit(receiver)
    elif giver[LOCATION] == receiver[LOCATION] and receiver[ACTIONS] > 0:
        if giver[pOffset][cardIndex] == giver[LOCATION]:
            receiver[pOffset].append(giver[pOffset].pop(cardIndex))
            receiver[ACTIONS] = receiver[ACTIONS] - 1
            handLimit(receiver)



def cure(player, *args):
    if player[ROLE] == SCIENTIST and player[ACTIONS] > 0 and gameBoard[player[LOCATION]][RESEARCH] == 1:
        cities = [gameBoard[args[1]], gameBoard[args[2]], gameBoard[args[3]], gameBoard[args[4]]]
        for i in xrange(len(cities)-2):
            if cities[i][COLOR] != cities[i+1][COLOR]:
                return
        cures[cities[0][COLOR]] = CURED
        player[ACTIONS] = player[ACTIONS] - 1
    if player[ACTIONS] > 0 and gameBoard[player[LOCATION]][RESEARCH] == 1:
        cities = [gameBoard[args[1]], gameBoard[args[2]], gameBoard[args[3]], gameBoard[args[4]], gameBoard[args[5]]]
        for i in xrange(len(cities)-2):
            if cities[i][COLOR] != cities[i+1][COLOR]:
                return
        cures[cities[0][COLOR]] = CURED
        player[ACTIONS] = player[ACTIONS] - 1



def resilientPopulation(player, card):
    infectDiscard.pop(card)
    if player[ROLE] == CONTINGENCY and player[STORED] == RESILIENTPOP:
        player[STORED] = 0
    else:
        player[pOffset].pop(player[pOffset].index(RESILIENTPOP))



def airlift(player, target, destination):
    target[LOCATION] = destination
    if player[ROLE] == CONTINGENCY and player[STORED] == AIRLIFT:
        player[STORED] = 0
    else:
        player[pOffset].pop(player[pOffset].index(AIRLIFT))



def govGrant(player, city):
    gameBoard[city][RESEARCH] = 1
    if researchStations.count(-1) > 0:
        researchStations[researchStations.index(-1)] = 1
    if player[ROLE] == CONTINGENCY and player[STORED] == GOVGRANT:
        player[STORED] = 0
    else:
        player[pOffset].pop(player[pOffset].index(GOVGRANT))



def oneQuietNight(player):
    oneQuietNightMarker = 1
    if player[ROLE] == CONTINGENCY and player[STORED] == ONEQUIETNIGHT:
        player[STORED] = 0
    else:
        player[pOffset].pop(player[pOffset].index(ONEQUIETNIGHT))



def forecast(player):
    #I have no idea how to code this one... it ties into the AI and I've no idea how to do that yet, either...
    #Draw the top six cards of the Infection Deck, and put them back in any order.
    topSix = [infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0), infectDeck.pop(0)]
    for i in xrange (len(topSix)):
        if gameBoard[topSix[i]][BLUE] == 3 or gameBoard[topSix[i]][BLACK] == 3 or gameBoard[topSix[i]][RED] == 3 or gameBoard[topSix[i]][YELLOW] == 3:
            infectDeck.insert(0, topSix.pop(i))
    for i in xrange (len(topSix)):
        if gameBoard[topSix[i]][BLUE] == 2 or gameBoard[topSix[i]][BLACK] == 2 or gameBoard[topSix[i]][RED] == 2 or gameBoard[topSix[i]][YELLOW] == 2:
            infectDeck.insert(0, topSix.pop(i))
    for i in xrange (len(topSix)):
        infectDeck.insert(0, topSix.pop(i))
    #This puts the cities back ontop in reverse order of the number of cubes they have: heavily-infected cities are drawn last, lightly infected ones are drawn first.
    if player[ROLE] == CONTINGENCY and player[STORED] == FORECAST:
        player[STORED] = 0
    else:
        player[pOffset].pop(player[pOffset].index(FORECAST))



def discard(player):    #The AI has to choose which card to discard and I have no idea how to code that yet.  Event cards, too...  For now, randomness.
    chosenCard = np.random.random_int(0, len(player[pOffset])-1)
    #if (player[pOffset][chosenCard] == GOVGRANT or player[pOffset][chosenCard] == ONEQUIETNIGHT or player[pOffset][chosenCard] == AIRLIFT or player[pOffset][chosenCard] == FORECAST or player[pOffset][chosenCard] == RESILIENTPOP):
        #Play the event card instead of discarding it.
    #else:
    playerDiscard.append(player[pOffset].pop(chosenCard))



def updateGame(player):
    if cures[BLUE] > 0 and cures[YELLOW] > 0 and cures[BLACK] > 0 and cures[RED] > 0:         #Check to see if you win!
        gameOver = 1
    if player[ROLE] == MEDIC:                                                                 #If the player's a Medic...
        for color in xrange(len(cures)):                                                      
            if cures[color+1] == CURED:                                                       #And there are cured disease cubes on the city he's in, treat them for free.
                cubes = gameBoard[player[LOCATION]][color+1]
                gameBoard[player[LOCATION]][color+1] = 0
                blocksRemaining[color+1] = blocksRemaining[color+1] + cubes
    for i in xrange(len(blocksRemaining)):                                                    #Check for eradication!
        if blocksRemaining[i] == 24 and cures[i] > 0:
            cures[i] = ERADICATED
    while len(player[pOffset]) > 7:                                                           #Check to see if the player needs to discard!
        discard(player)



def playerTurn(player):
    riskAssessment = examineBoard()
    while player[ACTIONS] > 0 and gameOver == 0:              #do 4 actions, or 5 with Generalists who aren't in this version of Pandemic.
        #insert code for choosing an action here!
        updateGame(player)                                    #Refresh the board, and check victory conditions, medic's free distribution of cures, eradication, and hand limit after each action.
    if player[ROLE] == OPERATIONS:
        player[STORED] = 0
    card = playDeck.pop(0)                                    #draw a card
    if card == EPIDEMIC:                                      #if it's an Epidemic...
        epidemic()                                            #Epidemic time!
    else:
        player[pOffset].append(card)                          #if not, put the card in the player's hand
    card = playDeck.pop(0)                                    #draw another card
    if card == EPIDEMIC:                                      #if it's an Epidemic...
        epidemic()                                            #Epidemic time!
    else:
        player[pOffset].append(card)                          #if not, put the card in the player's hand    
    updateGame(player)                                        #check hand limit
    if oneQuietNightMarker == 0:
        infectionStage(infectionRateMarker)                   #call the InfectionStage method...
    else:                                                     #unless One Quiet Night was played
        oneQuietNightMarker = 0                               #if it was, clear the event's effects.
    updateGame(player)
    epidemicLikelihood = epidemicLikelihood - 1



def gameOver():
    gameOver = 1 



#weights:
#Cubes remaining can be covered by examining blocksRemaining and comparing to the initial count of 24.  AI should look at board and determine how many cubes of each color could be placed based on outbreaks and similar
#AI needs to be aware of the cards that /were/ in the infection discard pile before an epidemic, but are now ontop of the infection deck after one.  Modifying Epidemic to include this.
def examineBoard():
    riskAssessment = []
    for i in xrange(len(gameBoard)):
        riskAssessment.append(0)
        city = gameBoard[i]
        for color in xrange(4):
            if (city[color] <0):
                riskAssessment[i] = riskAssessment[i] + city[color]
                if city[color] == 3:
                    city[color]
                    riskAssessment[i] += 1
                    for neighbors in xrange(len(city[cOffset])-1):
                        neighbor = gameBoard[city[cOffset]][neighbors][0]
                        if neighbors != 0:
                            riskAssessment[i] += 1
                            for color2 in xrange(4):
                                if (neighbor[color2] == 3):
                                    riskAssessment[i] += 1
                    if intensify.count(i) == 0:
                        riskAssessment[i] += 1
    print riskAssessment
    return riskAssessment
                        



createGame(2,4)
examineBoard()
#I do not understand these errors.




