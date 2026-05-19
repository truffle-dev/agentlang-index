```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let pattern = lines.next().unwrap();
    let text = lines.next().unwrap_or("");

    let mut count = 0;
    let mut index = 0;
    let pattern_len = pattern.len();

    while index <= text.len() - pattern_len {
        if &text[index..index + pattern_len] == pattern {
            count += 1;
            index += pattern_len;
        } else {
            index += 1;
        }
    }

    writeln!(io::stdout(), "{}", count).unwrap();
}
```