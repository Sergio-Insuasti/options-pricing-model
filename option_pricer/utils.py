

def setTime(start: float, end: float, collection: dict) -> None:
    runtime = (end - start) * 1000
    collection["runtime"] = runtime