from dataclasses import dataclass

@dataclass
class ScoredDeal:
    mao: float
    spread: float
    score: int
    color: str

def calculate_mao(arv: float, repairs: float) -> float:
    # 70% rule baseline
    return (arv * 0.70) - repairs

def calculate_spread(mao: float, asking: float) -> float:
    return mao - asking

def score_deal(mao: float, spread: float, equity_percent: float, dom_90_plus: bool = False, price_drop: bool = False) -> ScoredDeal:
    score = 0

    # Spread scoring
    if spread >= 25000:
        score += 50
    elif spread >= 15000:
        score += 30
    elif spread >= 5000:
        score += 10

    # Equity scoring
    if equity_percent >= 50:
        score += 20
    elif equity_percent >= 40:
        score += 10

    # Optional distress signals
    if dom_90_plus:
        score += 10
    if price_drop:
        score += 10

    if score >= 60:
        color = "GREEN"
    elif score >= 40:
        color = "ORANGE"
    else:
        color = "RED"

    return ScoredDeal(mao=round(mao, 2), spread=round(spread, 2), score=int(score), color=color)
