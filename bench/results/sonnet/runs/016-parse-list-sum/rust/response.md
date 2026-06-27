```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let stdout = io::stdout();
    let mut out = stdout.lock();

    let mut lines = input.lines().map(|l| l.trim_end());

    let first = match lines.next() {
        Some(l) => l,
        None => { out.write_all(b"error\n").unwrap(); return; }
    };

    let n: u32 = match first.trim_end().parse::<u32>() {
        Ok(v) if v <= 1000 => v,
        _ => { out.write_all(b"error\n").unwrap(); return; }
    };

    let mut sum: u32 = 0;
    for _ in 0..n {
        let line = match lines.next() {
            Some(l) => l,
            None => { out.write_all(b"error\n").unwrap(); return; }
        };
        let val: u32 = match line.parse::<u32>() {
            Ok(v) => v,
            Err(_) => { out.write_all(b"error\n").unwrap(); return; }
        };
        sum = match sum.checked_add(val) {
            Some(s) => s,
            None => { out.write_all(b"error\n").unwrap(); return; }
        };
    }

    write!(out, "{}\n", sum).unwrap();
}
```