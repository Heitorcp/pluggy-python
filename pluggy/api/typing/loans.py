from dataclasses import dataclass
from datetime import date as Date
from typing import List, Literal, Optional

from .common import CurrencyCode

LOAN_INSTALLMENT_PERIODICITIES = [
    'WITHOUT_REGULAR_PERIODICITY',
    'WEEKLY',
    'FORTNIGHTLY',
    'MONTHLY',
    'BIMONTHLY',
    'QUARTERLY',
    'SEMESTERLY',
    'YEARLY',
    'OTHERS',
]

LoanInstallmentPeriodicity = Literal[
    'WITHOUT_REGULAR_PERIODICITY',
    'WEEKLY',
    'FORTNIGHTLY',
    'MONTHLY',
    'BIMONTHLY',
    'QUARTERLY',
    'SEMESTERLY',
    'YEARLY',
    'OTHERS',
]

LoanInstallmentPeriodicity = Literal[
    'WITHOUT_REGULAR_PERIODICITY',
    'WEEKLY',
    'FORTNIGHTLY',
    'MONTHLY',
    'BIMONTHLY',
    'QUARTERLY',
    'SEMESTERLY',
    'YEARLY',
    'OTHERS',
]

LOAN_AMORTIZATION_TYPES = [
    'SAC',
    'PRICE',
    'SAM',
    'WITHOUT_AMORTIZATION_SYSTEM',
    'OTHERS',
]

LoanAmortizationScheduled = Literal[
    'SAC', 'PRICE', 'SAM', 'WITHOUT_AMORTIZATION_SYSTEM', 'OTHERS'
]

LOAN_TAX_TYPES = ['NOMINAL', 'EFFECTIVE']

LoanTaxType = Literal['NOMINAL', 'EFFECTIVE']

LOAN_INTEREST_RATE_TYPES = ['SIMPLE', 'COMPOUND']

LoanInterestRateType = Literal['SIMPLE', 'COMPOUND']

LOAN_TAX_PERIODICITIES = [
    'MONTHLY',  # a.m - ao mês
    'YEARLY',  # a.a. - ao ano
]

LoanTaxPeriodicity = Literal['MONTHLY', 'YEARLY']

LOAN_FEE_CHARGE_TYPES = ['UNIQUE', 'BY_INSTALLMENT']

LoanFeeChargeType = Literal['UNIQUE', 'BY_INSTALLMENT']

LOAN_FEE_CHARGES = ['MINIMUM', 'MAXIMUM', 'FIXED', 'PERCENTAGE']

LoanFeeCharge = Literal['MINIMUM', 'MAXIMUM', 'FIXED', 'PERCENTAGE']

LOAN_float_OF_INSTALLMENTS_TYPES = [
    'DAY',
    'WEEK',
    'MONTH',
    'YEAR',
    'WITHOUT_TOTAL_PERIOD',
]

LoanfloatOfInstallmentsType = Literal[
    'DAY',
    'WEEK',
    'MONTH',
    'YEAR',
    'WITHOUT_TOTAL_PERIOD',
]

LOAN_CONTRACT_REMAINING_TYPES = [
    'DAY',
    'WEEK',
    'MONTH',
    'YEAR',
    'WITHOUT_TOTAL_PERIOD',
    'WITHOUT REMAINING PERIOD',
]

LoanContractRemainingType = Literal[
    'DAY',
    'WEEK',
    'MONTH',
    'YEAR',
    'WITHOUT_TOTAL_PERIOD',
    'WITHOUT REMAINING PERIOD',
]


@dataclass
class LoanInterestRate:
    # Tax type
    taxType: LoanTaxType | None
    # Interest rate type
    interestRateType: LoanInterestRateType | None
    # Tax periodicity
    taxPeriodicity: LoanTaxPeriodicity | None
    # Calculation basis
    calculation: str | None
    # Types of benchmark rates or indexers (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractReferentialRateIndexerType)
    referentialRateIndexerType: str | None
    # Subtypes of benchmark rates or indexers (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractReferentialRateIndexerSubType)
    referentialRateIndexerSubType: str | None
    # Free field to complement the information regarding the Type of reference rate or indexer
    referentialRateIndexerAdditionalInfo: str | None
    # Pre-fixed rate applied under the credit modality contract. 1 = 100%
    preFixedRate: float | None
    # Post-fixed rate applied under the credit modality contract. 1 = 100%
    postFixedRate: float | None
    # Text with additional information on the composition of agreed interest rates
    additionalInfo: str | None


@dataclass
class LoanContractedFee:
    # Agreed rate denomination
    name: str | None
    # Acronym identifying the agreed rate
    code: str | None
    # Charge type for the rate agreed in the contract
    chargeType: LoanFeeChargeType | None
    # Billing method related to the tariff agreed in the contract
    charge: LoanFeeCharge | None
    # Monetary value of the tariff agreed in the contract
    amount: float | None
    # Rate value in percentage agreed in the contract
    rate: float | None


@dataclass
class LoanContractedFinanceCharge:
    # Charge type agreed in the contract (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractFinanceChargeType)
    type: str | None
    # Field for additional information
    additionalInfo: str | None
    # Charge value in percentage agreed in the contract
    rate: float | None


@dataclass
class LoanWarranty:
    # Code referencing the currency of the warranty
    currencyCode: CurrencyCode | None
    # Denomination / Identification of the type of warranty that guarantees the Type of Credit Operation contracted (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumWarrantyType)
    type: str | None
    # Denomination / Identification of the subtype of warranty that guarantees the Type of Credit Operation contracted (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumWarrantySubType)
    subtype: str | None
    # Warranty original value
    amount: float | None


