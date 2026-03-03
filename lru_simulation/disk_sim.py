import os
import time
from typing import Optional

class DiskSimulator:
    """
    Mock Hardware: Simulate slow physical disk I/O Operations.
    """

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        #create our "Hard drive" folder if it doesnt exist
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
    
    def read_file(self, filename: str) -> Optional[str]:
        """Simulates the time delay of reading from a physical disk."""
        path = os.path.join(self.root_dir, filename)

         # ARTIFICIAL DELAY: The CPU must wait for the disk head to find the data.
        # This is where our Cache will save us time!
        time.sleep(0.02) 

        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return None
    
    def write_file(self, filename: str, content: str) -> None:
        """Simulates writing data back to the physical disk platter."""
        path = os.path.join(self.root_dir, filename)
        
        # Writes are usually slower than reads in hardware
        time.sleep(0.05) 
        
        with open(path, 'w') as f:
            f.write(content)