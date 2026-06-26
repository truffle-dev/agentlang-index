```rust
use std::io::Read;

fn main() {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let a_str = lines.next().unwrap_or("").trim_end();
    let b_str = lines.next().unwrap_or("").trim_end();
    let ok = (|| {
        if a_str.is_empty() || b_str.is_empty() {
            return None;
        }
        if a_str.starts_with('+') || b_str.starts_with('+') {
            return None;
        }
        let a: u32 = a_str.parse().ok()?;
        let b: u32 = b_str.parse().ok()?;
        if b == 0 { return None; }
        Some(a / b)
    })();
    match ok {
        Some(v) => std::io::Write::write_all(&mut std::io::stdout(), format!("{}\n", v).as_bytes()).unwrap(),
        None => std::io::Write::write_all(&mut std::io::stdout(), b"error\n").unwrap(),
    }
}
```