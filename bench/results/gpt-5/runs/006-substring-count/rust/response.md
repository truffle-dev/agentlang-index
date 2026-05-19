```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    let mut lines = input.lines();
    let p = lines.next().unwrap_or("");
    let t = lines.next().unwrap_or("");

    let pb = p.as_bytes();
    let tb = t.as_bytes();

    let mut count: usize = 0;

    if !pb.is_empty() && !tb.is_empty() {
        let plen = pb.len();
        let mut i = 0usize;
        while i + plen <= tb.len() {
            if &tb[i..i + plen] == pb {
                count += 1;
                i += plen;
            } else {
                i += 1;
            }
        }
    }

    let out = format!("{}\n", count);
    let _ = io::stdout().write_all(out.as_bytes());
}
```