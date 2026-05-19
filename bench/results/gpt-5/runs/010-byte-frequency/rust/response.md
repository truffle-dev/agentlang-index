```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    let _ = io::stdin().read_to_end(&mut input);

    let mut counts = [0u64; 256];
    for &b in &input {
        counts[b as usize] += 1;
    }

    let mut out = Vec::new();
    for (i, &c) in counts.iter().enumerate() {
        if c != 0 {
            let _ = write!(&mut out, "{} {}\n", i, c);
        }
    }

    let _ = io::stdout().write_all(&out);
}
```