use std::sync::mpsc;
use std::thread;
use std::time::Duration;
use std::env;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
mod ipc;
mod manager;
use crate::ipc;
use crate::manager::PaperExecutor;


// $env:MARKET_DB_PATH="/my/custom/path.db"
fn main(){
    let market_db = env::var("MARKET_DB_PATH")
        .unwrap_or_else(|_| String::from("../../DataIngestion/market.db"));

    let positions = Arc::new(Mutex::new(HashMap::new()));
    let executor = Arc::new(Mutex::new(PaperExecutor::new()));
    let (tx, rx) = mpsc::channel();

    let tx_clone = tx.clone();
    thread::spawn(move || {
        ipc::run(tx_clone); 
    });

    let pos_clone = positions.clone();
    let exec_clone = executor.clone();
    let db_clone = market_db.clone();

    thread::spawn(move || {
        manager::run_tick_loop(pos_clone, exec_clone, db_clone);
    });

    manager::run_shock_consumer(rx, positions, executor, market_db);
}
