```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();

    let prime_count = sieve_of_eratosthenes(n);
    writeln!(io::stdout(), "{}", prime_count).unwrap();
}

fn sieve_of_eratosthenes(n: usize) -> usize {
    if n < 2 {
        return 0;
    }

    let mut is_prime = vec![true; n + 1];
    is_prime[0] = false;
    is_prime[1] = false;

    for i in 2..=((n as f64).sqrt() as usize) {
        if is_prime[i] {
            for j in (i * i..=n).step_by(i) {
                is_prime[j] = false;
            }
        }
    }

    is_prime.iter().filter(|&&prime| prime).count()
}
```