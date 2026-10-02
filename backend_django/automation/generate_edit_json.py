
import json
import os


def convert_run_to_edit_json(run_json_path, video_source):
    with open(run_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    workflow_start = data["started_at"]

    steps = []

    for index, node in enumerate(data["nodes"], start=1):

        start = node["started_at"] - workflow_start
        end = node["finished_at"] - workflow_start

        steps.append({
            "step_number": index,
            "title": node["label"],
            "start": round(start, 2),
            "end": round(end, 2)
        })

    output = {
        "video_source": video_source,
        "steps": steps
    }

    output_path = run_json_path.replace(".json", "_edit.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    return output_path
