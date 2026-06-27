```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let mut lines = input.splitn(2, '\n');
    let line1 = lines.next().unwrap_or("");
    let line2 = lines.next().unwrap_or("");

    let shift_str = line1.trim_end_matches(|c: char| c == ' ' || c == '\t' || c == '\r');
    let shift_str = shift_str.trim();

    let out = io::stdout();
    let mut out = out.lock();

    let shift: u8 = match parse_shift(shift_str) {
        Some(s) => s,
        None => {
            out.write_all(b"error\n").unwrap();
            return;
        }
    };

    // line2 is taken verbatim - strip trailing \r if present (from \r\n line endings)
    let plaintext = if line2.ends_with('\r') {
        &line2[..line2.len() - 1]
    } else {
        line2
    };

    if plaintext.is_empty() {
        out.write_all(b"error\n").unwrap();
        return;
    }

    for b in plaintext.bytes() {
        if b < b'a' || b > b'z' {
            out.write_all(b"error\n").unwrap();
            return;
        }
    }

    let cipher: Vec<u8> = plaintext
        .bytes()
        .map(|b| (b - b'a' + shift) % 26 + b'a')
        .collect();

    out.write_all(&cipher).unwrap();
    out.write_all(b"\n").unwrap();
}

fn parse_shift(s: &str) -> Option<u8> {
    if s.is_empty() {
        return None;
    }
    for c in s.chars() {
        if !c.is_ascii_digit() {
            return None;
        }
    }
    let val: u32 = s.parse().ok()?;
    if val > 25 {
        return None;
    }
    Some(val as u8)
}
```