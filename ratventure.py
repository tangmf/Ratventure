#Tang Ming Feng
#P12
#S10185023
#15/8/2020

#My program: Ratventure game with additional features, which include a shop system, potions and upgrades, lucky drops, and an inventory system.
#The player must kill the rat king to win the game, if the players health reaches 0HP, they will die, and has to start over again
#unless the player has saved their game. The map is randomly generated, with the exception of the starting town and the rat king.
#The program has input validation, and will display "Invalid input!" and "Try again!" when it recieves an invalid input.
#In my version of the game, farming is a thing that is important, in order to get money and upgrade items and buy potions.
#To prevent farming without risk once the player gets the Orb of Power or having a lot of upgrades, when player/enemy damage is 0 or less, it will be set to 1 instead.
#This way, farming still has a tiny amount of risk, and enemies cannot be invincible(except for rat king when you do not have orb of power).
#If not, the game will be way too easy.

from random import randint


# +------------------------+#
# | Text for various menus |#
# +------------------------+#

main_text = ["New Game",\
             "Resume Game",\
             "View Leaderboard",\
             "Exit Game"]

town_text = ["View Character",\
             "View Map",\
             "Move",\
             "Rest",\
             "Shop",\
             "Save Game",\
             "Exit Game"]

open_text = ["View Character",\
             "View Map",\
             "Move",\
             "Sense Orb",\
             "Exit Game"]

fight_text = ["Attack",\
              "Run",\
              "Inventory"]


#Empty to allow space for random town generation
world_map = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]


#Global variables
current_row = 0
current_column = 0
current_day = 1
game_started = False
game_over = False


#Added variables
orb = False #Will be True if orb is found
gapple = False #True if player uses a Golden Apple


#Spawns initial town.
town_list = [] #list of the coords of all towns that are randomly generated
world_map[0][0] = "T"
town_list.append([0, 0])

    



#Character assets
player = {"Name": "The Hero", "Min damage": 2, "Max damage": 4, "Defence":1, "HP":20, "Inventory":[], "fought": False}
rat = {"Name": "Rat", "Min damage": 1, "Max damage": 3, "Defence":1, "HP": 10}
rat_king = {"Name": "Rat King", "Min damage": 4, "Max damage": 10, "Defence": 5, "HP": 50}
#rat_king buffed as player can upgrade items and heal


orb_row = 4
orb_column = 4
treasures = {"orb":[orb_row,orb_column]}

#Additional assets
coins = 0 #coins can be used in shops found in towns

kills = 0 #for stats. Kiling a rat or rat king awards 1 kill

leaderboards = [] #highscores here.

#Addition: Shop (found in towns)
shop_items = [["Healing_Potion", "10"],         #Heals player for 5HP. Will not work if player is full HP 
              ["Weapon_Upgrade", "20"],         #Incrases max and min damage by 1 each
              ["Armour_Upgrade", "30"],         #Increases defence by 1
              ["Mysterious_Potion", "20"],      #reduce atk by 1 or reduce defence by 1 or increase atk by 2 or increase defence by 2 or does nothing
              ["Immortality_Potion", "50"],     #restores hp to 20 (Full HP)
              ["Golden_Apple", "50"]]           #Plus 5 coins after every battle and increase defence by 1 (plus 5 coins can only be activated once. Eating the apple again will only give 1 defence)
# Items need to be used via the inventory system to take effect.



#Functions
    

#1. Display main menu
def display_menu(main_text):

    
    print()
    print("Welcome to Ratventure!")
    print("----------------------")
    for main_text_items in main_text:
        main_text_number = main_text.index(main_text_items) + 1
        print('[{}] {}'.format(main_text_number, main_text_items))

    try:
        main_text_selection = int(input('Enter Choice: '))
        assert main_text_selection in range(1, 5)

    except:
        print()
        print("Invalid input!")
        print("Try again!")
        display_menu(main_text)

    else:
        #1.1 New Game
        if main_text_selection == 1:
            game_started = True
            random_gen()
            while game_started:
                start()

        #1.2 Resume Game
        elif main_text_selection == 2:
            resume_game()
            game_started = True
            while game_started:
                start()

        #3. View leaderboard
        elif main_text_selection == 3:
            check_leaderboard()
            display_menu(main_text)

        #1.3 Exit Game
        elif main_text_selection == 4:
            exit_game()

