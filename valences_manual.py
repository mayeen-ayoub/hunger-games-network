import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

checkpoints = ['00:00:00', '00:27:00', '01:04:00', '1:07:00', '01:24:00', '1:39:00', '1:51:30', '02:17:00']
# checkpoints = ['00:00:00', '02:17:00']

deaths = set()
imp_people = set()

# imp_people = {'Peeta', 'Glimmer', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Katniss', 'Peeta', 'Rue'}

# imp_people = {'Katniss', 'Peeta', 'Haymitch'}
# imp_people = {'Cato', 'Jason'}
# imp_people = {'Katniss', 'Foxface'}

# PART 5
# imp_people = {'Katniss', 'Rue', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'F8', 'Clove', 'Cato', 'Marvel', 'Glimmer'}
# imp_people = {'M10', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'M3', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Katniss', 'Marvel', 'Rue'}

# PART 6
# imp_people = {'Katniss', 'Thresh', 'Rue'}
# imp_people = {'Katniss', 'Thresh', 'Clove'}

# PART 7
# imp_people = {'Peeta', 'Katniss', 'Cato'}
# imp_people = {'President Snow', 'Seneca', 'Katniss'}

curr_valences = {}
valences_filepath = os.path.join('data', 'valences.csv')
df = pd.read_csv(valences_filepath)

def add_nodes(G):
  characters_filepath = os.path.join('data', 'characters.csv')
  characters_df = pd.read_csv(characters_filepath)
  for col, row in characters_df.iterrows():
    global imp_people
    if len(imp_people) != 0 and row['Character'] not in imp_people:
      continue
    global deaths
    if row['Character'] not in deaths:
      G.add_node(row['Character'])


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
      'F4': (1, -0.5), 'F3': (1.5, -0.5), 'F8': (1, 2.5), 'M9': (-2, 2), 'M7': (-2.5, -0.5), 
      'M8': (-1.2, 0.5), 'F7': (-1.2, 1), 'F9': (-1.2, 0), 'M3': (-0.5, 2.5), 'M10': (-1.2, 2.5), 
      'M4': (1, 0.5), 'Jason': (1, 1), 'M5': (1.5, 0), 'F10': (2, 1), 'F6': (2, 0.5), 
      'Foxface': (1, -1), 'President Snow': (-2, -1.5), 'Seneca': (-2, -1), 'Haymitch': (0, -1.5), 
      'Cinna': (-1.5, -1.5), 'Effie': (0.5, -1.5), 'Primrose': (-1, -2), 'Gale': (1, -1.5), 'Katniss\' mom': (-0.5, -1.5)
    }

    labels = {
      'Katniss': 'Katniss\nD12', 'Peeta': 'Peeta\nD12', 'Rue': 'Rue\nD11', 'Thresh': 'Thresh\nD11',
      'Clove': 'Clove\nD2', 'Marvel': 'Marvel\nD1', 'Cato': 'Cato\nD2', 'Glimmer': 'Glimmer\nD1',
      'F4': 'F4\nD4', 'F3': 'F3\nD3', 'F8': 'F8\nD8', 'M9': 'M9\nD9', 'M7': 'M7\nD7', 
      'M8': 'M8\nD8', 'F7': 'F7\nD7', 'F9': 'F9\nD9', 'M3': 'M3\nD3', 'M10': 'M10\nD10', 
      'M4': 'M4\nD4', 'Jason': 'Jason\nD6', 'M5': 'M5\nD5', 'F10': 'F10\nD10', 'F6': 'F6\nD6', 
      'Foxface': 'Foxface\nD5', 'President Snow': 'President\n Snow', 'Seneca': 'Seneca', 'Haymitch': 'Haymitch', 
      'Cinna': 'Cinna', 'Effie': 'Effie', 'Primrose': 'Primrose', 'Gale': 'Gale', 'Katniss\' mom': 'Katniss\'\nmom'
    }

    greyscale = [
      '#1A1A1A', '#2E2E2E', '#424242', '#565656',
      '#6A6A6A', '#7F7F7F', '#939393', '#A7A7A7',
      '#BBBBBB', '#D0D0D0', '#E4E4E4', '#F8F8F8'
    ]

    for node in G.nodes():
      label = labels.get(node, '')
      match = re.search(r'D(\d+)', label)
      if match:
        district_num = int(match.group(1)) 
        G.nodes[node]['color'] = greyscale[district_num - 1]
        if district_num <= 6:
          G.nodes[node]['font_color'] = 'white'
        else:
          G.nodes[node]['font_color'] = 'black'
      else: 
        G.nodes[node]['color'] = 'wheat'
        G.nodes[node]['font_color'] = 'black'
     
    plt.figure(figsize=(8, 6))

    weights = nx.get_edge_attributes(G, 'weight').values()
    edge_colours = nx.get_edge_attributes(G, 'color').values()
    node_colours = nx.get_node_attributes(G, 'color').values()
    white_font_nodes = [n for n in G.nodes() if G.nodes[n]['font_color'] == 'white']
    black_font_nodes = [n for n in G.nodes() if G.nodes[n]['font_color'] == 'black']

    nx.draw_networkx(G, pos, with_labels=False, width=list(weights), edge_color=edge_colours, node_size=3000, node_color=node_colours, edgecolors='black')    
    nx.draw_networkx_labels(G, pos, labels={n: labels.get(n, '') for n in white_font_nodes}, font_color='white', font_size=10)
    nx.draw_networkx_labels(G, pos, labels={n: labels.get(n, '') for n in black_font_nodes}, font_color='black', font_size=10)
    plt.show()

create_graphs()
