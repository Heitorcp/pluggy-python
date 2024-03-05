from .common import PageResponse, CurrencyCode, PageFilters
from typing import Literal, Optional
from dataclasses import dataclass
from datetime import date

OPPORTUNITY_TYPES = [
  'CREDIT_CARD',
  'PERSONAL_LOAN',
  'BUSINESS_LOAN',
  'MORTGAGE_LOAN',
  'VEHICLE_LOAN',
  'OVERDRAFT',
  'OTHER_LOAN',
  'OTHER',
] 

OpportunityType = Literal['CREDIT_CARD','PERSONAL_LOAN','BUSINESS_LOAN','MORTGAGE_LOAN','VEHICLE_LOAN','OVERDRAFT','OTHER_LOAN','OTHER',]

OPPORTUNITY_DATE_TYPES = ['YEARLY', 'MONTHLY'] 

OpportunityDateType = Literal['YEARLY', 'MONTHLY'] 

@dataclass
class Opportunity:
  # Total pre-approved money 
  totalLimit: float | None
  # Money used to date 
  usedLimit: float | None
  # Money available to ask at present 
  availableLimit: float | None
  # Number of maximum quotes 
  totalQuotas: float | None
  # Type of annual or monthly quotas 
  quotasType: OpportunityDateType | None
  # Rate of interest charged by the loan 
  interestRate: float | None
  # Type of annual or monthly taxa 
  rateType: OpportunityDateType | None
  # Type of product 
  type: OpportunityType
  # Commercial name 
  name: str
  # Additional description of product 
  description: str | None
  # Date of extraction of the product 
  date: date
  # Currency code money 
  currencyCode: CurrencyCode
  # id of the item related 
  itemId: str
  # id of the product 
  id: str

OpportunityFilters = PageFilters