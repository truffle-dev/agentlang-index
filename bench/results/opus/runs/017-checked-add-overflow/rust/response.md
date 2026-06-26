```rust
use std::io::Read;

fn main() {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let r = (|| {
        let a: u32 = lines.next()?.trim_end().parse().ok()?;
        let b: u32 = lines.next()?.trim_end().parse().ok()?;
        a.checked_add(b)
    })();
    match r {
        Some(s) => std::io::stdout().write_all(format!("{s}\n").as_bytes()).unwrap(),
        None => std::io::stdout().write_all(b"error\n").unwrap(),
    }
}
```