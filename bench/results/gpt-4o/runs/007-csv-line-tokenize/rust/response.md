```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    if input.is_empty() {
        return;
    }

    let input = input.trim_end(); // Remove the trailing newline
    let mut output = Vec::new();
    let mut field = String::new();
    let mut in_quotes = false;
    let mut chars = input.chars().peekable();

    while let Some(c) = chars.next() {
        match c {
            '"' => {
                if in_quotes {
                    if chars.peek() == Some(&'"') {
                        // Handle escaped quote
                        field.push('"');
                        chars.next();
                    } else {
                        in_quotes = false;
                    }
                } else {
                    in_quotes = true;
                }
            }
            ',' => {
                if in_quotes {
                    field.push(c);
                } else {
                    output.push(field.clone());
                    field.clear();
                }
            }
            _ => {
                field.push(c);
            }
        }
    }

    output.push(field);

    let mut stdout = io::stdout();
    for field in output {
        writeln!(stdout, "{}", field).unwrap();
    }
}
```