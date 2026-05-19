```rust
use std::io::{self, Read};
use std::time::Duration;
use reqwest::blocking::Client;
use reqwest::Error;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let url = input.trim();

    let client = Client::builder()
        .timeout(Duration::from_millis(5000))
        .build();

    match client {
        Ok(client) => {
            match client.get(url).send() {
                Ok(response) => {
                    println!("{}", response.status().as_u16());
                }
                Err(_) => {
                    println!("error");
                }
            }
        }
        Err(_) => {
            println!("error");
        }
    }
}
```