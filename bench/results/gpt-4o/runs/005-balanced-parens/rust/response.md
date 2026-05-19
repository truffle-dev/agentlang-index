```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let mut stack = Vec::new();

    for ch in input.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' => {
                if stack.pop() != Some('(') {
                    io::stdout().write_all(b"no\n").unwrap();
                    return;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    io::stdout().write_all(b"no\n").unwrap();
                    return;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    io::stdout().write_all(b"no\n").unwrap();
                    return;
                }
            }
            _ => {}
        }
    }

    if stack.is_empty() {
        io::stdout().write_all(b"yes\n").unwrap();
    } else {
        io::stdout().write_all(b"no\n").unwrap();
    }
}
```