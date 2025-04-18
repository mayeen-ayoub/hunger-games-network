# Hunger Games Network Project

Team 18 🚀

## Running the code 🛠️
1. pip install pandas networkx matplotlib
1. python <filename> (eg. python valences_manual.py)

## Changeable Variables 💾
For any of the Python code, the following variables can be changed:
- Modify `checkpoints` variable to include timestamps to break up the graph into checkpoint graphs
	- `checkpoints = ['00:00:00', '02:17:00']` will make one graph for the entire movie
- Modify `imp_people` variable to create subgraphs that only include the people listed
	- `imp_people = {'Peeta', 'Katniss', 'Cato'}` will only generate edges between Peeta, Katniss and Cato for each checkpoint
- **Note:** `deaths.py` does not have `checkpoints` variable and `triangle_stability.py` does not have `imp_people` variable

For `triangle_stability.py`:
- Modify `stable_first` to `True` if you want to see the triangles that changed from stable to unstable
- Modify `stable_first` to `False` if you want to see the triangles that changed from unstable to stable


## Repository Organization 🗂️
```bash
hunger-games-network
├── README.md
├── data
│   ├── characters.csv
│   ├── deaths.csv
│   └── valences.csv
├── deaths.py
├── triangle_stability.py
├── valences_circular.py
└── valences_manual.py
```
