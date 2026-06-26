```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();
    if input.is_empty() {
        return;
    }
    let mut out = io::stdout().lock();
    let mut count: usize = 1;
    for i in 1..input.len() {
        if input[i] == input[i - 1] {
            count += 1;
        } else {
            write!(out, "{} {}\n", count, input[i - 1]).unwrap();
            count = 1;
        }
    }
    write!(out, "{} {}\n", count, input[input.len() - 1]).unwrap();
}
```