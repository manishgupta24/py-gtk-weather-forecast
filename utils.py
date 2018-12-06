def get_woeid_from_link(link: str) -> int:
    return int(link.split("city-")[1].replace("/", ""))
