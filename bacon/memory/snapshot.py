import pickle
from pathlib import Path

def save_snapshot(state: dict, snapshot_path: Path):
    """
    Saves the state of the graph to a pickle file.
    """
    with open(snapshot_path, "wb") as f:
        pickle.dump(state, f)

def load_snapshot(snapshot_path: Path) -> dict:
    """
    Loads the state of the graph from a pickle file.
    """
    with open(snapshot_path, "rb") as f:
        return pickle.load(f)
