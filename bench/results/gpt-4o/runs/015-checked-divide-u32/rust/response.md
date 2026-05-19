```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let a_str = lines.next().unwrap_or("").trim();
    let b_str = lines.next().unwrap_or("").trim();

    if let (Ok(a), Ok(b)) = (a_str.parse::<u32>(), b_str.parse::<u32>()) {
        if b == 0 {
            io::stdout().write_all(b"error\n").unwrap();
        } else {
            let result = a / b;
            writeln!(io::stdout(), "{}", result).unwrap();
        }
    } else {
        io::stdout().write_all(b"error\n").unwrap();
    }
}
```