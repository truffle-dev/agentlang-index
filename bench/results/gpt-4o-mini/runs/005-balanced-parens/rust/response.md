```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        let _ = io::stdout().write_all(b"no\n");
        return;
    }

    let mut stack = Vec::new();
    let mut balanced = true;

    for ch in input.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' => {
                if stack.pop() != Some('(') {
                    balanced = false;
                    break;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    balanced = false;
                    break;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    balanced = false;
                    break;
                }
            }
            _ => {}
        }
    }

    if balanced && stack.is_empty() {
        let _ = io::stdout().write_all(b"yes\n");
    } else {
        let _ = io::stdout().write_all(b"no\n");
    }
}
```