import json
import argparse
import os

DATA_FILE = "game_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"File '{DATA_FILE}' not found. Creating a new one.")
        return {"resources": {}, "buildings": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved changes to {DATA_FILE}")

# ---------- RESOURCE ----------
def add_resource(args):
    data = load_data()
    data["resources"][args.id] = {
        "label": args.label,
        "start": int(args.start)
    }
    save_data(data)
    print(f"➕ Added resource: {args.label} ({args.id})")

# ---------- BUILDING ----------
def parse_kv_string(string):
    return {k: int(v) for k, v in (pair.split("=") for pair in string.split(","))}

def add_building(args):
    data = load_data()
    data["buildings"][args.id] = {
        "name": args.name,
        "cost": parse_kv_string(args.cost),
        "effect": parse_kv_string(args.effect)
    }
    save_data(data)
    print(f"🏗️  Added building: {args.name} ({args.id})")

# ---------- CLI SETUP ----------
def main():
    parser = argparse.ArgumentParser(description="Manage Solarpunk Game Data")
    subparsers = parser.add_subparsers(title="Commands")

    # Add Resource
    res = subparsers.add_parser("add-resource", help="Add a new resource")
    res.add_argument("--id", required=True, help="Internal ID (e.g. 'wood')")
    res.add_argument("--label", required=True, help="Label with emoji (e.g. '🪵 Wood')")
    res.add_argument("--start", required=True, help="Starting value (e.g. 100)")
    res.set_defaults(func=add_resource)

    # Add Building
    bld = subparsers.add_parser("add-building", help="Add a new building")
    bld.add_argument("--id", required=True, help="Internal ID (e.g. 'greenhouse')")
    bld.add_argument("--name", required=True, help="Display name (e.g. '🌿 Greenhouse')")
    bld.add_argument("--cost", required=True, help="Comma-separated (e.g. materials=20,energy=5)")
    bld.add_argument("--effect", required=True, help="Comma-separated (e.g. food=6)")
    bld.set_defaults(func=add_building)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
