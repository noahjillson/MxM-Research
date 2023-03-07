import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx

# Generate a random graph with 10 nodes and 15 edges
G = nx.gnm_random_graph(10, 15)

# Compute a force-directed layout for the graph
pos = nx.spring_layout(G, dim=3)

# Get the x, y, and z coordinates of the nodes
x = [pos[n][0] for n in G.nodes()]
y = [pos[n][1] for n in G.nodes()]
z = [pos[n][2] for n in G.nodes()]

# Create a 3D scatter plot of the nodes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, color='blue')

# Get the list of edges and their endpoints
edges = [(u, v) for (u, v) in G.edges()]

# Plot the edges
for (u, v) in edges:
    ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], [pos[u][2], pos[v][2]], color='red')

# Show the plot
plt.show()
