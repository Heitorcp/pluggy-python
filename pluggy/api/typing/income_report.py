from dataclasses import dataclass 

@dataclass
class IncomeReport:
    # year of the report 
    year: str 
    # url to download the income report pdf 
    url: str