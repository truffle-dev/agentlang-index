```rust
use std::io::{Read, Write};

fn write_output(s: &str) {
    let _ = std::io::stdout().write_all(s.as_bytes());
}

fn write_error_and_exit() {
    write_output("error\n");
}

fn main() {
    // Read entire stdin
    let mut input = String::new();
    if std::io::stdin().read_to_string(&mut input).is_err() {
        write_error_and_exit();
        return;
    }

    let s = input.trim();
    if s.is_empty() {
        write_error_and_exit();
        return;
    }

    // Parse integer and validate range
    let n_i64: i64 = match s.parse() {
        Ok(v) => v,
        Err(_) => {
            write_error_and_exit();
            return;
        }
    };

    if n_i64 < 0 || n_i64 > 10000 {
        write_error_and_exit();
        return;
    }

    let n = n_i64 as usize;

    // Handle small cases
    if n < 2 {
        write_output("0\n");
        return;
    }

    // Sieve of Eratosthenes
    let mut sieve = vec![true; n + 1];
    sieve[0] = false;
    sieve[1] = false;

    let mut p = 2usize;
    while p * p <= n {
        if sieve[p] {
            let mut m = p * p;
            while m <= n {
                sieve[m] = false;
                m += p;
            }
        }
        p += 1;
    }

    let count = sieve.iter().filter(|&&b| b).count();
    let out = format!("{}\n", count);
    write_output(&out);
}
```