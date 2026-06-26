```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let line = input.strip_suffix('\n').unwrap_or(&input);
    if line.is_empty() {
        return;
    }
    let mut out = io::stdout().lock();
    let bytes = line.as_bytes();
    let mut i = 0;
    loop {
        if i < bytes.len() && bytes[i] == b'"' {
            i += 1;
            let mut field = Vec::new();
            while i < bytes.len() {
                if bytes[i] == b'"' {
                    if i + 1 < bytes.len() && bytes[i + 1] == b'"' {
                        field.push(b'"');
                        i += 2;
                    } else {
                        i += 1;
                        break;
                    }
                } else {
                    field.push(bytes[i]);
                    i += 1;
                }
            }
            out.write_all(&field).unwrap();
        } else {
            let start = i;
            while i < bytes.len() && bytes[i] != b',' {
                i += 1;
            }
            out.write_all(&bytes[start..i]).unwrap();
        }
        out.write_all(b"\n").unwrap();
        if i < bytes.len() && bytes[i] == b',' {
            i += 1;
        } else {
            break;
        }
    }
}
```