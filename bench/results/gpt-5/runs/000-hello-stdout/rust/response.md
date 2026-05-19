```rust
use std::io::{self, Read, Write};

fn main() {
    let mut _input = String::new();
    let _ = io::stdin().read_to_string(&mut _input);

    let mut out = io::stdout();
    let _ = out.write_all(b"hello\n");
}
```