#Randomizes towns when player selects new game.
def random_gen():
    global world_map
    global town_list
    global orb_row
    global orb_column
    
    while len(town_list) < 5:
        row = randint(0,7)
        column = randint(0,7)
        add = True
        for town in town_list:
            if abs(row - town[0]) < 3 and abs(column - town[1]) < 3 or world_map[row][column] == 'K':
                add = False
        if add == True:  
            world_map[row][column] = "T"
            town_list.append([row, column])

    #Random orb generation
    orb_row = randint(4,7)
    orb_column = randint(4,7)
    while world_map[orb_row][orb_column] == "T" or "K": #To ensure orbs spawn at open tiles.
        orb_row = randint(4,6)
        orb_column = randint(4,6)
        if world_map[orb_row][orb_column] == " ":
            break


    
# Check tile player is on and acts accordingly (tile can be town,open,ratking or orb.)
def start():

    global kills
    global player
    global orb


    
    #Check what tile the player is on
    state = world_map[current_row][current_column]
            
    #Player is in a town
    if state == 'T':
        in_town(town_text)

    #5. Rat King
    #Player is on Rat King Tile
    elif state == 'K':
                
        combat_round(rat_king)

        try:
            choice = int(input("Enter your choice: "))
            assert choice in range(1, 4)
            
        except:
            print("Invalid input!")
            print("Try again!")

        else:
            if choice == 1:
                if orb == True:
                    attack(rat_king)
                else:

                    print()
                    #Rat king keeps dealing damage
                    print("You do not have the Orb of Power! - the Rat King is immune!")
                    print("You deal 0 damage to the Rat King")
                    rat_damage = randint(rat_king["Min damage"], rat_king["Max damage"]) - player["Defence"]
                    print("Ouch! The {} hit you for {} damage!".format(rat_king["Name"], rat_damage))
                    player["HP"] -= rat_damage
                    if player["HP"] <= 0:
                        player["HP"] = 0
                                

                    #Combat for the round is over
                    print("You have {} HP left.".format(player["HP"]))
                    #Game over if no more HP
                    if player["HP"] == 0:
                        print("Game over!")
                        exit_game()
                                    
            elif choice == 2:
                    
                run()

            elif choice == 3:
                display_inventory(player)
                print()
                print("The Rat King attacked whilst you were looking through your inventory!")
                skip_turn(rat_king)
                
            #5.1 Victory!
            if rat_king["HP"] <= 0:

                #Rat king defeated
                print()
                print("Rat King Defeated!")
                kills += 1
                print("You win!")
                #Game successfully completed!

                display_stats(current_day, kills)
                edit_leaderboard(current_day)
                exit_game()
                

    #Player is on Orb Tile
    elif treasures["orb"][0] == current_row and treasures["orb"][1] == current_column:
        print()
        print("You found the Orb of Power!")
        print("Your attack increases by 5!")
        print("Your defence increases by 5!")

        #Increase stats
        player["Min damage"] += 5
        player["Max damage"] += 5
        player["Defence"] += 5

                
        orb = True
        treasures["orb"][0] = 10
        treasures["orb"][1] = 10

        #Player does not need to fight in this tile
        player["fought"] = True

    #Player is on empty tile (open)
    else:

                
        #Fight the rat
        if player["fought"] == False:
            combat_round(rat)
            try:
                choice = int(input("Enter your choice: "))
                assert choice in range(1,4)
            except:
                print()
                print("Invalid input!")
                print("Try again!")
            else:

                if choice == 1:
                        attack(rat)
                            
                elif choice == 2:
                        run()

                elif choice == 3:
                    display_inventory(player)
                    print()
                    print("The rat attacked whilst you were looking through your inventory!")
                    skip_turn(rat)
                            


                #After defeating the rat
                if rat["HP"] <= 0:
                    print()
                    print("The rat is dead! You are victorious!")
                    kills += 1
                    player["fought"] = True
                    battle_drop()
                    rat["HP"] = 10
                    in_open(open_text)
                        
        #Rat has already been fought
        else:
            in_open(open_text)



                    
    
