```rust
use std::io::{self, Read, Write};

fn is_ws(b: u8) -> bool {
    matches!(b, b' ' | b'\t' | b'\n' | b'\r')
}

fn main() {
    let mut buf = Vec::new();
    // Read all bytes; on error, proceed with whatever was read (if any).
    let _ = io::stdin().read_to_end(&mut buf);

    let mut in_word = false;
    let mut count: u64 = 0;

    for &b in &buf {
        if is_ws(b) {
            in_word = false;
        } else if !in_word {
            count += 1;
            in_word = true;
        }
    }

    let mut out = io::stdout();
    let _ = out.write_all(format!("{}\n", count).as_bytes());
}
```