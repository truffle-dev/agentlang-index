```rust
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let lines: Vec<&str> = input.lines().collect();
    if lines.len() != 2 {
        println!("error");
        return;
    }

    let a = lines[0].trim();
    let b = lines[1].trim();

    match (a.parse::<u32>(), b.parse::<u32>()) {
        (Ok(a), Ok(b)) => match a.checked_add(b) {
            Some(sum) => println!("{}", sum),
            None => println!("error"),
        },
        _ => println!("error"),
    }
}
```