#2. Display Town Menu
def in_town(town_text):

    
    print()
    print('Day {}: You are in a town.'.format(current_day))
    for choice in town_text:
        print('{}) {}'.format(town_text.index(choice) + 1, choice))

    try:
        #Input
        choice = int(input("Enter your choice: "))
        assert choice in range (1, 8)
                               
    except:
        print()
        print("Invalid input! Try again!")
    else:
        if choice == 1:
            view_character(player)
                            
        elif choice == 2:
            view_map(world_map)
                            
        elif choice == 3:
            move()
                            
        elif choice == 4:
            rest()

        elif choice == 5:
            shop(shop_items)
                            
        elif choice == 6:
            save_game()
                            
        elif choice == 7:
            exit_game()


#4. Display outdoor menu
def in_open(open_text):

    
    print()
    print('Day {}: You are out in the open.'.format(current_day))
    for choice in open_text:
        print('{}) {}'.format(open_text.index(choice) + 1, choice))

    #Input
    try:
        choice = int(input("Enter your choice: "))
        assert choice in range(1, 6)

    except:
        print()
        print("Invalid input!")
        print("Try again!")
        in_open(open_text)

    else:
        
        if choice == 1:
            view_character(player)
            
        elif choice == 2:
            view_map(world_map)
            
        elif choice == 3:
            move()
            
        elif choice == 4:
            sense_orb()
            
        elif choice == 5:
            exit_game()
        
        
    
#4.1.
#2.1. View Character
# shows basic stats, if orb is found, coins and inventory
def view_character(player):

    #Basic stats
    print()
    print('{}'.format(player['Name']))
    print('{} {}-{}'.format("Damage:", player['Min damage'], player['Max damage']))
    print('{} {}'.format("Defence:", player['Defence']))
    print('{} {}'.format("HP:", player['HP']))


    if orb == True:
        print()
        print("You are holding the Orb of Power.")

    else:
        print("You do not have the Orb of Power yet.")
        print("You need it to be able to fight the Rat King.")


    #coins
    print()
    print("Coins: {}".format(coins))
    
    #Inventory
    print("Inventory: ")
    display_inventory(player)





        

#2.2. View Map
#4.2. View Map
def view_map(world_map):

    
    print()
        
    if world_map[current_row][current_column] == 'T':
        world_map[current_row][current_column]='H/T'
    elif world_map[current_row][current_column] == 'K':
        world_map[current_row][current_column] = 'H/K'
    else:
        world_map[current_row][current_column] = 'H'

    for r in range(8):             #len(world_map)
        print("+---+---+---+---+---+---+---+---+")
        print("|", end = '')
        for c in range(8):         #len(world_map[0])
            print("{:^3s}|".format(world_map[r][c]), end = '')
        print()
    print("+---+---+---+---+---+---+---+---+")


    if world_map[current_row][current_column] == 'H/T':
        world_map[current_row][current_column] = 'T'
    elif world_map[current_row][current_column] == 'H/K':
        world_map[current_row][current_column] = 'K'
    else:
        world_map[current_row][current_column] = ''




    



#2.3. Move
#4.3. Move
def move():
    
    global current_row
    global current_column
    global current_day
    global player

    view_map(world_map)

    #Instructions
    print("W = up; A = left; S = down; D = right")
    print()

    #Input
    
    choice = str(input("Your move: "))
    
    if choice.upper() == 'W':
        if current_row!= 0:
            current_row -= 1
            #Make sure the player will need to fight after moving    
            player["fought"] = False

            #Move takes 1 day
            current_day += 1

        
    elif choice.upper() == 'A':
        if current_column != 0:
            current_column -= 1
            #Make sure the player will need to fight after moving    
            player["fought"] = False

            #Move takes 1 day
            current_day += 1
        
    elif choice.upper() == 'S':
        if current_row != 7:
            current_row += 1
            #Make sure the player will need to fight after moving    
            player["fought"] = False

            #Move takes 1 day
            current_day += 1
        
    elif choice.upper() == 'D':
        if current_column != 7:
            current_column += 1
            #Make sure the player will need to fight after moving    
            player["fought"] = False

            #Move takes 1 day
            current_day += 1
            
    #The reason why I dont put current_day += 1 and fought = false out side of the if statement is
    #because if the input is something else (allows the player to "cancel their choice to move and do something else"
    #it wont still add a day or make the player's fought be true without actually fighting.        

    
        
