```rust
use std::io::{self, Read, Write};

fn main() {
    // Read entire stdin into a string
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    let mut stack: Vec<u8> = Vec::new();
    let mut ok = true;

    for b in input.bytes() {
        if b == b'\n' {
            break;
        }
        match b {
            b'(' => stack.push(b')'),
            b'[' => stack.push(b']'),
            b'{' => stack.push(b'}'),
            b')' | b']' | b'}' => {
                if let Some(expected) = stack.pop() {
                    if expected != b {
                        ok = false;
                        break;
                    }
                } else {
                    ok = false;
                    break;
                }
            }
            _ => {}
        }
    }

    let out = if ok && stack.is_empty() { "yes\n" } else { "no\n" };
    let _ = io::stdout().write_all(out.as_bytes());
}
```