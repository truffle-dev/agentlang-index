```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    if let Err(e) = io::stdin().read_to_end(&mut input) {
        let _ = writeln!(io::stdout(), "error");
        std::process::exit(0);
    }

    if input.is_empty() {
        return;
    }

    let mut count = 1;
    let mut previous = input[0];

    for &byte in &input[1..] {
        if byte == previous {
            count += 1;
        } else {
            let _ = writeln!(io::stdout(), "{} {}", count, previous);
            count = 1;
            previous = byte;
        }
    }
    let _ = writeln!(io::stdout(), "{} {}", count, previous);
}
```