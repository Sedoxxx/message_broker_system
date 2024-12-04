import subprocess
import time
import signal
import sys

NUM_PROCESSES = 30  # Adjust based on your system capabilities
VIDEO_FILE = "polish-cow.mp4"  # Path to the video file to process
MAIN_SCRIPT = "../../video-pipes-filters/main2.py"  # Path to your main.py script

processes = []  # Global list to store all subprocesses

def signal_handler(sig, frame):
    """Handle keyboard interrupt (Ctrl+C)."""
    print("\nKeyboard interrupt received. Terminating all processes...")
    for instance_id, p, log_file in processes:
        if p.poll() is None:  # Check if the process is still running
            p.terminate()
            log_file.close()
    sys.exit(0)

def main():
    global processes

    # Register the keyboard interrupt signal handler
    signal.signal(signal.SIGINT, signal_handler)

    start_time = time.time()

    print(f"Starting load test with {NUM_PROCESSES} parallel instances.")

    for instance_id in range(NUM_PROCESSES):
        print(f"Instance {instance_id}: Starting pipeline.")
        log_file = open(f"pipeline_{instance_id}.log", "w")
        p = subprocess.Popen(
            ["python", MAIN_SCRIPT, "--video", VIDEO_FILE, "--display"],
            stdout=log_file,
            stderr=log_file,
        )
        processes.append((instance_id, p, log_file))

    # Wait for all processes to complete
    for instance_id, p, log_file in processes:
        try:
            p.wait()  # Block until the process finishes
        finally:
            log_file.close()
            print(f"Instance {instance_id}: Pipeline completed.")

    end_time = time.time()
    total_duration = end_time - start_time

    print(f"Load test completed.")
    print(f"Total time taken: {total_duration:.2f} seconds.")

    # Write results to report.md
    with open("report2.md", "w") as report_file:
        report_file.write("# Load Testing Report for Pipes-and-Filters System\n\n")
        report_file.write(f"- **Total Instances**: {NUM_PROCESSES}\n")
        report_file.write(f"- **Total Time Taken**: {total_duration:.2f} seconds\n")
        report_file.write(f"- **Average Time per Instance**: {total_duration / NUM_PROCESSES:.2f} seconds\n")

if __name__ == "__main__":
    main()
