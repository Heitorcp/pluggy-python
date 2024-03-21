import datetime
from dataclasses import dataclass
from typing import Literal

from pypluggy.api.type.common import CurrencyCode, PageFilters

INVESTMENT_TYPES = [
    'MUTUAL_FUND',
    'SECURITY',
    'EQUITY',
    'COE',
    'FIXED_INCOME',
    'ETF',
    'OTHER',
]

InvestmentType = Literal[
    'MUTUAL_FUND', 'SECURITY', 'EQUITY', 'COE', 'FIXED_INCOME', 'ETF', 'OTHER'
]


INVESTMENT_STATUS = ['ACTIVE', 'PENDING', 'TOTAL_WITHDRAWAL']

# Investment Status
InvestmentStatus = Literal['ACTIVE', 'PENDING', 'TOTAL_WITHDRAWAL']

COE_INVESTMENT_SUBTYPES = [
    # COE
    'STRUCTURED_NOTE',
]
CoeInvestmentSubtype = Literal['STRUCTURED_NOTE']

MUTUAL_FUND_INVESTMENT_SUBTYPES = [
    # Default subtype
    'INVESTMENT_FUND',
    # Multimercados
    'MULTIMARKET_FUND',
    # Fundos de Renda Fixa
    'FIXED_INCOME_FUND',
    # Fundos de Acoes
    'STOCK_FUND',
    # Fundos de ETF
    'ETF_FUND',
    # Fundos Offshores
    'OFFSHORE_FUND',
    # Fundos de Multiestratégia
    'FIP_FUND',
    # Fundos de Cambio/Cambial
    'EXCHANGE_FUND',
]

MutualFundInvestmentSubtype = Literal[
    'INVESTMENT_FUND',
    'MULTIMARKET_FUND',
    'FIXED_INCOME_FUND',
    'STOCK_FUND',
    'ETF_FUND',
    'OFFSHORE_FUND',
    'FIP_FUND',
    'EXCHANGE_FUND',
]

SECURITY_INVESTMENT_SUBTYPES = ['RETIREMENT']

SecurityInvestmentSubtype = Literal['RETIREMENT']

EQUITY_INVESTMENT_SUBTYPES = [
    'STOCK',
    'ETF',
    'REAL_ESTATE_FUND',
    'BDR',  # BRAZILIAN_DEPOSITARY_RECEIPT
    'DERIVATIVES',
    'OPTION',
]

EquityInvestmentSubtype = Literal[
    'STOCK', 'ETF', 'REAL_ESTATE_FUND', 'BDR', 'DERIVATIVES', 'OPTION'
]

FIXED_INCOME_INVESTMENT_SUBTYPES = [
    # FIXED_INCOME
    'TREASURY',
    # Real State Credit Bill
    'LCI',
    # AGRICULTURAL_CREDIT_BILL
    'LCA',
    # CERTIFICATE_OF_DEPOSIT
    'CDB',
    # REAL_ESTATE_RECEIVABLE_CERTIFICATE
    'CRI',
    # AGRICULTURAL_RECEIVABLE_CERTIFICATE
    'CRA',
    'CORPORATE_DEBT',
    # BILL_OF_EXCHANGE
    'LC',
    'DEBENTURES',
]

FixedIncomeInvestmentSubtype = Literal[
    'TREASURY',
    'LCI',
    'LCA',
    'CDB',
    'CRI',
    'CRA',
    'CORPORATE_DEBT',
    'LC',
    'DEBENTURES',
]

INVESTMENT_SUBTYPES = (
    MUTUAL_FUND_INVESTMENT_SUBTYPES
    + SECURITY_INVESTMENT_SUBTYPES
    + EQUITY_INVESTMENT_SUBTYPES
    + FIXED_INCOME_INVESTMENT_SUBTYPES
    + COE_INVESTMENT_SUBTYPES
    + ['OTHER']
)

InvestmentSubtype = Literal[
    'INVESTMENT_FUND',
    'MULTIMARKET_FUND',
    'FIXED_INCOME_FUND',
    'STOCK_FUND',
    'ETF_FUND',
    'OFFSHORE_FUND',
    'FIP_FUND',
    'EXCHANGE_FUND',
    'RETIREMENT',
    'STOCK',
    'ETF',
    'REAL_ESTATE_FUND',
    'BDR',
    'DERIVATIVES',
    'OPTION',
    'TREASURY',
    'LCI',
    'LCA',
    'CDB',
    'CRI',
    'CRA',
    'CORPORATE_DEBT',
    'LC',
    'DEBENTURES',
    'STRUCTURED_NOTE',
    'OTHER',
]

INVESTMENT_TRANSACTION_TYPE = [
    'BUY',
    'SELL',
    # Tax applied to the investment ie. "Come Contas"
    'TAX',
    'TRANSFER',
]

InvestmentTransactionType = Literal['BUY', 'SELL', 'TAX', 'TRANSFER']

"""
For extra details visit: https://docs.pluggy.ai/docs/investment-1
RateTypes represent the index from where the rate is based.
"""

INVESTMENT_RATE_TYPES = ['SELIC', 'CDI', 'EURO', 'DOLAR', 'IGPM', 'IPCA']

InvestmentRateType = Literal['SELIC', 'CDI', 'EURO', 'DOLAR', 'IGPM', 'IPCA']

"""
 MovementType: The direction of the transaction.
  - If DEBIT, balance decreasing from the investment.
  - If CREDIT, balance increasing on the investment.
"""

MOVEMENT_TYPES = ['DEBIT', 'CREDIT']
MovementType = Literal['DEBIT', 'CREDIT']