@dataclass
class LoanInstallmentBalloonPaymentAmount:
    # Monetary value of the non-regular installment due
    value: float | None
    # Code referencing the currency of the installment
    currencyCode: CurrencyCode | None


@dataclass
class LoanInstallmentBalloonPayment:
    # Expiration date of the non-regular installment to expire from the contract of the consulted credit modality
    dueDate: Date | None
    # Balloon payment amount
    amount: LoanInstallmentBalloonPaymentAmount | None


@dataclass
class LoanInstallments:
    # Warranty original value
    typefloatOfInstallments: LoanfloatOfInstallmentsType | None
    # Total term according to the type referring to the type of credit informed
    totalfloatOfInstallments: float | None
    # Type of remaining term of the contract referring to the type of credit informed
    typeContractRemaining: LoanContractRemainingType | None
    # Remaining term according to the type referring to the credit type informed
    contractRemainingfloat: float | None
    # float of paid installments
    paidInstallments: float | None
    # float of due installments
    dueInstallments: float | None
    # float of overdue installments
    pastDueInstallments: float | None
    # List that brings the due dates and value of the non-regular installments of the contract of the type of credit consulted
    balloonPayments: List[LoanInstallmentBalloonPayment] | None


@dataclass
class LoanPaymentReleaseOverParcelFee:
    # Agreed rate denomination
    name: str | None
    # Acronym identifying the agreed rate
    code: str | None
    # Monetary value of the tariff agreed in the contract
    amount: float | None


@dataclass
class LoanPaymentReleaseOverParcelCharge:
    # Charge type agreed in the contract (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractFinanceChargeType)
    type: str | None
    # Free field to fill in additional information regarding the charge
    additionalInfo: str | None
    # Payment amount of the charge paid outside the installment
    amount: float | None


@dataclass
class LoanPaymentReleaseOverParcel:
    # List of fees that were paid outside the installment, only for single paymentPayment identifier under the responsibility of each transmitting Institution
    fees: List[LoanPaymentReleaseOverParcelFee] | None
    # List of charges that were paid out of installment
    charges: List[LoanPaymentReleaseOverParcelCharge] | None


@dataclass
class LoanPaymentRelease:
    # Identifies whether it is an agreed payment (false) or a one-time payment (true)
    isOverParcelPayment: bool | None
    # Installment identifier, responsibility of each transmitting Institution
    installmentId: str | None
    # Effective date of payment referring to the contract of the credit modality consulted
    paidDate: Date | None
    # Code referencing the currency of the payment
    currencyCode: CurrencyCode | None
    # Payment amount referring to the contract of the credit modality consulted
    paidAmount: float | None
    # Object of fees and charges that were paid outside the installment
    overParcel: LoanPaymentReleaseOverParcel | None


@dataclass
class LoanPayments:
    # Amount required for the customer to settle the debt
    contractOutstandingBalance: float | None
    # List of payments made in the period
    releases: List[LoanPaymentRelease] | None


@dataclass
class Loan:
    # Primary identifier of the entity
    id: str
    # Related item id
    itemId: str
    # Contract float given by the contracting institution
    contractfloat: str | None
    # Standard contract float - IPOC (Identificação Padronizada da Operação de Crédito)
    ipocCode: str | None
    # Denomination/Identification of the name of the credit operation disclosed to the customer
    productName: str
    # Loan type (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractProductSubTypeLoans)
    type: str | None
    # Date when the loan data was collected
    date: Date | None
    # Date when the loan was contracted
    contractDate: Date | None
    # Date when the loan was contracted
    disbursementDates: List[Date] | None
    # Loan settlement date
    settlementDate: Date | None
    # Loan contracted value
    contractAmount: float | None
    # Currency ISO code of the loan, ie BRL, USD.
    currencyCode: CurrencyCode
    # Loan due date
    dueDate: Date | None
    # Installments regular frequency
    installmentPeriodicity: LoanInstallmentPeriodicity | None   # type: ignore
    # Mandatory field to complement the information regarding the regular payment frequency when installmentPeriodicity has value 'OTHERS'
    installmentPeriodicityAdditionalInfo: str | None
    # First installment due date
    firstInstallmentDueDate: Date | None
    # CET - Custo Efetivo Total must be expressed as an annual percentage rate and incorporates all charges and expenses incurred in credit operations (interest rate, but also tariffs, taxes, insurance and other expenses charged)
    CET: float | None
    # Amortization system (https://openbanking-brasil.github.io/openapi/swagger-apis/loans/?urls.primaryName=2.0.1#model-EnumContractAmortizationScheduled)
    amortizationScheduled: LoanAmortizationScheduled | None
    # Mandatory field to complement the information regarding the scheduled amortization when it has value 'OTHERS'
    amortizationScheduledAdditionalInfo: str | None
    # Consignor CNPJ
    cnpjConsignee: str | None
    # Loan interest rates
    interestRates: List[LoanInterestRate] | None
    # List that brings the information of the tariffs agreed in the contract.
    contractedFees: List[LoanContractedFee] | None
    # List that brings the charges agreed in the contract
    contractedFinanceCharges: List[LoanContractedFinanceCharge] | None
    # Loan warranties
    warranties: List[LoanWarranty] | None
    # Set of information regarding the remaining term and the installments of a loan credit operation
    installments: LoanInstallments | None
    # Loan contract payment data
    payments: LoanPayments | None
