import time
import os
import random
import string
import matplotlib.pyplot as plt
from cache_logic import LRUCache
from disk_sim import DiskSimulator
from stats import PerformanceTracker

def provision_disk(folder_name: str, file_list: list[str]):
    """Creates mock data files on disk to ensure simulation has data to read."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"[DISK] Created directory: {folder_name}")

    print(f"[DISK] Provisioning {len(file_list)} files with random data...")
    for filename in file_list:
        path = os.path.join(folder_name, filename)
        
        # Only create if it doesn't exist, or overwrite to ensure 100 lines
        with open(path, 'w') as f:
            for i in range(100):
                # Generate a random string for each line
                random_line = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
                f.write(f"Line {i+1}: {random_line}\n")
    print("[DISK] Provisioning complete.\n")

def plot_performance(latency_history: list[float]):
    """Generates the Hits vs Misses latency graph."""
    plt.figure(figsize=(10, 6))
    
    # Plot the line with markers
    plt.plot(latency_history, marker='o', linestyle='-', color='b', label='Request Latency')
    
    # Add the "Disk Threshold" line at 20ms
    plt.axhline(y=20, color='r', linestyle='--', label='Slow Disk Threshold (20ms)')
    
    # Styling
    plt.title("OS Cache Performance: Hits vs Misses", fontsize=14)
    plt.xlabel("Request Number", fontsize=12)
    plt.ylabel("Latency (ms)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print("\n[INFO] Displaying performance graph...")
    plt.show()

def run_os_simulation():
    # Setup
    capacity = 3
    cache = LRUCache(capacity)
    
    # Path configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "disk_data")
    
    disk = DiskSimulator(root_dir=data_path)
    stats = PerformanceTracker()
    
    # Define our access pattern (matching the provisioned files)
    # We use a pattern that tests temporal locality (repeats) and eviction
    requests = [
        "File1.txt", "File2.txt", "File3.txt",  # Fill cache (Caps at 3)
        "File1.txt",                            # HIT (File1 is MRU)
        "File4.txt",                            # MISS (File2 is evicted as LRU)
        "File1.txt",                            # HIT
        "File2.txt",                            # MISS (Re-fetch, File3 evicted)
        "File1.txt",                            # HIT
        "File1.txt",                            # HIT
        "File4.txt",                            # HIT
        "File3.txt"                             # MISS
    ]
    
    print(f"Starting OS Memory Management Simulation (Capacity: {capacity})...\n")
    
    for filename in requests:
        start = time.perf_counter()
        data = cache.get(filename)
        
        if data:
            latency = time.perf_counter() - start
            stats.record_hit(latency)
            print(f"[CACHE HIT]  Quickly retrieved {filename}")
        else:
            disk_data = disk.read_file(filename)
            if disk_data:
                evicted = cache.put(filename, disk_data)
                latency = time.perf_counter() - start
                stats.record_miss(latency)
                
                msg = f"[DISK MISS]  Fetched {filename} from disk."
                if evicted:
                    msg += f" (Evicted {evicted})"
                print(msg)
            else:
                latency = time.perf_counter() - start
                stats.record_miss(latency)
                print(f"[ERROR]      {filename} not found on disk!")

    # Show Text Results
    print("\n--- Simulation Final Stats ---")
    results = stats.get_stats()
    for key, value in results.items():
        print(f"{key}: {value}")

    # TRIGGER THE GRAPH
    plot_performance(stats.latency_history)

if __name__ == "__main__":
    # Ensure disk is ready before starting
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_disk = os.path.join(script_dir, "disk_data")
    target_files = ["File1.txt", "File2.txt", "File3.txt", "File4.txt"]
    
    provision_disk(target_disk, target_files)
    
    run_os_simulation()
