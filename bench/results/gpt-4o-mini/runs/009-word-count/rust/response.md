```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let word_count = input.split_whitespace().count();
    let output = format!("{}\n", word_count);
    
    if let Err(_) = io::stdout().write_all(output.as_bytes()) {
        let _ = io::stdout().write_all(b"error\n");
    }
}
```