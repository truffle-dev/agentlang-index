```rust
use std::io::{self, Read};
use std::time::Duration;
use reqwest::blocking::Client;
use reqwest::header::HeaderMap;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let url = lines.next().unwrap_or("").trim();
    let header_name = lines.next().unwrap_or("").trim();

    let client = Client::builder()
        .timeout(Duration::from_millis(5000))
        .build()
        .unwrap();

    match client.get(url).send() {
        Ok(response) => {
            if response.status() == 200 {
                let headers: HeaderMap = response.headers().clone();
                if let Some(value) = headers.get(header_name) {
                    if let Ok(value_str) = value.to_str() {
                        println!("{}", value_str);
                        return;
                    }
                }
            }
            println!("error");
        }
        Err(_) => {
            println!("error");
        }
    }
}
```