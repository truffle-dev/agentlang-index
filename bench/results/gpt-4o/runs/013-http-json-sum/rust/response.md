```rust
use std::io::{self, Read};
use std::time::Duration;
use reqwest::blocking::Client;
use serde_json::Value;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let url = lines.next().unwrap_or("").trim();
    let a: i32 = lines.next().unwrap_or("").trim().parse().unwrap_or(0);
    let b: i32 = lines.next().unwrap_or("").trim().parse().unwrap_or(0);

    let client = Client::builder()
        .timeout(Duration::from_millis(5000))
        .build()
        .unwrap();

    let response = client.post(url)
        .header("Content-Type", "application/json")
        .body(format!(r#"{{"a":{},"b":{}}}"#, a, b))
        .send();

    match response {
        Ok(resp) => {
            if resp.status() == 200 {
                if let Ok(json) = resp.json::<Value>() {
                    if let Some(sum) = json.get("sum").and_then(|v| v.as_i64()) {
                        println!("{}", sum);
                        return;
                    }
                }
            }
        }
        Err(_) => {}
    }

    println!("error");
}
```