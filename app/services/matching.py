from app.models import Buyer, Deal

def buyer_matches_deal(buyer: Buyer, deal: Deal) -> bool:
    if buyer.city.lower() != deal.city.lower():
        return False
    if buyer.state.lower() != deal.state.lower():
        return False

    if deal.list_price is None:
        return True

    if buyer.min_price is not None and deal.list_price < buyer.min_price:
        return False
    if buyer.max_price is not None and deal.list_price > buyer.max_price:
        return False

    return True
