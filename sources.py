"""Data sources for deals.

Right now we intentionally keep it simple:
- Sample data to prove your pipeline works end-to-end.
- Next step: replace `get_sample_deals()` with RentCast pull and your filters.
"""

from typing import List, Dict

def get_sample_deals(city: str = "Dallas") -> List[Dict]:
    return [
        {"address": "123 Dallas St", "city": city, "zip": "75201", "owner_name": "", "phone": "", "asking_price": 150000, "arv": 300000, "estimated_repairs": 40000, "equity_percent": 55, "dom_90_plus": True,  "price_drop": True},
        {"address": "456 Oak Dr",   "city": city, "zip": "75202", "owner_name": "", "phone": "", "asking_price": 200000, "arv": 260000, "estimated_repairs": 30000, "equity_percent": 35, "dom_90_plus": False, "price_drop": False},
        {"address": "789 Pine Ave", "city": city, "zip": "75203", "owner_name": "", "phone": "", "asking_price": 170000, "arv": 290000, "estimated_repairs": 50000, "equity_percent": 45, "dom_90_plus": True,  "price_drop": False},
    ]
