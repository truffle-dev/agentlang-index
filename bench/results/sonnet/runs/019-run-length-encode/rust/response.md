```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let line = if let Some(line) = input.strip_suffix('\n') {
        line
    } else {
        &input
    };

    if line.is_empty() || line.bytes().any(|b| b < b'a' || b > b'z') {
        io::stdout().write_all(b"error\n").unwrap();
        return;
    }

    let bytes = line.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        let ch = bytes[i];
        let mut count = 1usize;
        while i + count < bytes.len() && bytes[i + count] == ch {
            count += 1;
        }
        out.push(ch);
        let num = count.to_string();
        out.extend_from_slice(num.as_bytes());
        i += count;
    }
    out.push(b'\n');
    io::stdout().write_all(&out).unwrap();
}
```