struct Position:
    trade_id:      TradeId
    asset:         String
    baseline:      f64
    entry_price:   f64
    entry_time:    DateTime<Utc>
    capital_usd:   f64
    state:         enum {"O", "CR", "CCD", "CT"}