#2.4. Rest

def rest():
    global player
    global current_day

    #Reset HP to 20 if not max HP
    if player["HP"] < 20:
        print()
        player["HP"] = 20
        current_day += 1
        print("You are fully healed.")
    else:
        print()
        print("You have max HP! You do not need to rest!")




#2.5. Save Game
def save_game():

    print()
    
    current = str(current_row) + '/' + str(current_column)
    file = open("savefile.txt", 'w')
    file.write("Saved Data: ")
    file.write("\n")
    file.write(str(current))
    file.write("\n")
    file.write(str(current_day))
    file.write("\n")
    file.write(str(orb))
    file.write("\n")
    
    for i in player:
        file.write(str(player[i]))
        file.write("\n")

    orb_pos = str(treasures["orb"][0]) + '/' + str(treasures["orb"][1])
    file.write(orb_pos)
    file.write("\n")
    file.write(str(gapple))
    file.write("\n")
    file.write(str(town_list))
    file.write("\n")
    file.write(str(coins))
    print("Game saved.")
    file.close


#Resume Game
def resume_game():

    global current_row
    global current_column
    global player
    global current_day
    global orb
    global treasures
    global gapple
    global world_map
    global town_list
    global coins



    file = open("savefile.txt", "r")
    file_contents = []
    file.readline()
    for line in file:
        line = line.strip("\n")
        row_list = line.split(',')
        file_contents.append(row_list)
    file.close()

    try:
        #Updating Coordinates
        current = file_contents[0][0].split('/')
        current_row = int(current[0])
        current_column = int(current[1])

        #Updating current day
        current_day = int(file_contents[1][0])

        #Updating orb
        if file_contents[2][0] == 'True':
            orb = True
        else:
            orb = False


        #Updating player
        inventory = str(file_contents[8]).replace("'", "").replace("[", "").replace("]", "").replace('"', '').replace(" ", "")
        if "," in inventory:
            inventory = inventory.split(",")
        else:
            if inventory == '':
                inventory = []
            else:
                inventory = [inventory]
        player = {"Name": file_contents[3][0],
                  "Min damage": int(file_contents[4][0]),
                  "Max damage": int(file_contents[5][0]),
                  "Defence": int(file_contents[6][0]),
                  "HP": int(file_contents[7][0]),
                  "Inventory": inventory,
                  "fought": bool(file_contents[9][0])}


        #Updating orb coords
        orb_pos = file_contents[10][0].split('/')
        treasures["orb"][0] = int(orb_pos[0])
        treasures["orb"][1] = int(orb_pos[1])

        #Updating Gapple
        if file_contents[11][0] == 'True':
            gapple = True
        else:
            gapple = False

        #Updating world map
        twn = str(file_contents[12]).replace("'", "").replace(" ", "")
        twn = twn[3:-3]
        twnlist = twn.split("],[")
        

        for row in range(0, 8):
            for column in range(0, 8):
                if world_map[row][column] == "T":
                    world_map[row][column] = " "
        print()
        for town in twnlist:
            world_map[int(town[0])][int(town[2])] = "T"
            town_list.append([int(town[0]), int(town[2])])
        
        coins = int(file_contents[13][0])

        print("Game resumed.")
        
    except Exception:
        print()
        print("Error!")
        print("There is no file saved!")



#1.3. Exit Game
#2.6. Exit Game
#4.4. Exit Game
def exit_game():
    print()
    print("Thank you for playing!")
    
    try:
        choice = int(input("Press 0 to exit: "))
        assert choice == 0
        
    except Exception:
        exit()   # so no matter what, player exits game
        
    else:
        if choice == 0:
            exit()
    

