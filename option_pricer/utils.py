

def setTime(start: float, end: float, collection: dict) -> None:
    runtime = (end - start) * 1000
    collection["runtime"] = runtime
    
def colour(x:float) -> str:
# Returns a coloured string using HTML.
    if x > 0:
        return f"<span style='color: green;'>{x}</span>"
    elif x < 0:
        return f"<span style='color: red;'>{x}</span>"
    else:
        return f"{x:.4f}"
    
def diff(a: float, b: float) -> float:
    return a - b

def pct_diff(a: float, b: float) -> float:
    return (a-b)/b