```rust
use std::io::{self, Read, Write};

fn main() {
    // Read all input
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    // Obtain first two lines (Rust's lines() handles \n and \r\n)
    let mut it = input.lines();
    let line1 = match it.next() {
        Some(s) => s,
        None => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };
    let line2 = match it.next() {
        Some(s) => s,
        None => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    // Trim only trailing whitespace on line 1 before parsing
    let shift_str = line1.trim_end();

    // Validate and parse shift: non-empty, all digits, <= 25
    if shift_str.is_empty() || !shift_str.bytes().all(|b| b.is_ascii_digit()) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let shift_val: u32 = match shift_str.parse() {
        Ok(v) => v,
        Err(_) => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };
    if shift_val > 25 {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let shift = shift_val as u8;

    // Validate plaintext: non-empty, only 'a'..'z'
    if line2.is_empty() || !line2.bytes().all(|b| (b'a'..=b'z').contains(&b)) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    // Encrypt
    let mut out = Vec::with_capacity(line2.len() + 1);
    for &b in line2.as_bytes() {
        let offset = b - b'a';
        let rotated = ((offset as u16 + shift as u16) % 26) as u8 + b'a';
        out.push(rotated);
    }
    out.push(b'\n');

    let _ = io::stdout().write_all(&out);
}
```