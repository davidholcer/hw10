import argparse
import csv
import json
import os
from collections import Counter

def clean_character_name(name):
    # Function to clean and lowercase character names
    name = name.lower().strip()
    forbidden_words = ["others", "ponies", "and", "all"]
    for word in forbidden_words:
        if word in name:
            return None
    return name

def get_top_characters(input_file, top_n=101):
    # Counter to store character frequencies
    character_counter = Counter()

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            speaker = clean_character_name(row['pony'])
            if speaker is not None:
                character_counter[speaker] += 1

    # Get the top N characters based on speaking lines
    top_characters = [character for character, _ in character_counter.most_common(top_n) if clean_character_name(character) is not None]
    return set(top_characters)

def build_interaction_network(input_file, output_file, top_characters):
    # Dictionary to store the interaction network
    interaction_network = {}
    current_episode = None
    current_speaker = None

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        

        for row in reader:
            episode_title = row['title']
            # If it's a new episode, reset the current speaker
            if current_episode != episode_title:
                current_episode = episode_title
                current_speaker = None

            speaker = clean_character_name(row['pony'])

            # print(current_speaker,speaker,current_episode,interaction_network)

            if speaker is not None and speaker in top_characters:
                # Check if the speaker is different from the previous speaker and not None
                if current_speaker is not None and current_speaker != speaker:
                    # Update interaction count
                    if current_speaker in interaction_network:
                        interaction_network[current_speaker][speaker] = interaction_network[current_speaker].get(speaker, 0) + 1
                    else:
                        interaction_network[current_speaker]={speaker:1}
                    if speaker in interaction_network:
                        interaction_network[speaker][current_speaker] = interaction_network[speaker].get(current_speaker, 0) + 1
                    else:
                        interaction_network[speaker]={current_speaker:1}
                elif current_speaker is None:
                    # First encounter with current_speaker, create an entry in the interaction network
                    # interaction_network[current_speaker] = {speaker: 1}
                    # interaction_network[speaker] = {current_speaker: 1}
                    pass

                current_speaker = speaker

    # Create the output folder if it does not exist
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write the interaction network to a JSON file
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(interaction_network, jsonfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description='Build MLP Interaction Network')
    parser.add_argument('-i', '--input', help='Path to the input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output JSON file', required=True)
    args = parser.parse_args()

    # Get the top 101 characters excluding specified words
    top_characters = get_top_characters(args.input)

    # Build the interaction network and save it to a JSON file
    build_interaction_network(args.input, args.output, top_characters)
