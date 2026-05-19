```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        return;
    }

    let words: Vec<&str> = input.split_whitespace().collect();
    if words.is_empty() {
        return;
    }

    let reversed: String = words.iter().rev().cloned().collect::<Vec<&str>>().join(" ");
    let _ = io::stdout().write_all(format!("{}\n", reversed).as_bytes());
}
```