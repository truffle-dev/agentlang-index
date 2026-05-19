```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        return;
    }

    let input = input.trim_end(); // Remove the trailing newline
    if input.is_empty() {
        return; // Output nothing for empty input
    }

    let mut fields = Vec::new();
    let mut current_field = String::new();
    let mut in_quotes = false;
    let mut chars = input.chars().peekable();

    while let Some(c) = chars.next() {
        match c {
            '"' => {
                if in_quotes {
                    if chars.peek() == Some(&'"') {
                        chars.next(); // Consume the next quote
                        current_field.push('"'); // Add a quote to the field
                    } else {
                        in_quotes = false; // Closing quote
                    }
                } else {
                    in_quotes = true; // Opening quote
                }
            }
            ',' => {
                if in_quotes {
                    current_field.push(c); // Comma inside quotes
                } else {
                    fields.push(current_field.clone());
                    current_field.clear(); // Move to the next field
                }
            }
            _ => {
                current_field.push(c); // Regular character
            }
        }
    }

    // Push the last field if not empty
    fields.push(current_field);

    // Write each field to stdout
    let stdout = io::stdout();
    let mut handle = stdout.lock();
    for field in fields {
        if let Err(_) = handle.write_all(field.as_bytes()) {
            return;
        }
        if let Err(_) = handle.write_all(b"\n") {
            return;
        }
    }
}
```