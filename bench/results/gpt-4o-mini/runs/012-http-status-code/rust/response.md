```rust
use std::io::{self, Read, Write};
use reqwest::Client;
use std::time::Duration;

#[tokio::main]
async fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        write!(io::stdout(), "error\n").unwrap();
        return;
    }

    let url = input.trim();
    let client = Client::builder()
        .timeout(Duration::from_millis(5000))
        .build()
        .unwrap();

    match client.get(url).send().await {
        Ok(response) => {
            let status_code = response.status().as_u16();
            writeln!(io::stdout(), "{}", status_code).unwrap();
        }
        Err(_) => {
            write!(io::stdout(), "error\n").unwrap();
        }
    }
}
```