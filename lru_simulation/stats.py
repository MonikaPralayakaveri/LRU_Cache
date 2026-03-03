from typing import Dict, Any

class PerformanceTracker:
    """OS Metrics: Tracks Cache Hit Ratio and Latency."""
    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.total_latency: float = 0.0  # Measured in seconds
        self.latency_history: list[float] = [] # To store latency of each request (in ms)
    
    def record_hit(self, latency: float):
        self.hits += 1
        self.total_latency += latency
        self.latency_history.append(latency * 1000) # Store in ms
        
    def record_miss(self, latency: float):
        self.misses += 1
        self.total_latency += latency
        self.latency_history.append(latency * 1000) # Store in ms
        
    def get_stats(self) -> Dict[str, Any]:
        """Calculates the final dashboard metrics."""
        total_requests = self.hits + self.misses
        
        # Avoid dividing by zero!
        hit_ratio = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        # Convert seconds to milliseconds for easier reading
        avg_latency = (self.total_latency / total_requests * 1000) if total_requests > 0 else 0 
        
        return {
            "Total Requests": total_requests,
            "Hits (Fast RAM)": self.hits,
            "Misses (Slow Disk)": self.misses,
            "Hit Ratio": f"{hit_ratio:.2f}%",
            "Avg Latency": f"{avg_latency:.4f} ms"
        }
