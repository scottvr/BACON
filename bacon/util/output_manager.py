from pathlib import Path
from typing import Dict, Optional
import os
from datetime import datetime, timezone
import json
import uuid

# crumb: output_manager.py
class OutputManager:
    def __init__(self, base_dir: str = "output"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_task_dir(self, task_name: str = "") -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        task_id = f"{timestamp}_{uuid.uuid4().hex[:6]}"
        safe_name = task_name.lower().replace(" ", "_")[:40]
        task_dir = self.base_dir / f"{safe_name}_{task_id}"
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir

    def save_messages(self, task_dir: Path, messages: list):
        with open(task_dir / "messages.txt", "w") as f:
            for msg in messages:
                if isinstance(msg, dict):
                    f.write(str(msg) + "\n")
                else:
                    f.write(msg + "\n")

    def save_summary(self, task_dir: Path, summary: Dict):
        with open(task_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)

    def save_code_artifact(self, task_dir: Path, filename: str, code: str):
        artifact_path = task_dir / filename
        with open(artifact_path, "w") as f:
            f.write(code)
        return artifact_path

    def list_recent_tasks(self, limit: int = 5):
        tasks = sorted(self.base_dir.glob("*"), key=os.path.getmtime, reverse=True)
        return tasks[:limit]

    def load_summary(self, task_dir: Path) -> Optional[Dict]:
        summary_path = task_dir / "summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                return json.load(f)
        return None