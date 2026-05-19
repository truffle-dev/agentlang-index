```rust
use std::io::{self, Write};

fn main() {
    io::stdout().write_all(b"hello\n").unwrap();
}
```