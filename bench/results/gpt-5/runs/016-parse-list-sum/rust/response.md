```rust
use std::io::{self, Read, Write};

fn trim_end_ascii_ws(s: &str) -> &str {
    s.trim_end_matches(|c: char| c.is_ascii_whitespace())
}

fn parse_u32_strict(s: &str) -> Option<u32> {
    if s.is_empty() {
        return None;
    }
    let mut v: u64 = 0;
    for &b in s.as_bytes() {
        if b < b'0' || b > b'9' {
            return None;
        }
        v = v * 10 + (b - b'0') as u64;
        if v > u32::MAX as u64 {
            return None;
        }
    }
    Some(v as u32)
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let lines: Vec<&str> = input.split_terminator('\n').collect();
    if lines.is_empty() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let n_line = trim_end_ascii_ws(lines[0]);
    let n = match parse_u32_strict(n_line) {
        Some(v) => v,
        None => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };
    if n > 1000 {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    if lines.len().saturating_sub(1) < n as usize {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let mut sum: u32 = 0;
    for i in 0..(n as usize) {
        let val_line = trim_end_ascii_ws(lines[1 + i]);
        let val = match parse_u32_strict(val_line) {
            Some(v) => v,
            None => {
                let _ = io::stdout().write_all(b"error\n");
                return;
            }
        };
        match sum.checked_add(val) {
            Some(s) => sum = s,
            None => {
                let _ = io::stdout().write_all(b"error\n");
                return;
            }
        }
    }

    let mut out = sum.to_string();
    out.push('\n');
    let _ = io::stdout().write_all(out.as_bytes());
}
```