#4.4. Sense Orb
# Senses location of orb and prints direction.
def sense_orb():
    global current_day

    
    if orb == False:
        print()
        row = treasures["orb"][0] #orb row
        column = treasures["orb"][1] #orb column
        if row > current_row and column > current_column:
            direction = "South East"
        elif row > current_row and column < current_column:
            direction = "South West"
        elif row < current_row and column < current_column:
            direction = "North West"
        elif row < current_row and column > current_column: 
            direction = "North East"
        elif row == current_row and column > current_column:
            direction = "East"
        elif row > current_row and column == current_column:
            direction = "South"
        elif row < current_row and column == current_column:
            direction = "North"
        elif row == current_row and column < current_column:
            direction = "West"

        print("You sense that the Orb of Power is to the {}.".format(direction))


        #Sensing orb takes 1 day
        current_day += 1

    #If orb = True
    else:
        print()
        print("You already found the Orb!")
    


#3. Combat Menu pt 1
# Display choices
def display_combat_menu(fight_text):
    #Displaying combat menu
    for choice in fight_text:
        print('{}) {}'.format(fight_text.index(choice) + 1, choice))

#3. Combat Menu pt 2
# Shows stats of rat
def combat_round(rat):

    print()
    print('Day {}: You are out in the open.'.format(current_day))

    
    #Displaying stats of rat
    print('Encounter! - {}'.format(rat["Name"]))
    print('Damage: {}-{}'.format(rat["Min damage"], rat["Max damage"]))
    print('Defence: {}'.format(rat["Defence"]))
    print('HP: {}'.format(rat["HP"]))

    display_combat_menu(fight_text)



#3.1. Attack
#Player deals damage, then rat deals damage.
def attack(rat):
    print()

    #Player deals damage first

    player_damage = randint(player["Min damage"], player["Max damage"]) - rat["Defence"]
    if player_damage <= 0:
        player_damage = 1 #so that the rat cannot be invincible and recieve no damage
        
    print("You deal {} damage to the {}".format(player_damage, rat["Name"]))
    rat["HP"] -= player_damage

    #Rat deals damage next


    rat_damage = randint(rat["Min damage"], rat["Max damage"]) - player["Defence"]
    if rat_damage <= 0: 
        rat_damage = 1 #so that you cannot be invincible and recieve no damage
        
    print("Ouch! The {} hit you for {} damage!".format(rat["Name"], rat_damage))
    player["HP"] -= rat_damage


    #Game over if no more HP
    if player["HP"] <= 0:
        player["HP"] = 0
        print()
        print("You have 0 HP left.")
        print("The Rat King has killed you!")
        print("Game over!")
        exit_game()

    #Combat for the round is over
    print("You have {} HP left.".format(player["HP"]))


#3.2. Run
#Runs from battle(resets enemy HP)
def run():
    print()
    print("You run and hide.")
    in_open(open_text)

    #resets enemy hp
    rat["HP"] = 10
    rat_king["HP"] = 50


# Displays inventory and player can use items.
def display_inventory(player):


    print()

    already_printed = [] # So that it doesnt print the same item again as it is stacked
    no = 1

    item_list = []




    #Addition: Inventory (interactable)
    if len(player["Inventory"]) != 0:
        for item in player["Inventory"]:
            
            item_label = []

            # Stacking items
            if item not in already_printed:
                x = player["Inventory"].count(item)
                already_printed.append(item)
                print("[{}]{} x{}".format(no, item, x))
                item_label.append(no)
                item_label.append(item)
                item_list.append(item_label)
                no += 1


        
        print()
        try:
            choice = int(input("Choose an item to use or enter any other number to go back: "))
        except:
            print()
            print("Invalid input!")
            print("Try again!")

        else:
        
            for label in item_list:
                item = label[1]
                if choice == label[0]:

                    use_item(item)

                
    else:
        print("Your inventory is empty.")
        print("Visit a shop in a town or get lucky drops from killing enemies to get items.")


        


# If user looks at inventory during battle
def skip_turn(rat):
    #Rat attacks after user uses an item
    rat_damage = randint(rat["Min damage"], rat["Max damage"]) - player["Defence"]
    if rat_damage <= 0:
        rat_damage = 1
    print("Ouch! The {} hit you for {} damage!".format(rat["Name"], rat_damage))
    player["HP"] -= rat_damage
    print("You have {} HP left.".format(player["HP"]))

                        
    if player["HP"] <= 0:
        print("Game over!")
        exit_game()


