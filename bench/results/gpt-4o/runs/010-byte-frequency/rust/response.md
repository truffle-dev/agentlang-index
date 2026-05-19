```rust
use std::io::{self, Read, Write};

fn main() -> io::Result<()> {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input)?;

    let mut counts = [0u32; 256];
    for &byte in &input {
        counts[byte as usize] += 1;
    }

    let stdout = io::stdout();
    let mut handle = stdout.lock();
    for (byte, &count) in counts.iter().enumerate() {
        if count > 0 {
            writeln!(handle, "{} {}", byte, count)?;
        }
    }

    Ok(())
}
```