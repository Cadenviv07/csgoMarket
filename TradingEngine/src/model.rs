use serde::Deserialize;
use serde_json::Value;


#[derive(Serialize, Deserialize)] 
ShockMessage{
    asset:  String,
    satus:  String,
    baseline: f64
}
