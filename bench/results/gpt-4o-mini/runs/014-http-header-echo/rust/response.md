```rust
use std::io::{self, Read, Write};
use reqwest::header::{HeaderMap, HeaderName};
use std::time::Duration;

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        write!(io::stdout(), "error\n").unwrap();
        return;
    }

    let mut lines = input.lines();
    let url = lines.next().unwrap_or("").trim();
    let header_name = lines.next().unwrap_or("").trim();

    let client = reqwest::Client::builder()
        .timeout(Duration::from_millis(5000))
        .build()
        .unwrap();

    match client.get(url).send() {
        Ok(response) => {
            if response.status().is_success() {
                let headers: HeaderMap = response.headers().clone();
                let header_name = HeaderName::from_lowercase(header_name.as_bytes()).unwrap();
                if let Some(value) = headers.get(&header_name) {
                    let value_str = value.to_str().unwrap_or("");
                    write!(io::stdout(), "{}\n", value_str).unwrap();
                    return;
                }
            }
        }
        Err(_) => {}
    }

    write!(io::stdout(), "error\n").unwrap();
}
```