use rusqlite::{Connection, Result};

let project_root = env!("CARGO_MANIFEST_DIR");
let db_path = PathBuf::from(project_root)
        .join("DataIngestion")
        .join("market.db");
let db_path = current_file.parent().expect("First parent failed").parent().expect("Second parent failed").join("DataIngestion").join("market.db");

let conn = Connection::open();

fn latest_price(conn: &Connection, asset: &str) -> Option<f64>{
    //Statments for query map should be mutable
    let sql = "
    SELECT price 
    FROM case_prices 
    WHERE name = ?1 
    ORDER BY date DESC 
    LIMIT 1 OFFSET 1
    ";

    let second_recent_price: Result<f64, rusqlite::Error> = conn.query_row(
        sql,
        [asset],
        |row| row.get(0)
    );

    match second_recent_price {
        Ok(price) => println!("The second most recent price is: {}", price),
        Err(rusqlite::Error::QueryReturnedNoRows) => println!("Not enough data for this item yet!"),
        Err(e) => println!("Database error: {}", e),
    }

    return second_recent_price.ok()
}
