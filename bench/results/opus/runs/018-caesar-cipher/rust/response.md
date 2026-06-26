```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.split('\n');

    let line1 = match lines.next() {
        Some(l) => l.trim_end(),
        None => { io::stdout().write_all(b"error\n").unwrap(); return; }
    };

    let shift: u8 = match line1.parse::<u32>() {
        Ok(v) if v <= 25 => v as u8,
        _ => { io::stdout().write_all(b"error\n").unwrap(); return; }
    };

    let line2 = match lines.next() {
        Some(l) if !l.is_empty() => l,
        _ => { io::stdout().write_all(b"error\n").unwrap(); return; }
    };

    let bytes = line2.as_bytes();
    if bytes.iter().any(|&b| b < b'a' || b > b'z') {
        io::stdout().write_all(b"error\n").unwrap();
        return;
    }

    let mut out: Vec<u8> = bytes.iter().map(|&b| (b - b'a' + shift) % 26 + b'a').collect();
    out.push(b'\n');
    io::stdout().write_all(&out).unwrap();
}
```