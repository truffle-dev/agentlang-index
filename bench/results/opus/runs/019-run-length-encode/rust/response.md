```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let line = match input.strip_suffix('\n') {
        Some(l) => l,
        None => {
            io::stdout().write_all(b"error\n").unwrap();
            return;
        }
    };

    if line.is_empty() || !line.bytes().all(|b| b >= b'a' && b <= b'z') {
        io::stdout().write_all(b"error\n").unwrap();
        return;
    }

    let bytes = line.as_bytes();
    let mut result = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        let ch = bytes[i];
        let mut count = 1usize;
        while i + count < bytes.len() && bytes[i + count] == ch {
            count += 1;
        }
        result.push(ch);
        result.extend_from_slice(count.to_string().as_bytes());
        i += count;
    }
    result.push(b'\n');
    io::stdout().write_all(&result).unwrap();
}
```