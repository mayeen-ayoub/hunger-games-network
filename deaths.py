import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

deaths_filepath = os.path.join('data', 'deaths.csv')
df = pd.read_csv(deaths_filepath)
G = nx.DiGraph()

for i in range(len(df)):
  killer = df['Killer'][i] 
  killed = df['Killed'][i] 
  G.add_edge(killer, killed)  

pos = {
  'Katniss': (-0.5, -0.5), 'Peeta': (1, 1.5), 'Rue': (-1, -0.5), 'Thresh': (-2, -0.5),
  'Clove': (-2, 1.5), 'Marvel': (-0.5, 1.5), 'Cato': (0.5, 1.5), 'Glimmer': (1.5, 1.5),
  'F4': (1, -0.5), 'F3': (1.5, -0.5), 'F8': (1, 2.5), 'M9': (-2.5, 1.5), 'M7': (-2.5, -0.5), 
  'M8': (-1.2, 0.5), 'F7': (-1.2, 1), 'F9': (-1.2, 0), 'M3': (-0.5, 2.5), 'M10': (-1.2, 2.5), 
  'M4': (1, 0.5), 'Jason': (1, 1), 'M5': (1.5, 0), 'F10': (2, 1), 'F6': (2, 0.5),
  'Foxface': (1, -1.5), 'President Snow': (-2, -1.5), 'Seneca': (-2, -1), 'Haymitch': (0, -1.5),
  'Cinna': (-1.5, -1.5), 'Effie': (0.5, -1.5), 'Primrose': (-1, -2), 'Gale': (1, -1.5), 'Katniss\' mom': (-0.5, -1.5)
}

plt.figure(figsize=(8, 6))
nx.draw_networkx(G, pos, with_labels=True, node_size=3000, node_color='white', edgecolors='black', font_size=10, font_weight='bold')
plt.show()
