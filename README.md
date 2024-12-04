
# Cyber Deception with IoT Botnets: Reproducing the Analysis from "Analyzing Variation Among IoT Botnets Using Medium Interaction Honeypots"

## Overview

This project aims to reproduce the results and methodology described in the paper **"Analyzing Variation Among IoT Botnets Using Medium Interaction Honeypots"** by Bryson Lingenfelter, Iman Vakilinia, and Shamik Sengupta. In this paper, the authors analyze sessions in which files were created and downloaded on Cowrie SSH/Telnet honeypots. Their analysis reveals that IoT botnets, particularly Mirai, are the most common sources of malware on systems with weak credentials.

By setting up **Cowrie honeypots** and analyzing the botnet activity, this project simulates an environment for capturing malicious activity, particularly IoT botnet interactions, and evaluates these attacks using the **ELK Stack** (Elasticsearch, Logstash, Kibana) for log visualization and analysis.

## Objective

The goal is to reproduce the analysis done by the authors by setting up the following:

1. **Cowrie Honeypot**: To simulate an SSH/Telnet server that attracts IoT botnet attacks.
2. **Mirai Botnet**: To simulate real-world attacks targeting weak IoT devices.
3. **ELK Stack**: To collect, store, and visualize logs for attack analysis.
4. **Filebeat**: To ship logs from Cowrie to Elasticsearch for real-time analysis in Kibana.

---

## Setup Instructions

This section provides a comprehensive guide on how to set up the components required for this project.

### Prerequisites

#### 1. Software Requirements

- **Operating System**: Linux-based (Ubuntu preferred)
- **Python 3.x** (required for Cowrie and its dependencies)
- **Mirai Botnet** (for simulating IoT botnet attacks)
- **Elasticsearch**, **Kibana**, and **Filebeat** (for log analysis and visualization)

#### 2. Libraries

- **Cowrie**:
  - `virtualenv`, `pip` for Python package management
  - Dependencies: `libssl-dev`, `libffi-dev`, `libpcap-dev`, `build-essential`

- **Mirai Botnet**:
  - `make`, `gcc`, `g++`, `git`

#### 3. Hardware Requirements

- **CPU**: Minimum 2 cores (recommended 4 cores)
- **RAM**: Minimum 4GB (recommended 8GB)
- **Disk Space**: 40GB (for logs, software, and datasets)

---

### Step-by-Step Installation

#### 1. **Set Up Cowrie Honeypot**

1. **Install dependencies for Cowrie**:
   Run the following commands to install the required packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-dev libssl-dev libffi-dev build-essential libpython3-dev libpcap-dev
   ```

2. **Clone the Cowrie repository**:
   Clone the Cowrie honeypot repository:
   ```bash
   git clone https://github.com/cowrie/cowrie.git
   cd cowrie
   ```

3. **Create a virtual environment and install dependencies**:
   Set up the Python virtual environment:
   ```bash
   virtualenv --python=python3 venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Cowrie**:
   Edit the `cowrie.cfg` file to simulate an SSH server:
   ```bash
   nano cowrie.cfg
   ```

5. **Start Cowrie**:
   Run the Cowrie honeypot:
   ```bash
   bin/cowrie start
   ```

#### 2. **Install Elasticsearch**

1. **Update the package list**:
   ```bash
   sudo apt-get update
   ```

2. **Add the GPG key for Elasticsearch**:
   ```bash
   sudo sh -c 'wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -'
   ```

3. **Add the Elasticsearch APT repository**:
   ```bash
   sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list'
   ```

4. **Update the package list again**:
   ```bash
   sudo apt-get update
   ```

5. **Install Elasticsearch**:
   ```bash
   sudo apt-get install elasticsearch
   ```

#### 3. **Install Kibana**

1. **Install Kibana** (if not already installed):
   ```bash
   sudo apt-get install kibana
   ```

2. **Configure Kibana** to read from Elasticsearch and access it at:
   ```
   http://<Kibana-IP>:5601
   ```

#### 4. **Install Filebeat to Ship Logs to Elasticsearch**

1. **Install Filebeat**:
   ```bash
   sudo apt-get install filebeat
   ```

2. **Configure Filebeat**:
   Edit `filebeat.yml` to specify the path to Cowrie logs:
   ```yaml
   filebeat.inputs:
     - type: log
       paths:
         - /home/server/cowrie/var/logs/cowrie/cowrie.json
   ```

3. **Configure Filebeat Output**:
   Set the output to Elasticsearch:
   ```yaml
   output.elasticsearch:
     hosts: ["http://localhost:9200"]
   ```

4. **Start Filebeat**:
   ```bash
   sudo systemctl start filebeat
   sudo systemctl enable filebeat
   ```

#### 5. **Clone and Set Up Mirai Botnet**

1. **Clone the Mirai Botnet repository**:
   ```bash
   git clone https://github.com/jgamblin/Mirai-Source-Code.git
   cd Mirai-Source-Code
   ```

2. **Install dependencies**:
   Ensure you have the necessary build tools:
   ```bash
   sudo apt-get install make gcc g++ git
   ```

3. **Build Mirai Botnet**:
   Compile the source code:
   ```bash
   make
   ```

4. **Configure Mirai Botnet**:
   Modify the configuration files to target your Cowrie honeypot and adjust settings.

---

### Running the Experiment

1. **Start the Cowrie Honeypot**:
   ```bash
   bin/cowrie start
   ```

2. **Launch the Mirai Botnet** to simulate attacks on the Cowrie honeypot.

3. **Monitor Cowrie Logs**:
   Use the `tail` command to monitor the Cowrie log output:
   ```bash
   tail -f /home/server/cowrie/var/logs/cowrie/cowrie.json
   ```

4. **View Logs in Kibana**:
   - Open Kibana at `http://localhost:5601`.
   - Use the **Discover** tab to view and analyze logs.

---

### Troubleshooting

- **Version mismatches**:
  - Ensure Python 3.x is used for Cowrie.
  - Ensure all dependencies for Mirai (make, gcc, git) are installed.

- **Elasticsearch connection issues**:
  - Ensure Elasticsearch is running:
    ```bash
    sudo systemctl status elasticsearch
    ```

  - Ensure Kibana is configured correctly to connect to Elasticsearch.
  - Making sure correct logs file is specify in filebeat by adding * to back og logs file to fetch all.


### Conclusion

By setting up **Cowrie honeypots** and simulating attacks with **Mirai Botnet**, this project aims to replicate the findings of Lingenfelter et al. in their research. Through the **ELK Stack** (Elasticsearch, Kibana), we can analyze and visualize the attack logs, providing insights into IoT botnet activity and honeypot effectiveness.
