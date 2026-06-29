trait Executor{
    fn execute_buy(& mut self, asset: &str, price: f64, capital_usd: f64) -> Result<TradeId>
    fn execute_sell(&mut self, trade_id: TradeId, price: f64) -> Result<RealizedPnL>
}
