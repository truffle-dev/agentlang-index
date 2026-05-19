```rust
use std::io::{self, Read, Write};

fn run_length_encode(line: &str) -> Option<String> {
    if line.is_empty() {
        return None;
    }
    let bytes = line.as_bytes();
    for &b in bytes {
        if !(b'a'..=b'z').contains(&b) {
            return None;
        }
    }

    let mut out = String::new();
    let mut prev = bytes[0];
    let mut count: usize = 1;

    for &b in &bytes[1..] {
        if b == prev {
            count += 1;
        } else {
            out.push(prev as char);
            out.push_str(&count.to_string());
            prev = b;
            count = 1;
        }
    }
    out.push(prev as char);
    out.push_str(&count.to_string());
    out.push('\n');

    Some(out)
}

fn process(input: &str) -> Option<String> {
    if !input.ends_with('\n') {
        return None;
    }
    let body = &input[..input.len().saturating_sub(1)];
    if body.contains('\n') {
        return None;
    }
    run_length_encode(body)
}

fn main() {
    let mut input = String::new();
    let output = match io::stdin().read_to_string(&mut input) {
        Ok(_) => process(&input).unwrap_or_else(|| "error\n".to_string()),
        Err(_) => "error\n".to_string(),
    };
    let _ = io::stdout().write_all(output.as_bytes());
}
```