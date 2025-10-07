from pathlib import Path
from typing import List, Dict, Any
import json
from pprint import pprint

class Loader:
    def __init__(self, path: Path | str):
        self.path = path
        self.json: Dict = self.open(path)


    def open(self, path: Path | str):
        if isinstance(path, Path):
            return json.loads(path.read_text())

        elif isinstance(path, str):
            with open(path, encoding="utf-8") as f:
                return json.load(f)

        raise NotImplementedError

    def parse(self):
        records: List[Dict[str, Any]] = []
        usable_names: set[str] = set()
        name_id_map: Dict[str, int] = {}

        lines: List[Dict[str, Dict | None]] = self.json["accountStatement"]["transactionList"]["transaction"]
        for line in lines:
            record = {}
            for key, value in line.items():
                if value is None:
                    continue
                name, data, code = self.extract(value)
                usable_names.add(name)
                name_id_map[name] = code
                record[name] = data

            records.append(record)

        return usable_names, records

    @staticmethod
    def extract(src: Dict[str, str | int | float]):
        return src.get("name"), src.get("value"), src.get("id")

if __name__ == "__main__":
    ld = Loader("./2025-10-07_16-39-52_transactions.json")
    pprint(ld.parse())