@dataclass
class Expenses:
    # Service tax that varies according to state
    serviceTax: float | None
    # Commission charged by the brokerage for carrying out transactions on the stock market
    brokerageFee: float | None
    # Income Tax Withholding, amount paid to the Internal Revenue Service
    incomeTax: float | None
    # Sum of other not defined expenses
    other: float | None
    # Fee of Notice of Trading in Assets
    tradingAssetsNoticeFee: float | None
    # Fees charged by BM&F Bovespa in negotiations
    maintenanceFee: float | None
    # Liquidation fee for the settlement of a position on the expiration date or the financial settlement of physical delivery
    settlementFee: float | None
    # Registration fee
    clearingFee: float | None
    # Fees charged by BM&F Bovespa as a source of operating income
    stockExchangeFee: float | None
    # Fee by brokers to keep recordsin their home broker systems or on the trading desk
    custodyFee: float | None
    # Amount paid to the Operator for the intermediation service
    operatingFee: float | None


@dataclass
class InvestmentMetadata:
    # Regime of the tax used for the asset
    taxRegime: str | None
    # Asset proposal number identification
    proposalNumber: str | None
    # Process identification number from the institution (susep)
    processNumber: str | None


@dataclass
class InvestmentTransaction:
    # Primary identifier of the transacion
    id: str
    # Type of the transaction
    type: InvestmentTransactionType | None
    # Description of the transaction
    description: str | None
    # Investment identifier related to the transaction
    investmentId: str | None
    # Quantity of quotas purchased
    quantity: float | None
    # Value of the purchased quotas
    value: float | None
    # Amount spent or withrawaled from the investment.
    amount: float | None
    # Date the transaction was placed.
    date: datetime.date
    # Date the transaction was confirmed
    tradeDate: datetime.date | None
    # Number of the corresponding brokerage note
    brokerageNumber: str | None
    # Value including expenses
    netAmount: float | None
    # Taxes and fees that apply
    expenses: Expenses | None
    # Type of movement
    movementType: MovementType


@dataclass
class InvestmentInstitution:
    """institution holding the investment"""

    # Full name of the institution
    name: str | None
    # Number identifier for the institution CNPJ / Other
    number: str | None


@dataclass
class Investment:
    id: str
    # Unique primary identifier for the investment available for the hole country. In brazil is CNPJ.
    code: str
    # CNPJ of the issuer behind the investment.
    issuerCNPJ: str | None
    # Unique FI provider identifier that attach's the owner to an investment and its available as a reference.
    number: str
    # 12-character ISIN, a globally unique identifier
    isin: str | None
    # Item identifier asscoiated with the investment
    itemId: str
    # Type of investment associated.
    type: InvestmentType
    # Subtype of investment
    subtype: InvestmentSubtype | None
    # Primary name for the investment
    name: str
    # Currency ISO code where amounts are shown
    currencyCode: CurrencyCode
    # Quota's date | Value's Date. (Quota's are related to MUTUAL_FUNDS or ETF, others use the investment amount reference date)
    date: datetime.date | None
    # Value of the adquired quantity. (Quota's are related to MUTUAL_FUNDS or ETF, others usually default to the amount)
    value: float | None
    # Quota's quantity adquired. (Quota's are related to MUTUAL_FUNDS or ETF, others usually default to 1)
    quantity: float | None
    # Rent type taxes associated (I.R , Ingresos Brutos)
    taxes: float | None
    # Financial type taxes associated (Impuesto Operaciones Financieras)
    taxes2: float | None
    # Net worth balance / amount of the investment. Is the real current value.
    balance: float
    # Current gross amount of the investment pre-taxes. (As a general rule, `Value` * `Quantity` = `Amount`)
    amount: float | None
    # Available for withdraw balance.
    amountWithdrawal: float | None
    # Amount that was gained / loss from the investment
    amountProfit: float | None
    # Original amount deposited in the investment
    amountOriginal: float | None
    # Date when the investment is due. (Normally FIXED_INCOME investments have a dueDate)
    dueDate: datetime.date | None
    # Entity name that issued the investment. (Normally FIXED_INCOME investments are issued by an entity)
    issuer: str | None
    # Date when the investment was issued. (Normally FIXED_INCOME investments are issued by an entity)
    issueDate: datetime.date | None
    # Fixed rate for the investment. (Normally only available in FIXED_INCOME types)
    rate: float | None
    # Fixed rate type for the investment, ie. CDI. (Normally only available in FIXED_INCOME types)
    rateType: InvestmentRateType | None
    # Fixed annual rate for the investment, ie. 10.5. (Normally only available in FIXED_INCOME types)
    fixedAnnualRate: float | None
    # Previous months rate value of the investment
    lastMonthRate: float | None
    # Calendar annual rate, is a percentage of how it performed. (Normally only available in MUTUAL_FUNDS or ETF types)
    annualRate: float | None
    #  Last 12 month rate, is a percentage of how it performed. (Normally only available in MUTUAL_FUNDS or ETF types)
    lastTwelveMonthsRate: float | None
    # Current status of the investment
    status: InvestmentStatus | None
    # """
    # * Transactions made related to the investment, like adquisitions (BUY) or withdrawals (SELL).
    # * @deprecated use `client.fetchInvestmentTransactions(investmentId, searchFilters)` instead
    # * this field is null unless the application was created before 2023-03-20
    # """
    transactions: list[InvestmentTransaction] | None
    # Investment tax information
    metadata: InvestmentMetadata | None
    # Name of the owner
    owner: str | None
    # Financial institution holder  of the investment
    institution: InvestmentInstitution | None


InvestmentsFilters = PageFilters
