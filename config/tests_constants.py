SAMPLE_MARKETS_DATA = {
    "markets": [
        {"id": "market_1"},
        {"id": "market_2"},
        {"id": "market_3"},
    ]
}

SAMPLE_MARKET_DATA_ID_1 = {"id": "market_1"}

SAMPLE_MARKETS_DATA_MISSING_MARKET_ID = {
    "markets": [
        {"id": "market_1"},
        {"id": "market_2"},
        {"id": "unknown_market"},
    ]
}

SAMPLE_TICKER_DATA_MARKET_1 = {
    "ticker": {
        "market_id": "market_1",
        "max_bid": ["900", "CLP"],
        "min_ask": ["1000", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_2 = {
    "ticker": {
        "market_id": "market_2",
        "max_bid": ["500", "CLP"],
        "min_ask": ["550", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_3 = {
    "ticker": {
        "market_id": "market_3",
        "max_bid": ["50", "CLP"],
        "min_ask": ["200", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA = {
    "ticker": {
        "market_id": "market_1",
        "max_bid": ["900"],
        "min_ask": ["xx", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD = {
    "ticker": {
        "market_id": "market_2",
        "max_bid": ["100", "CLP"],
    }
}
SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATA_AND_MISSING_FIELD = {
    "ticker": {"market_id": "market_3", "max_bid": ["xx", "CLP"]}
}

SAMPLE_TICKERS_DATA_SET = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKERS_DATA_SET_INVALID_VALUE = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1_INVALID_DATA,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKERS_DATA_SET_MISSING_FIELD = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2_MISSING_FIELD,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3,
}

SAMPLE_TICKERS_DATA_SET_INVALID_VALUE_AND_MISSING_FIELD = {
    "market_1": SAMPLE_TICKER_DATA_MARKET_1,
    "market_2": SAMPLE_TICKER_DATA_MARKET_2,
    "market_3": SAMPLE_TICKER_DATA_MARKET_3_INVALID_DATA_AND_MISSING_FIELD,
}

SAMPLE_SPREAD_ALERT_WITH_VALUE_SETUP = {"value": "100"}
SAMPLE_SPREAD_ALERT_EMPTY = {"value": None}
