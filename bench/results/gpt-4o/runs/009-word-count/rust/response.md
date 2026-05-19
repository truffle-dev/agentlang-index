```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let word_count = input.split_whitespace().count();
    writeln!(io::stdout(), "{}", word_count).unwrap();
}
```