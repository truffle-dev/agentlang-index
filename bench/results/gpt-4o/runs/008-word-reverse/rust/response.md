```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let words: Vec<&str> = input.split_whitespace().collect();
    if !words.is_empty() {
        let reversed: String = words.into_iter().rev().collect::<Vec<&str>>().join(" ");
        io::stdout().write_all(reversed.as_bytes()).unwrap();
        io::stdout().write_all(b"\n").unwrap();
    }
}
```