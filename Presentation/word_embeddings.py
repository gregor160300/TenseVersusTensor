import plotly.graph_objects as go

# Sample word embeddings (3D vectors)
embeddings = {
    'dog': [0.8, 0.5, 0.3],
    'cat': [0.7, 0.6, 0.2],
    'turtle': [0.4, 0.3, 0.9],
    'bus': [-0.6, 0.7, -0.2],
    'car': [-0.5, 0.5, -0.1],
    'airplane': [-0.3, 0.2, 0.9],
    'rock': [0.1, -0.8, -0.5]
}

# Extract coordinates and labels
words = list(embeddings.keys())
x, y, z = zip(*[embeddings[word] for word in words])

# Create the 3D scatter plot for points
scatter = go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+text',
    text=words,
    marker=dict(size=10, color=list(range(len(words))), colorscale='Viridis'),
    textfont=dict(size=48),
    textposition="top center"
)

# Create lines from origin to each point
lines = []
for word, (xi, yi, zi) in zip(words, zip(x, y, z)):
    lines.append(go.Scatter3d(
        x=[0, xi], y=[0, yi], z=[0, zi],
        mode='lines',
        line=dict(color='black', width=3),
        hoverinfo='none',
        showlegend=False
    ))

# Add arrow heads
arrow_heads = go.Cone(
    x=x, y=y, z=z,
    u=[xi*0.1 for xi in x],
    v=[yi*0.1 for yi in y],
    w=[zi*0.1 for zi in z],
    sizemode="absolute",
    sizeref=0.01,
    anchor="tip",
    colorscale=[[0, 'black'], [1, 'black']],
    showscale=False
)

# Combine scatter plot, lines, and arrow heads
fig = go.Figure(data=[scatter] + lines + [arrow_heads])

# Update layout
fig.update_layout(
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        aspectmode="cube"
    ),
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'

)

# Show the plot
fig.show()
