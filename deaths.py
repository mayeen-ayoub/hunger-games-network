import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import re

deaths_filepath = os.path.join('data', 'deaths.csv')
df = pd.read_csv(deaths_filepath)
G = nx.DiGraph()

highlighted_edges = {
  ('Marvel', 'F7'),
  ('Marvel', 'M8'),
  ('Marvel', 'F9'),
  ('Glimmer', 'F10'),
  ('Glimmer', 'F6'),
  ('Glimmer', 'M5'),
  ('Cato', 'Jason'),
  ('Cato', 'M4'),
  ('Clove', 'M9'),
  ('F4', 'F3'),
  ('M5', 'F3'),
  ('Thresh', 'M7')
}

# CHANGEABLE VARIABLE
imp_people = set()
# imp_people = {'Katniss', 'Marvel', 'Rue'}

for i in range(len(df)):
  killer = df['Killer'][i] 
  killed = df['Killed'][i]

  colour = 'black'
  if (killer, killed) in highlighted_edges:
    colour = 'red'

  if len(imp_people) == 0 or killer in imp_people and killed in imp_people:
    G.add_edge(killer, killed, color=colour)  

pos = {
  'Katniss': (-0.5, -0.5), 'Peeta': (1, 1.5), 'Rue': (-1, -0.5), 'Thresh': (-2, -0.5),
  'Clove': (-2, 1.5), 'Marvel': (-0.5, 1.5), 'Cato': (0.5, 1.5), 'Glimmer': (1.5, 1.5),
  'F4': (1, -0.5), 'F3': (1.5, -0.5), 'F8': (1, 2.5), 'M9': (-2.5, 1.5), 'M7': (-2.5, -0.5), 
  'M8': (-1.2, 0.5), 'F7': (-1.2, 1), 'F9': (-1.2, 0), 'M3': (-0.5, 2.5), 'M10': (-1.2, 2.5), 
  'M4': (1, 0.5), 'Jason': (1, 1), 'M5': (1.5, 0), 'F10': (2, 1), 'F6': (2, 0.5),
  'Foxface': (1, -1.5), 'President Snow': (-2, -1.5), 'Seneca': (-2, -1), 'Haymitch': (0, -1.5),
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

edge_colours = nx.get_edge_attributes(G, 'color').values()
node_colours = nx.get_node_attributes(G, 'color').values()
white_font_nodes = [n for n in G.nodes() if G.nodes[n]['font_color'] == 'white']
black_font_nodes = [n for n in G.nodes() if G.nodes[n]['font_color'] == 'black']

nx.draw_networkx(G, pos, with_labels=False, edge_color=edge_colours, node_size=3000, node_color=node_colours, edgecolors='black')    
nx.draw_networkx_labels(G, pos, labels={n: labels.get(n, '') for n in white_font_nodes}, font_color='white', font_size=10)
nx.draw_networkx_labels(G, pos, labels={n: labels.get(n, '') for n in black_font_nodes}, font_color='black', font_size=10)
plt.show()
