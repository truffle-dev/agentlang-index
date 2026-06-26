```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();
    if n < 2 {
        io::stdout().write_all(b"0\n").unwrap();
        return;
    }
    let mut sieve = vec![true; n + 1];
    sieve[0] = false;
    sieve[1] = false;
    let mut i = 2;
    while i * i <= n {
        if sieve[i] {
            let mut j = i * i;
            while j <= n {
                sieve[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    let count = sieve.iter().filter(|&&b| b).count();
    io::stdout().write_all(format!("{}\n", count).as_bytes()).unwrap();
}
```