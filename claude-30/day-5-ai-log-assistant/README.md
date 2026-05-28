---
type: code
tags: 
  - ai
  - agent
---
# K8s SRE AI Agent

- An automated Site Reliability Engineering (SRE) agent built with Python and the Anthropic Claude API. The agent automatically reviews system log files, executes live kubectl commands to diagnose infrastructure anomalies, fixes local configuration manifests, and deploys updates back to your cluster.

- It includes a built-in safety engine that intercepts file writes and cluster mutations when running in evaluation modes.

## Features
- Log Parsing: Scans local applications logs (sample.log) to identify crashes, connection timeouts, and stack traces.
- Live Cluster Diagnosis: Safely utilizes kubectl to inspect real-time pod health, check states, and pull live runtimes.
- Auto-Remediation: Modifies resource manifests (configmap.yaml) directly when configuration discrepancies are detected.
- Dry-Run Protection Mode: Safe sandboxing framework that simulates changes without impacting live production resources.

## Requirements
- Python 3.8 or higher
- Configured kubectl CLI pointing to an active cluster or local environment (e.g., Minikube, Kind)
- Valid Anthropic API KeyInstallation
- Clone or download the script files to your workspace.
- Install the necessary library dependencies:

```bash
pip install anthropic python-dotenv
```

- Configure your Anthropic environment key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

- (Alternatively, create a .env file containing ANTHROPIC_API_KEY=your-key in the execution directory)

## How to Run It
1. Active Operational Mode (Live Changes)

- Runs the tool, updates the local files, applies configs, and restarts the target deployments in your cluster automatically:

```bash
python3 agent.py
```

2. Dry-Run Mode (Simulation & Auditing)
- Executes logs analysis and structural debugging safely. File system edits are printed directly to the terminal, and cluster modifications have safety verification flags applied:

```bash
python3 agent.py --dry-run
```

### Example Output (--dry-run Active)
```log
text[AI Tool Call] get_file_contents with args: {'path': 'sample.log'}
[Tool Response]: {'path': 'sample.log', 'file_content': '2026-05-19 18:45:12,118 [ERROR] ... ConnectionRefusedError: [Errno 111]'}

[AI Tool Call] run_shell_command with args: {'command': 'kubectl get pods -l app=myapp'}
[Tool Response]: {'command': 'kubectl get pods -l app=myapp', 'exit_code': 0, 'stdout': 'NAME                               READY   STATUS    RESTARTS   AGE\nmyapp-deployment-7fcf8b-abc12      1/1     Running   0          4m\n', 'stderr': ''}

[AI Tool Call] write_file_contents with args: {'path': 'configmap.yaml', 'content': 'apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: myapp-config\ndata:\n  DATABASE_URL: "mysql://user:pass@prod-db.internal:3306/mydb"\n'}

[DRY RUN] Would write the following content to 'configmap.yaml':
----------------------------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_URL: "mysql://user:pass@prod-db.internal:3306/mydb"
----------------------------------------
[Tool Response]: {'path': 'configmap.yaml', 'status': 'dry-run-skipped', 'message': '[DRY RUN ENABLED] File changes were simulated and logged but not saved to disk.'}

[AI Tool Call] run_shell_command with args: {'command': 'kubectl apply -f configmap.yaml'}
[DRY RUN] Appended safety flag. Executing: kubectl apply -f configmap.yaml --dry-run=client
[Tool Response]: {'command': 'kubectl apply -f configmap.yaml --dry-run=client', 'exit_code': 0, 'stdout': 'configmap/myapp-config configured (dry run)\n', 'stderr': ''}

*** Final Agent Summary ***
Root Cause: The Flask app application logs indicate a connection mismatch due to a missing or misconfigured DATABASE_URL.
Fix Applied: Corrected structural endpoint targets within configmap.yaml to map to the target production endpoint.
Action Taken: Simulated config mapping file creation and executed safe client dry-run verification against the cluster.
```