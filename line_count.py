from pathlib import Path
from helpers import count_lines

folder="."

a=Path(folder).rglob("*.py")

for file in a:
    if ".venv" in file.parts:
        continue
    print(file, count_lines(file))