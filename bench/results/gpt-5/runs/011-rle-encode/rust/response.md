```rust
// ref.rs
use std::io::{self, Read, Write};

fn main() {
    // Read all of stdin into a String (UTF-8). If this fails, treat as empty input.
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    let bytes = input.as_bytes();

    let mut out: Vec<u8> = Vec::new();

    if !bytes.is_empty() {
        let mut prev = bytes[0];
        let mut count: usize = 1;

        for &b in &bytes[1..] {
            if b == prev {
                count += 1;
            } else {
                let _ = write!(&mut out, "{} {}", count, prev);
                out.push(b'\n');
                prev = b;
                count = 1;
            }
        }
        // Emit the last run
        let _ = write!(&mut out, "{} {}", count, prev);
        out.push(b'\n');
    }

    let mut stdout = io::stdout();
    let _ = stdout.write_all(&out);
}
```