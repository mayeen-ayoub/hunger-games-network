import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os

checkpoints = ['00:00:00', '00:27:00', '01:04:00', '1:07:00', '01:24:00', '1:39:00', '1:51:30', '02:17:00']
# checkpoints = ['00:00:00', '02:17:00']
deaths = set()

# imp_people = {'Katniss', 'Rue', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Peeta', 'Glimmer', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'M3', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Katniss', 'Peeta', 'Rue'}
# imp_people = {'Peeta', 'Katniss', 'Cato'}
# imp_people = {'Katniss', 'Peeta', 'Haymitch'}
# imp_people = {'Cato', 'Jason'}
# imp_people = {'President Snow', 'Seneca'}
# imp_people = {'President Snow', 'Katniss'}
# imp_people = {'Katniss', 'Foxface'}

imp_people = set()

curr_valences = {}
valences_filepath = os.path.join('data', 'valences.csv')
df = pd.read_csv(valences_filepath)

def add_nodes(G):
  characters_filepath = os.path.join('data', 'characters.csv')
  characters_df = pd.read_csv(characters_filepath)
  non_tributes = ['Primrose', 'Gale', 'Effie', 'Katniss\' mom', 'Haymitch', 'Cinna', 'President Snow', 'Seneca']
  for col, row in characters_df.iterrows():
    global imp_people
    if len(imp_people) != 0 and row['Character'] not in imp_people:
      continue
    colour = 'white'
    curr_character = row['Character']
    if curr_character in non_tributes:
      colour = 'lightgray'
    global deaths
    if row['Character'] not in deaths:
      G.add_node(row['Character'], color=colour)


# EDGES ACCUMULATE
def add_edges(G, checkpoint_start_time, checkpoint_end_time):
  for col, row in df.iterrows():
    acting_node = row['Acting Character']  
    receiving_node = row['Receiving Character']  
    global imp_people
    if len(imp_people) != 0 and (acting_node not in imp_people or receiving_node not in imp_people):
      continue
    row_start_time = datetime.strptime(row['Time Start'], '%H:%M:%S').time()
    row_end_time = datetime.strptime(row['Time End'], '%H:%M:%S').time()
    if (((checkpoint_start_time <= row_start_time <= checkpoint_end_time) or (checkpoint_start_time <= row_end_time <= checkpoint_end_time) or (row_start_time <= checkpoint_start_time <= row_end_time and row_start_time <= checkpoint_end_time <= row_end_time))):
      if (acting_node != receiving_node):
        sorted_characters = [acting_node, receiving_node]
        sorted_characters.sort()
        dict_key = tuple(sorted_characters)
        curr_valences[dict_key] = row['Valence'] + curr_valences.get(dict_key, 0)
        G.add_edge(acting_node, receiving_node, weight=curr_valences[dict_key])  

        if '[DEATH]' in row['Action / Dialogue'] and receiving_node != 'Rue':
          global deaths
          deaths.add(receiving_node)

        if (G[acting_node][receiving_node]['weight'] < 0):
          G[acting_node][receiving_node]['color'] = 'red'
        elif (G[acting_node][receiving_node]['weight'] == 0):
          G[acting_node][receiving_node]['color'] = 'black'
        else: 
          G[acting_node][receiving_node]['color'] = 'green'
  for u, v in G.edges():
    if (G[u][v]['weight'] == 0):
      G[u][v]['weight'] = 1


def create_graphs():
  for i in range(len(checkpoints) - 1):
    G = nx.Graph()
    add_nodes(G)
    checkpoint_start_time = datetime.strptime(checkpoints[i], '%H:%M:%S').time()
    checkpoint_end_time = datetime.strptime(checkpoints[i + 1], '%H:%M:%S').time()

    add_edges(G, checkpoint_start_time, checkpoint_end_time)

    pos = {
      'Katniss': (-0.5, -0.5), 'Peeta': (0, 1), 'Rue': (-1.5, -0.5), 'Thresh': (-2, -0.5),
      'Clove': (-1.2, 2), 'Marvel': (-0.5, 1.5), 'Cato': (0.5, 2), 'Glimmer': (1.5, 1.5),
      'F4': (1, -0.5), 'F3': (1.5, -0.5), 'F8': (1, 2.5), 'M9': (-2.5, 1.5), 'M7': (-2.5, -0.5), 
      'M8': (-1.2, 0.5), 'F7': (-1.2, 1), 'F9': (-1.2, 0), 'M3': (-0.5, 2.5), 'M10': (-1.2, 2.5), 
      'M4': (1, 0.5), 'Jason': (1, 1), 'M5': (1.5, 0), 'F10': (2, 1), 'F6': (2, 0.5), 
      'Foxface': (1, -1), 'President Snow': (-2, -1.5), 'Seneca': (-2, -1), 'Haymitch': (0, -1.5), 
      'Cinna': (-1.5, -1.5), 'Effie': (0.5, -1.5), 'Primrose': (-1, -2), 'Gale': (1, -1.5), 'Katniss\' mom': (-0.5, -1.5)
    }

    plt.figure(figsize=(8, 6))

    weights = nx.get_edge_attributes(G, 'weight').values()
    edge_colours = nx.get_edge_attributes(G, 'color').values()
    node_colours = nx.get_node_attributes(G, 'color').values()

    nx.draw_networkx(G, pos, with_labels=True, width=list(weights), edge_color=edge_colours, node_size=3000, node_color=node_colours, edgecolors='black', font_size=10, font_weight='bold')
    plt.show()

create_graphs()
