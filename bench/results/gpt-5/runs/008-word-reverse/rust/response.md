```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    if input.ends_with('\n') {
        input.pop();
        if input.ends_with('\r') {
            input.pop();
        }
    }

    let mut words: Vec<&str> = input.split(' ').filter(|w| !w.is_empty()).collect();
    if words.is_empty() {
        return;
    }

    words.reverse();
    let mut out = String::new();
    out.push_str(&words.join(" "));
    out.push('\n');

    let _ = io::stdout().write_all(out.as_bytes());
}
```