#Addition: Using Items
def use_item(item):
    global player
    global gapple
    
    #If item is Healing Potion
    if item == "Healing_Potion":
        if player["HP"] < 20:
            player["HP"] += 5
            player["Inventory"].pop(player["Inventory"].index(item))
            print("You used {}!".format(item))
            print("The Healing_Potion healed you by 5HP!")
                    
            if player["HP"] > 20:
                player["HP"] = 20
            print("Your HP is now {}".format(player["HP"]))
        else:
            print()
            print("You already have max health!")


    #If item is Mysterious Potion
    elif item == "Mysterious_Potion":

        player["Inventory"].pop(player["Inventory"].index(item))
        print()
        print("You used a Mysterious_Potion!")
        
        spin = randint(1,11)
        if spin in range(1,3):
            player["Defence"] += 2
            print("The Mysterious_Potion granted you +2 Defence!")

        elif spin in range(3,5):
            player["Defence"] -= 1
            if player["Defence"] < 0:
                player["Defence"] = 0
            print("The Mysterious_Potion weakened your Defence by 1!")

        elif spin in range(5,7):
            player["Max damage"] += 2
            print("The Mysterious_Potion granted you +2 Max damage!")

        elif spin in range(7,9):
            if player["Max damage"] - player["Min damage"] > 1: # To ensure max wont be lesser than min
                player["Max damage"] -= 1
                print("The Mysterious_Potion weakened your Max damage by 1!")
            else:
                print("The Mysterious_Potion did nothing!")

        else:
            print("The Mysterious_Potion did nothing!")

    #If item is weapon Upgrade
    elif item == "Weapon_Upgrade":
         player["Inventory"].pop(player["Inventory"].index(item))
         print()
         print("You used a Weapon_Upgrade!")
         player["Max damage"] += 1
         player["Min damage"] += 1
         print("Your damage is increased by 1!")
         print("Your damage is now {}-{}".format(player["Min damage"], player["Max damage"]))
    
    #If item is immortality potion (full hp)
    elif item == "Immortality_Potion":
        if player["HP"] < 20:
            player["Inventory"].pop(player["Inventory"].index(item))
            print()
            print("You used a Immortality_Potion!")
            player["HP"] = 20
            print("You now have full HP.")
        else:
            print("You already have full HP")
    #If item is golden apple (+5 coins every battle and +1 defence)
    elif item == "Golden_Apple":
        if gapple == False:
            player["Inventory"].pop(player["Inventory"].index(item))
            print()
            print("You used a Golden_Apple!")
            gapple = True
            print("You will now recieve an extra 5 coins after every battle")
            player["Defence"] += 1
            print("Also, your defence is increased by 1!")
            print("Eating another Golden_Apple will only reward you with +1 Defence.")
        else:
            print()
            print("Eating another Golden_Apple makes you stronger!")
            player["Defence"] += 1
            print("Your defence is increased by 1!")

    elif item == "Armour_Upgrade":
        player["Inventory"].pop(player["Inventory"].index(item))
        print()
        print("You used an Armour_Upgrade!")
        player["Defence"] += 1
        print("Your defence is increased by 1!")
        print("Your defence is now {}".format(player["Defence"]))
         
    #If item is not valid, nothing will happen and game will continue   
    

    


