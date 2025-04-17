import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

checkpoints = ['00:00:00', '00:27:00', '01:04:00', '1:07:00', '01:24:00', '1:39:00', '1:51:30', '02:17:00']
triangle_stability = {} # False = unstable, True = stable
# deaths = set()

curr_valences = {}
valences_filepath = os.path.join('data', 'valences.csv')
df = pd.read_csv(valences_filepath)

def add_nodes(G):
  characters_filepath = os.path.join('data', 'characters.csv')
  characters_df = pd.read_csv(characters_filepath)
  for col, row in characters_df.iterrows():
    G.add_node(row['Character'])
    # global deaths
    # if row['Character'] not in deaths:
    #   G.add_node(row['Character'])
    # else:
    #   for triangle_key in list(triangle_stability.keys()):
    #       if row['Character'] in triangle_key:
    #           del triangle_stability[triangle_key]


def check_stability(G, checkpoint_end_time, stable_first):
  # FORM EDGES
  temp_valences = {}
  for col, row in df.iterrows():
    acting_node = row['Acting Character']  
    receiving_node = row['Receiving Character']  
    row_end_time = datetime.strptime(row['Time End'], '%H:%M:%S').time()
    if (row_end_time <= checkpoint_end_time):
      if (acting_node != receiving_node):
        sorted_characters = [acting_node, receiving_node]
        sorted_characters.sort()
        dict_key = tuple(sorted_characters)
        temp_valences[dict_key] = row['Valence'] + temp_valences.get(dict_key, 0)
        G.add_edge(acting_node, receiving_node, weight=temp_valences[dict_key])

        # if '[DEATH]' in row['Action / Dialogue'] and receiving_node != 'Rue':
        #   global deaths
        #   deaths.add(receiving_node)

  # TRIANGLE STABILITY
  triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
  for triangle in triangles:
    [character_a, character_b, character_c] = triangle
    
    character_pairs = [
        sorted([character_a, character_b]),
        sorted([character_b, character_c]),
        sorted([character_a, character_c])
    ]

    stability_check = 1
    for pair in character_pairs:
      stability_check = stability_check * temp_valences[tuple(pair)]

    # A triangle is stable if stability_check is positive -> if the weights are pos * pos * pos = pos or pos * neg * neg = pos
    # A triangle is stable if stability_check is negative -> if the weights are neg * neg * neg = neg or pos * pos * neg = neg
    triangle.sort()
    stability_key = tuple(triangle)
    if stable_first:
      stable_to_unstable(stability_key, stability_check)
    else:
      unstable_to_stable(stability_key, stability_check)
  print(triangle_stability)

def stable_to_unstable(stability_key, stability_check):
  if stability_check < 0:
    # only update stability if we've already logged the triangle as stable
    if stability_key in triangle_stability:
      triangle_stability[stability_key] = False 
  else:
    triangle_stability[stability_key] = True

def unstable_to_stable(stability_key, stability_check):
  if stability_check < 0:
    triangle_stability[stability_key] = False 
  else:
    # only update stability if we've already logged the triangle as unstable
    if stability_key in triangle_stability:
      triangle_stability[stability_key] = True

def main():
  for i in range(len(checkpoints) - 1):
    G = nx.Graph()
    add_nodes(G)
    checkpoint_start_time = datetime.strptime(checkpoints[i], '%H:%M:%S').time()
    checkpoint_end_time = datetime.strptime(checkpoints[i + 1], '%H:%M:%S').time()
    print(checkpoint_start_time)
    stable_first = False # change to False if you want to see the triangle that resolve from unstable to stable
    check_stability(G, checkpoint_end_time, stable_first)

main()
