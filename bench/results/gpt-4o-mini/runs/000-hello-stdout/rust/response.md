```rust
use std::io::{self, Write};

fn main() {
    let output = b"hello\n";
    io::stdout().write_all(output).unwrap();
}
```