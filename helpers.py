from pathlib import Path

def count_lines(file):
    return len(file.read_text().splitlines())