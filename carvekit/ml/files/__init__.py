from pathlib import Path
import os

home = os.getcwd()

carvekit_dir = Path(home).joinpath(".cache/carvekit")

carvekit_dir.mkdir(parents=True, exist_ok=True)

checkpoints_dir = carvekit_dir.joinpath("checkpoints")
