```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

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

    if !stack.is_empty() {
        balanced = false;
    }

    let out = if balanced { "yes\n" } else { "no\n" };
    io::stdout().write_all(out.as_bytes()).unwrap();
}
```