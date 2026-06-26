```rust
use std::io::{self, Read, Write};
use std::time::Duration;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok();
    let url = input.trim();

    let result = (|| -> Result<u16, ()> {
        let resp = ureq::AgentBuilder::new()
            .timeout_connect(Duration::from_millis(5000))
            .timeout_read(Duration::from_millis(5000))
            .timeout_write(Duration::from_millis(5000))
            .build()
            .get(url)
            .call();
        match resp {
            Ok(r) => Ok(r.status()),
            Err(ureq::Error::Status(code, _)) => Ok(code),
            Err(_) => Err(()),
        }
    })();

    let out = match result {
        Ok(code) => format!("{}\n", code),
        Err(()) => "error\n".to_string(),
    };
    io::stdout().write_all(out.as_bytes()).ok();
}
```

And the `Cargo.toml`:

```toml
[package]
name = "ref"
edition = "2021"

[[bin]]
name = "ref"
path = "ref.rs"

[dependencies]
ureq = "2"
```