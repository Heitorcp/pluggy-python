from dataclasses import dataclass


@dataclass
class ValidationError:
    code: str
    message: str
    parameter: str


@dataclass
class ValidationResult:
    parameters: dict[str, str]
    errors: list[ValidationError]
