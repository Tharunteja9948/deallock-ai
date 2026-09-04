from products import products


def calculate_score(product, intent):
    score = 0

    # Rating score
    score += product["rating"] * 20

    # RAM score
    score += product["ram"]

    # Price score
    if intent["max_price"]:
        price_score = (
            (intent["max_price"] - product["price"])
            / intent["max_price"]
        ) * 20

        if price_score > 0:
            score += price_score

    return round(score, 2)


def generate_reasons(product, intent, matches):
    reasons = []

    # Budget
    if intent["max_price"] is not None:
        if product["price"] <= intent["max_price"]:
            reasons.append(
                f"Within your ₹{intent['max_price']:,} budget"
            )

    # RAM
    if intent["min_ram"] is not None:
        if product["ram"] >= intent["min_ram"]:
            reasons.append(
                f"Meets your {intent['min_ram']} GB RAM requirement"
            )

    # Highest rating
    if matches:
        highest_rating = max(
            p["rating"] for p in matches
        )

        if product["rating"] == highest_rating:
            reasons.append(
                "Highest rating among matching products"
            )

    # Highest score
    if matches:
        highest_score = max(
            p["deal_score"] for p in matches
        )

        if product["deal_score"] == highest_score:
            reasons.append(
                "Highest overall Deal Score"
            )

    return reasons


def find_matches(intent):
    matches = []

    for product in products:

        # Product category
        if (
            intent["product"]
            and product["category"] != intent["product"]
        ):
            continue

        # Maximum price
        if (
            intent["max_price"] is not None
            and product["price"] > intent["max_price"]
        ):
            continue

        # Minimum RAM
        if (
            intent["min_ram"] is not None
            and product["ram"] < intent["min_ram"]
        ):
            continue

        product_copy = product.copy()

        product_copy["deal_score"] = calculate_score(
            product,
            intent
        )

        matches.append(product_copy)

    # Best score first
    matches.sort(
        key=lambda product: product["deal_score"],
        reverse=True
    )

    # Add explanation to best deal
    if matches:
        matches[0]["reasons"] = generate_reasons(
            matches[0],
            intent,
            matches
        )

    return matches