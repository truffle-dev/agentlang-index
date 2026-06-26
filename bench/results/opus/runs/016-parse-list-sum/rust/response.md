```rust
use std::io::Read;

fn main() {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();

    let result = (|| -> Option<u32> {
        let mut lines = input.lines();
        let n: u32 = parse_u32(lines.next()?)?;
        if n > 1000 {
            return None;
        }
        let mut sum: u32 = 0;
        for _ in 0..n {
            let val = parse_u32(lines.next()?)?;
            sum = sum.checked_add(val)?;
        }
        Some(sum)
    })();

    match result {
        Some(s) => std::io::Write::write_all(&mut std::io::stdout(), format!("{}\n", s).as_bytes()).unwrap(),
        None => std::io::Write::write_all(&mut std::io::stdout(), b"error\n").unwrap(),
    }
}

fn parse_u32(line: &str) -> Option<u32> {
    let s = line.trim_end();
    if s.is_empty() {
        return None;
    }
    for b in s.bytes() {
        if !b.is_ascii_digit() {
            return None;
        }
    }
    s.parse::<u32>().ok()
}
```