```rust
use std::io::{self, Read, Write};
use std::time::Duration;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let url = input.trim_end_matches('\n').trim_end_matches('\r').trim();

    let result = ureq::builder()
        .timeout(Duration::from_millis(5000))
        .build()
        .get(url)
        .call();

    let output = match result {
        Ok(resp) => format!("{}\n", resp.status()),
        Err(ureq::Error::Status(code, _)) => format!("{}\n", code),
        Err(_) => "error\n".to_string(),
    };

    io::stdout().write_all(output.as_bytes()).unwrap();
}
```