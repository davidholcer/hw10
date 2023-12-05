import argparse
import json
import networkx as nx

def load_interaction_network(input_file):
    with open(input_file, 'r', encoding='utf-8') as jsonfile:
        interaction_network = json.load(jsonfile)
    return interaction_network

def compute_stats(interaction_network):
    # Create an undirected graph from the interaction network
    G = nx.Graph(interaction_network)

    # Compute centrality measures
    degree_centrality = nx.degree_centrality(G)
    weighted_degree_centrality = nx.degree_centrality(G, weight='weight')
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

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
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(stats, jsonfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Compute MLP Interaction Network Statistics')
    parser.add_argument('-i', '--input', help='Path to the input interaction network JSON file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output stats JSON file', required=True)
    args = parser.parse_args()

    # Load the interaction network from the input file
    interaction_network = load_interaction_network(args.input)

    # Compute network statistics
    stats = compute_stats(interaction_network)

    # Save the stats to the output file
    save_stats(args.output, stats)
