import csv
from datetime import datetime
import os
import platform
import subprocess
import time

# List of targets to monitor
TARGETS = ["google.com", "github.com", "8.8.8.8"]
LOG_FILE = "incident_log.csv"


def initialize_log():
  """Creates the CSV log file with headers if it doesn't exist."""
  if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["Timestamp", "Target", "Status", "Details"])


def ping_host(host):
  """Pings a host and returns True if online, False if offline."""
  param = "-n" if platform.system().lower() == "windows" else "-c"
  command = ["ping", param, "1", host]

  try:
    result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0
  except Exception as e:
    return False


def log_incident(timestamp, target, status, details):
  """Appends an incident record to the CSV file."""
  with open(LOG_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([timestamp, target, status, details])


def monitor_network():
  initialize_log()
  print(
      "[*] Starting Network Uptime Monitor... Click the Stop button (square icon"
      f" on the left of the cell) to stop.\nMonitoring targets: {TARGETS}\n"
  )

  previous_states = {target: True for target in TARGETS}

  # Running for a few cycles in Colab to demonstrate cleanly
  for cycle in range(3):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- Check Cycle {cycle + 1} at {current_time} ---")

    for target in TARGETS:
      is_online = ping_host(target)

      if is_online:
        print(f"  {target} -> UP")
        if not previous_states[target]:
          log_incident(current_time, target, "RECOVERED", "Service restored")
          previous_states[target] = True
      else:
        print(f"  ⚠️ {target} -> DOWN (Incident Detected)")
        if previous_states[target]:
          log_incident(
              current_time, target, "DOWN", "Packet loss / Connection failed"
          )
          previous_states[target] = False

    print("-" * 40)
    if cycle < 2:
      time.sleep(5)

  print(
      "\n[!] Monitoring demo completed. CSV log file 'incident_log.csv' has"
      " been saved!"
  )


if __name__ == "__main__":
  monitor_network()
