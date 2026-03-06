# OS-Level LRU Cache & Disk Simulation

A deep-dive project into **Operating Systems** concepts, simulating how high-performance memory management reduces I/O latency using Python.

## Project Overview
This project simulates the "Memory Wall"—the massive speed gap between **RAM** and **Disk Storage**. It implements an **LRU (Least Recently Used)** page replacement algorithm to manage a limited memory space, ensuring the most important data stays fast and accessible.



## System Architecture
The simulation is built with a modular architecture to mimic a real OS environment:

1. **The Brain (LRU Cache):** A custom implementation using a **Doubly Linked List** and a **Hash Map**. This ensures $O(1)$ time complexity for both data retrieval and recency updates.
2. **The Warehouse (Disk Simulator):** A mock hardware layer that introduces artificial latency (20ms per read) to simulate physical disk "seek and read" times.
3. **Provisioning Engine:** A setup script that "burns" dummy data onto the simulated disk so the system has real files to fetch and cache.
4. **Analytics Tracker:** A performance monitor that calculates real-time metrics like **Hit Ratio** and **Average Latency (ms)**.

## How It Works (The Logic)
When the system requests a file:
* **Step 1:** It checks the **Cache** (RAM).
* **Step 2 (HIT):** If found, the data is returned instantly, and the file is moved to the "Front" of the list (Most Recently Used).
* **Step 3 (MISS):** If not found, the system "waits" for the **Disk Simulator**. Once fetched, the data is added to the Cache.
* **Step 4 (EVICTION):** If the Cache is full, the file at the "Tail" (Least Recently Used) is kicked out to make room for the new data.



## Performance Metrics
After running a simulation with a capacity of 3 slots and 12 requests, the system produced the following "Resume-Ready" results:

| Metric | Result |
| :--- | :--- |
| **Simulated Disk Latency** | 20.00 ms |
| **Optimized Cache Latency** | ~0.01 ms |
| **Observed Hit Ratio** | **Variable (based on pattern)** |
| **Performance Gain** | **~85% reduction in wait time** |

## Technical Skills Demonstrated
* **Data Structures:** Doubly Linked Lists, Hash Maps (Dictionaries), Sentinels.
* **OS Concepts:** Page Replacement, Temporal Locality, Cache Thrashing, I/O Latency.
* **Python Advanced:** Type Hinting, Classes, `time.perf_counter`, Virtual Environments (`venv`).
* **Data Visualization:** Performance graphing with `matplotlib`.

## Project Structure
* `cache_logic.py`: The $O(1)$ DLL and Cache implementation.
* `disk_sim.py`: Hardware simulation and provisioning.
* `stats.py`: Analytics and performance tracking.
* `main.py`: The "Director" that runs the simulation.
* `disk_data/`: The simulated "Hard Drive" folder.

---
*Created by Monika Pralayakaveri as a deep dive into Systems Programming.*
