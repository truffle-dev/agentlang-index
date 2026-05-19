```rust
use std::io::{self, Read, Write};

fn main() {
    let mut buffer = vec![0; 256];
    if let Ok(mut input) = io::stdin().read_to_string(&mut String::new()) {
        for byte in input.bytes() {
            buffer[byte as usize] += 1;
        }
    }

    let stdout = io::stdout();
    let mut handle = stdout.lock();
    for (byte, count) in buffer.iter().enumerate() {
        if *count > 0 {
            let _ = writeln!(handle, "{} {}", byte, count);
        }
    }
}
```