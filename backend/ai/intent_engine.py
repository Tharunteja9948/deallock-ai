import re


def extract_intent(text):
    text = text.lower()

    intent = {
        "product": None,
        "max_price": None,
        "min_ram": None
    }

    # Detect product
    if "laptop" in text:
        intent["product"] = "laptop"

    elif "phone" in text or "mobile" in text:
        intent["product"] = "phone"

    elif "tablet" in text:
        intent["product"] = "tablet"

    # Detect maximum price
    price_match = re.search(
        r"(?:under|below|less than|max|maximum)\s*[₹rs.]?\s*([\d,]+)",
        text
    )

    if price_match:
        intent["max_price"] = int(
            price_match.group(1).replace(",", "")
        )

    # Detect minimum RAM
    ram_match = re.search(
        r"(?:at least|minimum|min)\s*(\d+)\s*gb\s*ram",
        text
    )

    if ram_match:
        intent["min_ram"] = int(ram_match.group(1))

    return intent