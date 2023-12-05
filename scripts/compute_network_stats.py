import argparse
import json
import networkx as nx

#here it's loading the interaction network
def load_interaction_network(input_file):
    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        interaction_network = json.load(jsonfile)
    return interaction_network

#computing the stats
def compute_stats(graph):
    # Compute weighted degree centrality
    weighted_degree_centrality = dict(graph.degree(weight='weight'))

    # Compute other centrality measures
    degree_centrality = nx.degree_centrality(graph)
    closeness_centrality = nx.closeness_centrality(graph, distance='weight')
    betweenness_centrality = nx.betweenness_centrality(graph, weight='weight')

    # Get the top three characters for each centrality measure
    top_degree = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:3]
    top_weighted_degree = sorted(weighted_degree_centrality, key=weighted_degree_centrality.get, reverse=True)[:3]
    top_closeness = sorted(closeness_centrality, key=closeness_centrality.get, reverse=True)[:3]
    top_betweenness = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:3]

    # Build the output structure
    output_stats = {
        "degree": top_degree,
        "weighted_degree": top_weighted_degree,
        "closeness": top_closeness,
        "betweenness": top_betweenness
    }

    return output_stats

def save_stats(output_file, stats):
    # Write the stats to a JSON file
    with open(output_file, 'w', encoding='utf-8') as theOutput:
        json.dump(stats, theOutput, indent=2)

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Compute MLP Interaction Network Statistics')
    parser.add_argument('-i', '--input', help='Path to the input interaction network JSON file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output stats JSON file', required=True)
    args = parser.parse_args()

    # Load the interaction network from the input file
    interaction_network = load_interaction_network(args.input)

    # Create a weighted directed graph from the interaction network
    # it is directed since both a and b are accounted for but in reality 
    # functions as undirected as a->b iff b->a
    G = nx.DiGraph()

    for source, targets in interaction_network.items():
        for target, weight in targets.items():
            G.add_edge(source, target, weight=weight)

    # Compute network statistics
    stats = compute_stats(G)

    # Save the stats to the output file
    save_stats(args.output, stats)
