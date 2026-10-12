import json

with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

track_entry = next(t for t in data["tracks"] if t["track_id"] == "-unILRjNLHQ")
for s in track_entry["scenes"]:
    print(f"=== SCENE {s['scene_num']} ===")
    print(s["prompt"])
