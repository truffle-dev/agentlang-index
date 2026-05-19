```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    if input.is_empty() || !input.ends_with('\n') {
        io::stdout().write_all(b"error\n").unwrap();
        return;
    }

    let input = input.trim_end(); // Remove the trailing newline for processing

    if input.is_empty() || input.chars().any(|c| !('a'..='z').contains(&c)) {
        io::stdout().write_all(b"error\n").unwrap();
        return;
    }

    let mut result = String::new();
    let mut chars = input.chars().peekable();

    while let Some(current_char) = chars.next() {
        let mut count = 1;
        while let Some(&next_char) = chars.peek() {
            if next_char == current_char {
                count += 1;
                chars.next();
            } else {
                break;
            }
        }
        result.push(current_char);
        result.push_str(&count.to_string());
    }

    result.push('\n');
    io::stdout().write_all(result.as_bytes()).unwrap();
}
```