#Addition: Special battle drops
def battle_drop():
    global coins
    global player
    
    reward = randint(1, 5)
    coins += reward


    #Lucky Drop #1: Healing Potion (1-10)
    random_spin = randint(1, 101)
    if random_spin in range(1, 11):
        
        player["Inventory"].append("Healing_Potion")
        print("Lucky! You got a Healing_Potion!")
        print("During battle, drink the potion to replenish 5 HP!")
        
        
    #Lucky Drop #2: Bag of coins (11-20)
    elif random_spin in range(11, 21):
        print("Lucky! You got a bag of coins!")
        print("You opened the bag of coins and got 20 coins!")
        coins += 20

    #Lucky Drop #3: Mysterious Potion (21-30)
    elif random_spin in range(21,30):
        player["Inventory"].append("Mysterious_Potion")
        print("Lucky! You got a Mysterious_Potion!")
        print("I wonder what it does...")
        
    #Lucky Drop #4: Immortality Potion (100) super rare drop (100)
    elif random_spin == 100:
        player["Inventory"].append("Immortality_Potion")
        print("You were extremely lucky and found an Immortality_Potion!")
        print("During battle, use this item to replinsh full HP!")


    #Coins earned for battling
    print("You have been awarded {} coins for your bravery.".format(reward))
    if gapple == True:
        print("You found 5 more coins because of the Golden_Apple you ate!")
        coins += 5
    print("You now have {} coins.".format(coins))
        

#Addition: Shop menu
def shop(shop_items):
    global coins
    global player

    #Print items for sale
    print()
    print("Welcome to the shop!")
    print()
    print("You have {} coins.".format(coins))
    print()

    print("{:8s} {:20s} {:8s}".format("Item no.", "Item Name", "Price"))
    print()
    for item in shop_items:
        print("{:8s} {:20s} {:8s}".format(str(shop_items.index(item) + 1) + ")", str(item[0]), str(item[1])))
        print()


    #Input
    print()
    print("Press 0 to go back")
    try:
        buying = int(input("What would you like to buy? Enter the item no.: "))
        assert buying in range(0, len(shop_items) + 1)
        
    except Exception:
        print()
        print("Invalid input!")
        print("Try again!")

    else:
        if buying == 0:
            in_town(town_text)
        else:
            for item in shop_items:
                name = item[0]
                price = int(item[1])
                if buying == shop_items.index(item) + 1:
                    print()
                    if coins >= price:
                        coins -= price
                        player["Inventory"].append(name)
                        print("You have bought a {} for {} coins!".format(name, price))
                        print("You now have {} coins left!".format(coins))
                        print("A {} has been added to your inventory!".format(name))
                    else:
                        print("You do not have enough money to purchase that item!")

            print()
            print("You can use the item from your inventory via View Character!")
        
    
    

def display_stats(current_day, kills):
    print()
    print("###################")
    print("  Days Taken: {:<3d}".format(current_day))
    print("  Kills: {}".format(kills))
    print("  Coins left: {}".format(coins))
    print("###################")




# Displays leaderboards (in main menu)
def check_leaderboard():

    global leaderboards
    leaderboards = []
    n = 0
    try:
        file = open("leaderboard.txt", "r")
        file.readline()
        for line in file:
            line = line.strip("\n")
            leaderboards.append(int(line))
            
        file.close

    except Exception:
        print()
        print("Error with the leaderboards file!")
    else:
        print()
        print("Leaderboard:")

        if len(leaderboards) > 0:
                
            for line in leaderboards:
                print("[{}] {} {}".format(n+1, line, "days taken"))
                n += 1
        else:
            print()
            print("No highscores yet!")




#After beating game, this function determines if the score is low enough to be on the leaderboards and adds if it is.
def edit_leaderboard(current_day):

    global leaderboards

    leaderboards.sort()
    if len(leaderboards) == 0:
        leaderboards.append(current_day)
        print("New highscore: {}".format(current_day))

    else:
        if int(current_day) >= int(leaderboards[len(leaderboards)-1]):
            print("You didn't make it to the leaderboards!")
                
        else:
            leaderboards.append(current_day)
            print("New highscore!")
            print("New highscore: {}".format(current_day))


    #Ensure leaderboard only records top 5 scores that take shortest time
    leaderboards.sort()
    if len(leaderboards) > 5:
        leaderboards.pop()

        
    #Updating to leaderboard file
    file = open("leaderboard.txt", "w")
    file.write("Highscores:")
    file.write("\n")

    for highscore in leaderboards:
        file.write(str(highscore))
        file.write("\n")
    file.close

    #display leaderboards (at end of the game)
    print()
    print("Leaderboard:")
    n = 0
    for highscore in leaderboards:
        print("[{}] {} {}".format(n+1, highscore, "days taken"))
        n += 1



display_menu(main_text)

