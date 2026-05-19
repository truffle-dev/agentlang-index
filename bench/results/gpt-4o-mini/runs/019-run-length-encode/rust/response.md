```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() || input.is_empty() {
        write_error();
        return;
    }

    let input = input.trim_end(); // Remove the trailing newline
    if !input.chars().all(|c| c.is_ascii_lowercase()) {
        write_error();
        return;
    }

    let mut result = String::new();
    let mut count = 1;

    for i in 1..input.len() {
        if input.as_bytes()[i] == input.as_bytes()[i - 1] {
            count += 1;
        } else {
            result.push(input.as_bytes()[i - 1] as char);
            result.push_str(&count.to_string());
            count = 1;
        }
    }

    // Handle the last run
    if !input.is_empty() {
        result.push(input.as_bytes()[input.len() - 1] as char);
        result.push_str(&count.to_string());
    }

    result.push('\n');
    io::stdout().write_all(result.as_bytes()).unwrap();
}

fn write_error() {
    io::stdout().write_all(b"error\n").unwrap();
}
```