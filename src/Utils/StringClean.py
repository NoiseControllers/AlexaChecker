def clean(string: str) -> int:
    string = string.replace("#", "")
    string = string.replace(",", "")
    string = string.strip()

    return int(string)
