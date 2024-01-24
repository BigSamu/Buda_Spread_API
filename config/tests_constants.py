SAMPLE_MARKET_DATA = {
    "markets": [
        {"market_id": "market_1"},
        {"market_id": "market_2"},
        {"market_id": "market_3"},
    ]
}

SAMPLE_TICKER_DATA_MARKET_1 = {
    "tikcer": {
        "market_id": "market_1",
        "max_bid": ["900", "CLP"],
        "min_ask": ["1000", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_2 = {
    "tikcer": {
        "market_id": "market_2",
        "max_bid": ["500", "CLP"],
        "min_ask": ["550", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_3 = {
    "tikcer": {
        "market_id": "market_3",
        "max_bid": ["100", "CLP"],
        "min_ask": ["200", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_1_NEGATIVE_SPREAD = {
    "tikcer": {
        "market_id": "market_1",
        "max_bid": ["900", "CLP"],
        "min_ask": ["800", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_2_INVALID_VALUE = {
    "tikcer": {
        "market_id": "market_2",
        "max_bid": ["100", "CLP"],
        "min_ask": ["xx", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_3_MISSING_FIELD = {
    "tikcer": {"market_id": "market_3", "max_bid": ["100", "CLP"]}
}

SAMPLE_TICKER_DATA = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKER_DATA_NEGATIVE_SPREAD = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1_NEGATIVE_SPREAD,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKER_DATA_INVALID_VALUE = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2_INVALID_VALUE,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKER_DATA_MISSING_FIELD = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3_MISSING_FIELD,
}
