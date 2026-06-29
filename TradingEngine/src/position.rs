#[derive(Debug, Serialize, Deserialize, PartialEq)]
pub enum TradeState {
    #[serde(rename = "O")]
    Open,
    #[serde(rename = "CR")]
    CloseRequested,
    #[serde(rename = "CCD")]
    ClosedCanceled,
    #[serde(rename = "CT")]
    ClosedTriggered,
}


struct Position:
    trade_id:      TradeId,
    asset:         String,
    baseline:      f64,
    entry_price:   f64,
    entry_time:    DateTime<Utc>,
    capital_usd:   f64,
    state:         TradeState,

