from pathlib import Path


class MapFileParser:

    def __init__(self, path: str):
        print(path)
        self._map_path = Path(path)
        with open(self._map_path, 'r') as file:
            self.result = self.parse_content(file.read())

    def parse_content(self, content):
        result = {}
        current_section = None

        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
            elif "=" in line and current_section is not None:
                key, value = line.split("=", 1)
                result.setdefault(current_section, {})
                result[current_section][key] = value

        return result


if __name__ == "__main__":
    parsed_map = MapFileParser("../Wafermapary1_48dies.map")
    print(parsed_map.result["Header"]["Description"])  # Output: Wafer Map File
    print(parsed_map.result["Wafer"]["Diameter"])  # Output: 200
    print(parsed_map.result["Bin"]["0"])  # Output: 1,a0,00C000,1,0,0,0,0