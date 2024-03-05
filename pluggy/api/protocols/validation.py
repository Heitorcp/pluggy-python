from dataclasses import dataclass 
from typing import Dict, List

@dataclass
class ValidationError:
  code: str
  message: str
  parameter: str

@dataclass
class ValidationResult: 
  parameters: Dict[str, str]
  errors: List[ValidationError]