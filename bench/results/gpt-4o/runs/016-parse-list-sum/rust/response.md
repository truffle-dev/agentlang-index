```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let n_line = lines.next().unwrap_or("").trim();
    let n: usize = match n_line.parse() {
        Ok(num) if num <= 1000 => num,
        _ => {
            println!("error");
            return;
        }
    };

    let mut sum: u64 = 0;
    for _ in 0..n {
        let value_line = lines.next().unwrap_or("").trim();
        let value: u32 = match value_line.parse() {
            Ok(num) => num,
            _ => {
                println!("error");
                return;
            }
        };

        sum = match sum.checked_add(value as u64) {
            Some(s) if s <= u32::MAX as u64 => s,
            _ => {
                println!("error");
                return;
            }
        };
    }

    if lines.next().is_some() {
        println!("error");
    } else {
        println!("{}\n", sum);
    }
}
```