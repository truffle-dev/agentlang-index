```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let line = input.trim_end_matches('\n');
    
    if line.is_empty() {
        return;
    }
    
    let stdout = io::stdout();
    let mut out = stdout.lock();
    
    let bytes = line.as_bytes();
    let mut i = 0;
    let n = bytes.len();
    
    loop {
        if i < n && bytes[i] == b'"' {
            // quoted field
            i += 1;
            let mut field = Vec::new();
            loop {
                if i >= n {
                    break;
                }
                if bytes[i] == b'"' {
                    if i + 1 < n && bytes[i + 1] == b'"' {
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
            out.write_all(b"\n").unwrap();
        } else {
            // unquoted field
            let start = i;
            while i < n && bytes[i] != b',' {
                i += 1;
            }
            out.write_all(&bytes[start..i]).unwrap();
            out.write_all(b"\n").unwrap();
        }
        
        if i >= n {
            break;
        }
        // skip comma
        i += 1;
    }
}
```