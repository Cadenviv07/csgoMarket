// TAU_RECOVERY_HOURS = 24.0
// TAU_CONFIDENCE_HOURS = 6.0 
// BASE_CAPITAL_USD = 5.0 
// MAX_CONCURRENT_POSITIONS = 3


fn signal_confidence(hours_elapsed: f64, tau_conf: f64) -> f64 {
    let e_val: f64 = std::f64::consts::E;
    let confidence: f64 = e_val.exp(-hours_elapsed/tau_conf);
    confidence
}

fn position_size(base_capital: f64, num_open: usize, max_concurrent: usize) -> f64{
    if num_open >= max_concurrent: return 0.0   -- refuse to trade
    let fraction_used = num_open as f64 / max_concurrent as f64
    return base_capital * (1.0 - fraction_used)
}