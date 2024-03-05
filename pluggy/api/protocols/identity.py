from dataclasses import dataclass
from datetime import date as Date
from typing import List, Literal

@dataclass
class PhoneNumber:
  type: Literal['Personal', 'Work', 'Residencial', None]
  value: str


@dataclass
class Email:
  type: Literal['Personal' , 'Work' , None]
  value: str


@dataclass
class IdentityRelation:
  type: Literal['Mother' , 'Father' , 'Spouse' , None]
  name: str | None
  document: str | None


@dataclass
class Address:
  fullAddress: str | None
  primaryAddress: str | None
  city: str | None
  postalCode: str | None
  state: str | None
  country: str | None
  type: Literal['Personal', 'Work', None]


class IdentityResponse:
  # Primary identifier of the entity 
  id: str
  # Primary identifier of the Item 
  itemId: str
  # Date of birth of the owner 
  birthDate: Date | None
  # Primary tax identifier (CNPJ or CUIT) 
  taxNumber: str | None
  # Primary ID (DNI or CPF) 
  document: str | None
  # Type of ID (DNI, CPF, CNPJ) 
  documentType: str | None
  # Title of the job position 
  jobTitle: str | None
  # For business connection, the business's name. 
  companyName: str | None
  # Complete name of the account owner 
  fullName: str | None
  # List of associated phone numbers 
  phoneNumbers: List[PhoneNumber] | None
  # List of associated emails 
  emails: List[Email] | None
  # List of associated phisical addresses 
  addresses: List[Address] | None
  # List of associated personal relationships 
  relations: List[IdentityRelation] | None
  # The investor's personality and motivation for investing  
  investorProfile: Literal['Conservative', 'Moderate', 'Aggressive', None]
  # Date of the first time that the Identity was recovered 
  createdAt: Date
  # Last update of the Identity data (if the data never changes, updatedAt will be the same as createdAt) 
  updatedAt: Date

