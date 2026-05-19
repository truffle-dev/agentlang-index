```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();

    if input.is_empty() {
        return;
    }

    let mut output = Vec::new();
    let mut current_byte = input[0];
    let mut count = 1;

    for &byte in &input[1..] {
        if byte == current_byte {
            count += 1;
        } else {
            writeln!(output, "{} {}", count, current_byte).unwrap();
            current_byte = byte;
            count = 1;
        }
    }
    writeln!(output, "{} {}", count, current_byte).unwrap();

    io::stdout().write_all(&output).unwrap();
}
```