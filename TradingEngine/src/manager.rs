use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use std::sync::mpsc::Receiver;

use crate::PaperExecutor; 
use crate::model::ShockMessage;
use rusqlite::Connection;

mod market_data;
mod decay;

use market_date::latest_price;
use decay::position_size;

pub fn run_tick_loop(
    positions: Arc<Mutex<HashMap<String, f64>>>, 
    executor: Arc<Mutex<PaperExecutor>>,
    db_path: String,
) {
    println!("Starting tick loop using DB at: {}", db_path);
    
    loop {
      
        std::thread::sleep(std::time::Duration::from_millis(10*10*10*60));
    }
}

pub fn run_shock_consumer(rx: Receiver<ShockMessage>, 
    positions: Arc<Mutex<HashMap<String, f64>>>, 
    executor: Arc<Mutex<PaperExecutor>>, 
    db_path: String,
){
    for message in rx{
        match message{
            {

                let conn = Connection::open(&db_path).expect("Failed to open SQLite");

                let mut guard_p = positions.lock().unwrap();
                let target_asset = message.asset;
                if guard.contains_key(&message.asset) {
                    // Log it to the terminal
                    println!("Duplicate shock received for {}. Skipping.", message.asset);
                    continue; 
                }

                if guard.len() >= 3 {
                    println!("At capacity! Cannot trade {}. Skipping.", message.asset);
                    continue;
                }

                match latest_price(&conn, &target_asset){
                    Some(price) => {
                        println!("Got price: ${}. Proceeding to math engine.", price);
                        size = position_size()
                    },
                    None => {
                        println!("No price data found in SQLite for {}. Skipping.", message.asset);
                        continue; 
                    }
                }
            }
        }
    }
}

//Note about scopes and locking 