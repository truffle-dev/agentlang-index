```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    
    let pattern = lines.next().unwrap();
    let text = lines.next().unwrap();
    
    let mut count = 0;
    let mut start = 0;

    while let Some(pos) = text[start..].find(pattern) {
        count += 1;
        start += pos + pattern.len();
    }

    let output = format!("{}\n", count);
    io::stdout().write_all(output.as_bytes()).unwrap();
}
```