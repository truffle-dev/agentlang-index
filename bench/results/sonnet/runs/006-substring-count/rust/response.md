```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let p = lines.next().unwrap_or("");
    let t = lines.next().unwrap_or("");

    let pb = p.as_bytes();
    let tb = t.as_bytes();
    let plen = pb.len();
    let tlen = tb.len();

    let mut count = 0;
    let mut i = 0;
    while i + plen <= tlen {
        if &tb[i..i + plen] == pb {
            count += 1;
            i += plen;
        } else {
            i += 1;
        }
    }

    let out = format!("{}\n", count);
    io::stdout().write_all(out.as_bytes()).unwrap();
}
```