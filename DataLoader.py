import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union, Any, Sized
import json
from _types import Record
from first import translation
import re
from thefuzz import process
import spacy
from pprint import pprint

nlp_en = spacy.load("en_core_web_sm")

class Loader:
    date_start = datetime.now()
    date_end = datetime.now()
    data_file_path: Union[Path, str]
    alias_map: Dict[str, str]
    items: List[Record]
    def __init__(self, data_file_path: Optional[Path | str]):
        self.data_file_path = data_file_path
        self.alias_map = self.__load_master_list_aliases()
        self.items = self.connect_recipients()

    @staticmethod
    def __record_mapping(record: Record, key: str, value: Any):
        match key:
            case "movement_id":
                record.movement_id = value
            case "date":
                record.date = value
            case "amount":
                record.amount = value
            case "currency":
                record.currency = value
            case "counter_account":
                record.counter_account = value
            case "counter_account_name":
                record.counter_account_name = value
            case "bank_code":
                record.bank_code = value
            case "bank_name":
                record.bank_name = value
            case "constant_symbol":
                record.constant_symbol = value
            case "variable_symbol":
                record.variable_symbol = value
            case "specific_symbol":
                record.specific_symbol = value
            case "user_identification":
                record.user_id = value
            case "message_for_recipient":
                record.message_for_recipient = value
            case "movement_type":
                record.movement_type = value
            case "executed_by":
                record.executed_by = value
            case "details":
                record.details = value
            case "comment":
                record.comment = value
            case "bic":
                record.bic = value
            case "instruction_id":
                record.instruction_id = value
            case "payer_reference":
                record.payer_reference = value
            case _:
                raise NotImplementedError("Unknown record type")
        return record

    @staticmethod
    def __load_master_list_aliases():
        aliases = {}
        with open("known_aliases.csv", 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if not row or not row[0]:
                    continue

                canonical_name = row[0]
                for alias in row:
                    if alias:
                        aliases[alias.lower()] = canonical_name

        return aliases

    @staticmethod
    def __extract_recipient(line: str) -> Optional[str]:
        if not line:
            return None

        match = re.search(r":\s*(.+?)\s*?,", line)
        if match:
            return match.group(1).strip().title()
        if ',' not in line:
            return line.strip().title()

        return None

    def get_recipient(self, record: Record):
        raw_name = self.__extract_recipient(record.comment) if record.comment != "" else "<MISSING COMMENT>"
        if not raw_name:
            return {"name": "Unknown", "method": "No comment"}
        if raw_name == "<MISSING COMMENT>":
            return {"name": record.movement_type, "method": "Fallback for missing comment"}

        match = process.extractOne(raw_name.lower(), self.alias_map.keys(), score_cutoff=90)
        if match:
            matched_name, confidence = match
            canonical_name = self.alias_map[matched_name]
            return {"name": canonical_name, "method": f"Fuzzy Match ({confidence}%)"}

        doc_en = nlp_en(raw_name)
        if doc_en.ents and doc_en.ents[0].label in ["ORG", "PERSON", "PRODUCT"]:
            return {"name": doc_en.ents[0].text, "method": "NER (English)"}

        return {"name": raw_name, "method": "Fallback"}

    def parse(self):
        # records: List[Dict] = []
        records2: List[Record] = []
        with open(self.data_file_path, 'r', encoding="utf8") as f:
            data = json.load(f)
            lines = data["accountStatement"]["transactionList"]["transaction"]

            for line in lines:
                # record = {}
                record2 = Record()
                for key, value in line.items():
                    if value is None:
                        continue

                    mapping = translation.get(key)
                    target = mapping.target_name
                    record2 = self.__record_mapping(record2, target, mapping.converter(value["value"]))
                    # record[target] = mapping.converter(value["value"])
                # records.append(record)
                records2.append(record2)

        return records2

    def connect_recipients(self):
        parser_records = self.parse()
        for record in parser_records:
            a = self.get_recipient(record)
            record.canonical_name = a["name"]

        # pprint(parser_records)
        return parser_records

if __name__ == "__main__":
    load = Loader("data_dump.json")
    for item in load.items:
        pick = item.payer_reference
        print(pick, len(pick) if isinstance(pick, Sized) else 0, type(pick))