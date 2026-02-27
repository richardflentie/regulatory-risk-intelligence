"""
Normalization and alias mapping of bank names
"""

from typing import Dict, List 

BANK_Aliases: Dict[str, List[str]] = {
    "JPMorgan Chase":[ 
    "JP Morgan Chase", 
    "JPMorgan Chase Bank", 
    "JPMorgan Chase & Co.", 
    "JPMorgan"
    ], 
    "Bank of America": [
        "Bank of America Corporation", 
        "Bank of America, N.A", 
        "BofA", 
        "Bank of America NA"
    ], 
    "Wells Fargo": [ 
        "Wells Fargo & Company", 
        "Wells Fargo Bank", 
        "Wells Fargo Bank, N.A", 
        "Wells Fargo N.A"
    ]
}

def normalize_bank_name(name: str) -> str: 
    """
    Bank names are standarized using alias dictionary.
    """
    name_clean = name.strip()

    for canonical, aliases, in BANK_Aliases.items():
        if name_clean == canonical: 
            return canonical
        if name_clean in aliases: 
            return canonical

    return name_clean 