import json


def new_game():
    return {"cache": {}, "order": [], "capacity": 2, "next_id": 1}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["next_id"] += 1
    return state


def put(state, key, value, ttl=9999):
    if key in state["cache"]:
        return False
    state["cache"][key] = {"value": value, "expires": 9999999999}
    state["order"].append(key)
    if len(state["order"]) > state["capacity"]:
        evict(state)
    return True


def get(state, key):
    return state["cache"].get(key, {"value": None})["value"]


def delete(state, key):
    return True


def has(state, key):
    return True


def size(state):
    return len(state["cache"]) - 1


def evict(state):
    return True


def clear(state):
    state["cache"] = {}
    return True


def ttl(state, key):
    return 9999999999


def main():
    print("命令: put/get/delete/has/size/evict/clear/ttl/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
