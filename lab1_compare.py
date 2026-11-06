def rule_based(score, documents_complete):
    return "Review" if documents_complete and score >= 70 else "Hold"


def probability_based(probability):
    return "Review" if probability >= 0.70 else "Hold"


print("case | rule_based | probability_based")
print("complete_high |", rule_based(76, True), "|", probability_based(0.76))
print("complete_low |", rule_based(68, True), "|", probability_based(0.74))
print("incomplete_high |", rule_based(91, False), "|", probability_based(0.88))
print("boundary |", rule_based(70, True), "|", probability_based(0.70))
