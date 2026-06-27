```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();
    
    let mut counts = [0u64; 256];
    for &b in &input {
        counts[b as usize] += 1;
    }
    
    let mut out = Vec::new();
    for (i, &c) in counts.iter().enumerate() {
        if c > 0 {
            out.extend_from_slice(format!("{} {}\n", i, c).as_bytes());
        }
    }
    
    io::stdout().write_all(&out).unwrap();
}
```