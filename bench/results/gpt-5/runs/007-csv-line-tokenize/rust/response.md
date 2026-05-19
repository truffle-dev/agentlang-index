```rust
use std::io::{Read, Write};

fn main() {
    let mut input = String::new();
    let _ = std::io::stdin().read_to_string(&mut input);

    // Consider only the first line up to '\n', if present.
    let line = match input.find('\n') {
        Some(pos) => &input[..pos],
        None => input.as_str(),
    };

    if line.is_empty() {
        // Empty input line => write nothing.
        return;
    }

    let bytes = line.as_bytes();
    let mut i = 0usize;
    let len = bytes.len();
    let mut in_quotes = false;
    let mut field: Vec<u8> = Vec::new();
    let mut out: Vec<u8> = Vec::new();

    while i < len {
        let b = bytes[i];
        if in_quotes {
            if b == b'"' {
                if i + 1 < len && bytes[i + 1] == b'"' {
                    field.push(b'"');
                    i += 2;
                    continue;
                } else {
                    in_quotes = false;
                    i += 1;
                    continue;
                }
            } else {
                field.push(b);
                i += 1;
                continue;
            }
        } else {
            if b == b',' {
                out.extend_from_slice(&field);
                out.push(b'\n');
                field.clear();
                i += 1;
                continue;
            } else if b == b'"' {
                in_quotes = true;
                i += 1;
                continue;
            } else {
                field.push(b);
                i += 1;
                continue;
            }
        }
    }

    // Final field
    out.extend_from_slice(&field);
    out.push(b'\n');

    let _ = std::io::stdout().write_all(&out);
}
```