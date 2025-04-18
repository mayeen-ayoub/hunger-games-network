import pandas as pd
import networkx as nx
from datetime import datetime
import os

checkpoints = ['00:00:00', '00:27:00', '01:04:00', '1:07:00', '01:24:00', '1:39:00', '1:51:30', '02:17:00']
triangle_stability = {} # False = unstable, True = stable

# read the data from valences.csv 
valences_filepath = os.path.join('data', 'valences.csv')
df = pd.read_csv(valences_filepath)

# add the nodes to the graph
def add_nodes(G):
  characters_filepath = os.path.join('data', 'characters.csv')
  characters_df = pd.read_csv(characters_filepath)
  for col, row in characters_df.iterrows():
    G.add_node(row['Character'])

def add_edges(G, checkpoint_end_time):
    # Add the edges to the graph
  temp_valences = {}
  for col, row in df.iterrows():
    acting_node = row['Acting Character']  
    receiving_node = row['Receiving Character']  
    row_end_time = datetime.strptime(row['Time End'], '%H:%M:%S').time()

    # only add the edge if we have reached that point in time
    if (row_end_time <= checkpoint_end_time):
      if (acting_node != receiving_node): # this ensures no self loops
        # create dictionary key for the valences eg. { ('Katniss', 'Gale', 'Peeta'): -1 }
        sorted_characters = [acting_node, receiving_node]
        sorted_characters.sort()
        dict_key = tuple(sorted_characters)

        # add valences together and add the edge
        temp_valences[dict_key] = row['Valence'] + temp_valences.get(dict_key, 0)
        G.add_edge(acting_node, receiving_node, weight=temp_valences[dict_key])
  return temp_valences

def check_stability(G, checkpoint_end_time, stable_first):
  temp_valences = add_edges(G, checkpoint_end_time)
  # get all triangles in the graph and check if they are stable
  triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
  for triangle in triangles:
    [character_a, character_b, character_c] = triangle
    
    character_pairs = [
        sorted([character_a, character_b]),
        sorted([character_b, character_c]),
        sorted([character_a, character_c])
    ]

    # A triangle is stable if stability_check is positive -> if the weights are pos * pos * pos = pos or pos * neg * neg = pos
    # A triangle is stable if stability_check is negative -> if the weights are neg * neg * neg = neg or pos * pos * neg = neg
    stability_check = 1
    for pair in character_pairs:
      stability_check = stability_check * temp_valences[tuple(pair)]

    triangle.sort()
    stability_key = tuple(triangle)

    # if stable_first is true, check triangles going from stable to unstable
    # if srable_first is false, check triangles going from unstable to stable
    if stable_first:
      stable_to_unstable(stability_key, stability_check)
    else:
      unstable_to_stable(stability_key, stability_check)
  print_triangle_stability()

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

# formatting the printing
def print_triangle_stability():
  for key in triangle_stability:
    (a, b, c) = key
    names = a + "/" + b + "/" + c
    stability_string = 'stable' if triangle_stability[key] else 'unstable' 

    print(f"{names:<35} {stability_string}")
  print()

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
