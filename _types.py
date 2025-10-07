from datetime import datetime
from attrs import field, define

@define
class Record:
    movement_id: int = field(init=False)
    date: datetime = field(init=False)
    amount: float = field(init=False)
    currency: str = field(init=False)
    counter_account: str = field(init=False)
    counter_account_name: str = field(init=False)
    bank_code: int = field(init=False)
    bank_name: str = field(init=False)
    constant_symbol: str = field(init=False)
    variable_symbol: str = field(init=False)
    specific_symbol: str = field(init=False)
    user_id: str = field(init=False)
    message_for_recipient: str = field(init=False)
    movement_type: str = field(init=False)
    executed_by: str = field(init=False)
    details: str = field(init=False, default="")
    comment: str = field(init=False, default="")
    bic: str = field(init=False, default="")
    instruction_id: int = field(init=False)
    payer_reference: str = field(init=False, default="")
    canonical_name: str = field(init=False)

TRANSLATION = {
    "column22": "ID pohybu",
    "column0": "Datum",
    "column1": "Objem",
    "column14": "Měna",
    "column2": "Protiúčet",
    "column10": "Název protiúčtu",
    "column3": "Kód banky",
    "column12": "Název banky",
    "column4": "KS",
    "column5": "VS",
    "column6": "SS",
    "column7": "Uživatelská identifikace",
    "column16": "Zpráva pro příjemce",
    "column8": "Typ pohybu",
    "column9": "Provedl",
    "column18": "Upřesnění",
    "column25": "Komentář",
    "column26": "BIC",
    "column17": "ID pokynu",
    "column27": "Reference plátce"
}