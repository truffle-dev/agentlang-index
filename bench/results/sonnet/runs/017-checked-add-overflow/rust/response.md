```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let out = run(lines.next(), lines.next());
    io::stdout().write_all(out.as_bytes()).unwrap();
}

fn run(a: Option<&str>, b: Option<&str>) -> String {
    let parse = |s: Option<&str>| -> Option<u32> {
        let s = s?.trim_end();
        if s.is_empty() { return None; }
        s.parse::<u32>().ok()
    };
    match (parse(a), parse(b)) {
        (Some(a), Some(b)) => match a.checked_add(b) {
            Some(sum) => format!("{}\n", sum),
            None => "error\n".to_string(),
        },
        _ => "error\n".to_string(),
    }
}
```