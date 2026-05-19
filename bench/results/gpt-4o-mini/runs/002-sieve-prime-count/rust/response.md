```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();

    if n < 2 {
        let _ = io::stdout().write_all(b"0\n");
        return;
    }

    let mut is_prime = vec![true; n + 1];
    is_prime[0] = false;
    is_prime[1] = false;

    for i in 2..=((n as f64).sqrt() as usize) {
        if is_prime[i] {
            for j in (i * i)..=n {
                is_prime[j] = false;
            }
        }
    }

    let count = is_prime.iter().filter(|&&x| x).count();
    let _ = io::stdout().write_all(format!("{}\n", count).as_bytes());
}
```