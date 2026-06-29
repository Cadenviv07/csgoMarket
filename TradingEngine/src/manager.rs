use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use std::sync::mpsc::Receiver;

use crate::PaperExecutor; 
use crate::model::ShockMessage;

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
            }
        }
    }
}

//Note about scopes and locking 