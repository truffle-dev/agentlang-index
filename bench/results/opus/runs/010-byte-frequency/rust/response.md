```rust
use std::io::{self, Read, Write};

fn main() {
    let mut buf = Vec::new();
    io::stdin().read_to_end(&mut buf).unwrap();
    let mut counts = [0u64; 256];
    for &b in &buf {
        counts[b as usize] += 1;
    }
    let out = io::stdout();
    let mut out = out.lock();
    for (i, &c) in counts.iter().enumerate() {
        if c > 0 {
            let _ = write!(out, "{} {}\n", i, c);
        }
    }
}
```