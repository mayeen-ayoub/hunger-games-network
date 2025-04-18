# Note: This file was used to generate the valence graphs used in the presentation

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os

deaths = set()
curr_valences = {}

# CHANGEABLE VARIABLES
checkpoints = ['00:00:00', '00:27:00', '01:04:00', '1:07:00', '01:24:00', '1:39:00', '1:51:30', '02:17:00']
imp_people = set()

# PART 1
# imp_people = {'Katniss', 'Peeta', 'Haymitch'}

# PART 2
# imp_people = {'Peeta', 'Glimmer', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Cato', 'Jason'}

# PART 4
# imp_people = {'Peeta', 'Glimmer', 'Clove', 'Cato', 'Marvel'}
# imp_people = {'Katniss', 'Peeta', 'Rue'}

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

# read the data from valences.csv 
valences_filepath = os.path.join('data', 'valences.csv')
df = pd.read_csv(valences_filepath)

# add the nodes to the graph
def add_nodes(G):
  # read the data from characters.csv
  characters_filepath = os.path.join('data', 'characters.csv')
  characters_df = pd.read_csv(characters_filepath)
  non_tributes = ['Primrose', 'Gale', 'Effie', 'Katniss\' mom', 'Haymitch', 'Cinna', 'President Snow', 'Seneca']
  # add a node for each entry unless the character has died by this point or they are not in imp_people
  for col, row in characters_df.iterrows():
    global imp_people
    if len(imp_people) != 0 and row['Character'] not in imp_people:
      continue
    # colour the node white, unless this is a non-tribute (in this case colour them gray)
    colour = 'white'
    curr_character = row['Character']
    if curr_character in non_tributes:
      colour = 'lightgray'
    global deaths
    if row['Character'] not in deaths:
      G.add_node(row['Character'], color=colour)


# add the edges to the graph
def add_edges(G, checkpoint_start_time, checkpoint_end_time):
  for col, row in df.iterrows():
    acting_node = row['Acting Character']  
    receiving_node = row['Receiving Character']  
    # do not add this edge if the nodes are not in the graph
    global imp_people
    if len(imp_people) != 0 and (acting_node not in imp_people or receiving_node not in imp_people):
      continue
    row_start_time = datetime.strptime(row['Time Start'], '%H:%M:%S').time()
    row_end_time = datetime.strptime(row['Time End'], '%H:%M:%S').time()
    # only add the edge if we have reached that point in time or it's an existing alliance
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

        # colour the edge according to its valence
        if (G[acting_node][receiving_node]['weight'] < 0):
          G[acting_node][receiving_node]['color'] = 'red'
        elif (G[acting_node][receiving_node]['weight'] == 0):
          G[acting_node][receiving_node]['color'] = 'black'
        else: 
          G[acting_node][receiving_node]['color'] = 'green'
  # if there are any neutral edges (ie. with weight 0) set their weight to 1 to ensure it shows in the graph
  for u, v in G.edges():
    if (G[u][v]['weight'] == 0):
      G[u][v]['weight'] = 1

# create a graph for each part (based on checkpoints)
def create_graphs():
  for i in range(len(checkpoints) - 1):
    G = nx.Graph()
    add_nodes(G)
    checkpoint_start_time = datetime.strptime(checkpoints[i], '%H:%M:%S').time()
    checkpoint_end_time = datetime.strptime(checkpoints[i + 1], '%H:%M:%S').time()

    add_edges(G, checkpoint_start_time, checkpoint_end_time)
    # use NetworkX's built-in circular layout option to position the nodes
    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 6))

    weights = nx.get_edge_attributes(G, 'weight').values()
    edge_colours = nx.get_edge_attributes(G, 'color').values()
    node_colours = nx.get_node_attributes(G, 'color').values()

    # draw the graph using the node and edge properties set earlier 
    nx.draw_networkx(G, pos, with_labels=True, width=list(weights), edge_color=edge_colours, node_size=3000, node_color=node_colours, edgecolors='black', font_size=10, font_weight='bold')
    plt.show()

create_graphs()
