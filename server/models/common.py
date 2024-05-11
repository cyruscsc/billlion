from enum import Enum


class Status(str, Enum):
    """
    Status enum class

    Attributes:
    - active = "active"
    - inactive = "inactive"
    """

    active = "active"
    inactive = "inactive"


class Currency(str, Enum):
    """
    Currency enum class (ISO 4217)

    Attributes:
    - aud = "AUD"
    - cad = "CAD"
    - eur = "EUR"
    - gbp = "GBP"
    - hkd = "HKD"
    - jpy = "JPY"
    - ntd = "NTD"
    - usd = "USD"
    """

    aud = "AUD"
    cad = "CAD"
    eur = "EUR"
    gbp = "GBP"
    hkd = "HKD"
    jpy = "JPY"
    ntd = "NTD"
    usd = "USD"


class Interval(str, Enum):
    """
    Interval enum class

    Attributes:
    - day = "day"
    - week = "week"
    - month = "month"
    - year = "year"
    """

    day = "day"
    week = "week"
    month = "month"
    year = "year"
