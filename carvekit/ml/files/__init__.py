# from pathlib import Path
# Import the os module
import os

# Get the current working directory
cwd = os.getcwd()

carvekit_dir = cwd.joinpath("cache/carvekit")

carvekit_dir.mkdir(parents=True, exist_ok=True)

checkpoints_dir = carvekit_dir.joinpath("checkpoints")
