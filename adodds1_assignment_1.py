def hawkid():
    return(["Adam Dodds", "adodds1"])

import csv

def import_data(filename):
    main_list = []
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            row = [item.strip() for item in row]
            
            pokemon = []
            for item in row:
                try:
                    pokemon.append(float(item))
                except ValueError:
                    pokemon.append(item)
            
            main_list.append(pokemon)
    
    return main_list

filename = "test_input.csv"
participants = import_data(filename)
print(participants)

def attack_multiplier(attacker_type, defender_type):
    attack_multipliers = {
        ("Water", "Fire"): 2.5,
        ("Electric", "Water"): 1.3,
        ("Ground", "Electric"): 2.0,
        ("Fire", "Grass"): 3.0,
        ("Grass", "Water"): 1.5
    }
    return attack_multipliers.get((attacker_type, defender_type), 1.0)

attack_types = ["Water", "Electric", "Ground", "Fire", "Grass"]
defense_types = ["Water", "Electric", "Ground", "Fire", "Grass"]

for attacker_type in attack_types:
    for defender_type in defense_types:
        multiplier = attack_multiplier(attacker_type, defender_type)
        print("Attacker: {}, Defender: {}, Multiplier: {}".format(attacker_type, defender_type, multiplier))

def fight(participant1, participant2, first2attack):
    rounds = 0
    
    variable1 = participant1[2] 
    variable2 = participant2[2] 
    
    while variable1 > 0 and variable2 > 0:
        if first2attack == 1:
            attack_multi = attack_multiplier(participant1[1], participant2[1])
            new_damage = attack_multi * participant1[3]
            variable2 -= new_damage
        else:
            attack_multi = attack_multiplier(participant2[1], participant1[1])
            new_damage = attack_multi * participant2[3]
            variable1 -= new_damage
        
        rounds += 1
        
        first2attack = 1 if first2attack == 2 else 2
        
    winner = 1 if variable1 > 0 else 2
    
    return [winner, rounds]

participant1 = ["Alomomola", "Water", 165, 76]
participant2 = ["Luxio", "Electric", 243, 54]
first2attack = 1

result = fight(participant1, participant2, first2attack)
print("Rounds:", result[1])
print("Winner:", result[0])

def tournament(participants):
    wins = [0] * len(participants)
    
    num_participants = len(participants)
    for i in range(num_participants):
        for j in range(i + 1, num_participants):
            result_home = fight(participants[i], participants[j], 1)
            result_away = fight(participants[i], participants[j], 2)
            
            if result_home[0] == 1:
                wins[i] += 1
            else:
                wins[j] += 1
    
    return wins

participants = [
    ["Baltoy", "Ground", 325, 36],
    ["Flareon", "Fire", 700, 11],
    ["Alomomola", "Water", 165, 76],
    ["Pikachu", "Grass", 367, 32],
    ["Luxio", "Electric", 243, 54]
]

tournament_results = tournament(participants)
print("Tournament Results:", tournament_results)
