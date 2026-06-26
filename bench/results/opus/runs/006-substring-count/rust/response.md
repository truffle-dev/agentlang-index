```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let p = lines.next().unwrap();
    let t = lines.next().unwrap_or("");
    let plen = p.len();
    let mut count = 0u64;
    let mut i = 0;
    let tb = t.as_bytes();
    let pb = p.as_bytes();
    while i + plen <= tb.len() {
        if &tb[i..i + plen] == pb {
            count += 1;
            i += plen;
        } else {
            i += 1;
        }
    }
    io::stdout().write_all(format!("{}\n", count).as_bytes()).unwrap();
}
```