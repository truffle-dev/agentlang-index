```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();
    let stdout = io::stdout();
    let mut out = stdout.lock();
    if input.is_empty() { return; }
    let mut cur = input[0];
    let mut count = 1usize;
    for &b in &input[1..] {
        if b == cur {
            count += 1;
        } else {
            writeln!(out, "{} {}", count, cur).unwrap();
            cur = b;
            count = 1;
        }
    }
    writeln!(out, "{} {}", count, cur).unwrap();
}
```