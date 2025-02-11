import psutil
import os
import time

#set cpu thresholds

CPU_THRESHOLD = 10  # Percentage of CPU usage
MEMORY_THRESHOLD = 10  # Percentage of memory usage

#function to terminate a process by its PID
def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        print(f"Process {pid} terminated successfully.")
    except Exception as e:
        print(f"Failed to terminate process {pid}: {e}")

#Monitor System Resources

def monitor_resources(auto_kill=False):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # Get process details
            process_name = proc.info['name']
            process_id = proc.info['pid']
            cpu_usage = psutil.Process(process_id).cpu_percent(interval=1.0)
            memory_usage = proc.info['memory_percent']

            # Check if the process exceeds thresholds
            if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
                print(f"Process {process_name} (PID: {process_id}) is using too many resources!")
                print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")

                # Prompt the user to terminate the process
                action = input("Do you want to terminate this process? (y/n): ").lower()
                if action == 'y':
                    terminate_process(process_id)
                else:
                    print("Process not terminated.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    print("Starting system resource monitor...")
    while True:
        monitor_resources(auto_kill=False)  # Set auto_kill=False to prompt the user
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()