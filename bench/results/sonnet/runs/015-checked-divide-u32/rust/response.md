```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let out = run(&mut lines);
    io::stdout().write_all(out.as_bytes()).unwrap();
}

fn run<'a>(lines: &mut impl Iterator<Item = &'a str>) -> String {
    let line_a = match lines.next() {
        Some(l) => l.trim_end().to_string(),
        None => return "error\n".to_string(),
    };
    let line_b = match lines.next() {
        Some(l) => l.trim_end().to_string(),
        None => return "error\n".to_string(),
    };

    let a: u32 = match line_a.parse() {
        Ok(v) => v,
        Err(_) => return "error\n".to_string(),
    };
    let b: u32 = match line_b.parse() {
        Ok(v) => v,
        Err(_) => return "error\n".to_string(),
    };

    if b == 0 {
        return "error\n".to_string();
    }

    format!("{}\n", a / b)
}
```