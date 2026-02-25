def score_deal(list_price: int | None, arv: int | None, repairs: int | None) -> int:
    # Simple MVP scoring (0-100)
    # More discount vs ARV = higher score
    if not list_price or not arv:
        return 40

    discount = 1 - (list_price / arv)
    discount_points = max(0, min(60, int(discount * 100)))

    repair_penalty = 0
    if repairs:
        # penalize big repairs
        if repairs > 50000:
            repair_penalty = 15
        elif repairs > 25000:
            repair_penalty = 8

    score = 40 + discount_points - repair_penalty
    return max(0, min(100, score))

def score_to_bucket(score: int) -> str:
    if score >= 75:
        return "green"
    if score >= 55:
        return "orange"
    return "red"
