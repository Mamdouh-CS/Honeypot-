import json
import os
import pandas as pd
import numpy as np
import Levenshtein as lev
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Define the path to your Cowrie log directory
log_dir = '/home/server/cowrie/var/log/cowrie'

# Define baseline commands (legitimate commands)
baseline_commands = ["ls", "pwd", "cat", "whoami", "cd", "echo", "uname", "touch"]

# Function to load the Cowrie JSON logs
def load_cowrie_logs(log_dir):
    all_data = []
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.json')]
    for log_file in log_files:
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    all_data.append(data)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line in {log_file}")
    return all_data

# Function to extract session data, including login attempts and commands
def extract_sessions_and_commands(log_data):
    session_data = []
    for entry in log_data:
        session_id = entry.get('session')
        event_id = entry.get('eventid')
        
        if event_id in ['cowrie.login.failed', 'cowrie.login.success']:
            username = entry.get('username', '')
            password = entry.get('password', '')
            command = f"{username}/{password}"
            session_data.append((session_id, command))
        elif 'input' in entry:
            command = entry['input']
            session_data.append((session_id, command))
    return session_data

# Function to calculate anomalies based on Levenshtein distance
def detect_anomalies(session_data, baseline_commands, threshold=3):
    anomalies = []
    for session_id, command in session_data:
        distances = [lev.distance(command, baseline) for baseline in baseline_commands]
        min_distance = min(distances)
        if min_distance > threshold:
            anomalies.append((session_id, command, min_distance))
    return anomalies

# Function to calculate Levenshtein distance matrix
def calculate_levenshtein_matrix(session_data):
    sessions = list(set([session for session, _ in session_data]))
    matrix = np.zeros((len(sessions), len(sessions)))

    for i, session_1 in enumerate(sessions):
        for j, session_2 in enumerate(sessions):
            commands_1 = [command for session, command in session_data if session == session_1]
            commands_2 = [command for session, command in session_data if session == session_2]
            dist = np.mean([lev.distance(c1, c2) for c1 in commands_1 for c2 in commands_2])
            matrix[i, j] = dist
    return sessions, matrix

# Function to generate and save the dendrogram
def generate_dendrogram(matrix, sessions):
    linked = linkage(matrix, method='average')
    plt.figure(figsize=(10, 7))
    dendrogram(linked, labels=sessions, orientation='top', distance_sort='descending')
    plt.title('Clustering of Sessions based on Levenshtein Distance')
    plt.xlabel('Session ID')
    plt.ylabel('Distance')
    plt.savefig('dendrogram.png')
    plt.show()

# Main function to process logs and detect anomalies
def main():
    print("Loading Cowrie logs...")
    log_data = load_cowrie_logs(log_dir)
    session_data = extract_sessions_and_commands(log_data)
    print(f"Extracted {len(session_data)} session-command pairs.")

    print("Detecting anomalies...")
    anomalies = detect_anomalies(session_data, baseline_commands)
    if anomalies:
        print(f"Detected {len(anomalies)} anomalies:")
        for anomaly in anomalies:
            print(f"  Session: {anomaly[0]} | Command: {anomaly[1]} | Distance: {anomaly[2]}")
    else:
        print("No anomalies detected.")

    # Save anomalies to CSV
    anomalies_df = pd.DataFrame(anomalies, columns=["Session ID", "Command", "Distance"])
    anomalies_df.to_csv("anomalies.csv", index=False)
    print("Anomalies saved to 'anomalies.csv'.")

    print("Calculating Levenshtein distance matrix...")
    sessions, matrix = calculate_levenshtein_matrix(session_data)

    # Save the distance matrix
    df = pd.DataFrame(matrix, index=sessions, columns=sessions)
    df.to_csv('levenshtein_distance_matrix.csv')
    print("Levenshtein distance matrix saved to 'levenshtein_distance_matrix.csv'.")

    print("Generating dendrogram...")
    generate_dendrogram(matrix, sessions)
    print("Dendrogram generated and saved as 'dendrogram.png'.")

if __name__ == "__main__":
    main()
