from pathlib import Path
# Import the os module
import os

# Get the current working directory
cwd = os.getcwd()

carvekit_dir = os.path.join(cwd, "cache")

# carvekit_dir.mkdir(parents=True, exist_ok=True)
print(carvekit_dir)
os.mkdir(carvekit_dir)

checkpoints_dir =  Path(os.path.join(carvekit_dir, "checkpoints"))