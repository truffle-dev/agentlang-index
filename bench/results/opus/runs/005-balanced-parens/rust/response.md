```rust
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let line = input.trim_end_matches('\n');
    let mut stack = Vec::new();
    let mut balanced = true;
    for c in line.chars() {
        match c {
            '(' | '[' | '{' => stack.push(c),
            ')' => if stack.pop() != Some('(') { balanced = false; break },
            ']' => if stack.pop() != Some('[') { balanced = false; break },
            '}' => if stack.pop() != Some('{') { balanced = false; break },
            _ => {}
        }
    }
    if balanced && stack.is_empty() {
        print!("yes\n");
    } else {
        print!("no\n");
    }
}
```