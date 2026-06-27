```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let count = input.split_whitespace().count();
    io::stdout().write_all(format!("{}\n", count).as_bytes()).unwrap();
}
```