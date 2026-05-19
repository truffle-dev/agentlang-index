```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let mut lines = input.lines();
    let first_line = lines.next().unwrap_or("").trim();

    let n: u32 = match first_line.parse() {
        Ok(num) if num <= 1000 => num,
        _ => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    let mut sum: u32 = 0;

    for line in lines.take(n as usize) {
        let value_str = line.trim();
        if value_str.is_empty() {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }

        match value_str.parse::<u32>() {
            Ok(value) => {
                if sum.checked_add(value).is_none() {
                    let _ = io::stdout().write_all(b"error\n");
                    return;
                }
                sum += value;
            }
            _ => {
                let _ = io::stdout().write_all(b"error\n");
                return;
            }
        }
    }

    if lines.count() > 0 {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let _ = writeln!(io::stdout(), "{}", sum);
}
```