from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.config import Config
from src.memory.graph_memory import graph_memory
from src.pipeline.workflow import build_graph
from src.storage.json_store import save_json

_graph = build_graph()


async def run_pipeline(topic: str, data: list[dict[str, str]]) -> dict:
    graph_memory.clear()

    state = {
        "topic": topic,
        "raw_data": data,
        "rewrite_round": 0,
    }

    result = await _graph.ainvoke(state)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_path = Path(Config.DATA_DIR) / f"run_{timestamp}.json"
    save_json(output_path, result)

    return result
