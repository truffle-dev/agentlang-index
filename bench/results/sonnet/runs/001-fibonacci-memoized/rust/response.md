```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: usize = input.trim().parse().unwrap();

    let mut memo = vec![0u64; n.max(2) + 1];
    memo[1] = 1;
    for i in 2..=n {
        memo[i] = memo[i-1] + memo[i-2];
    }

    let out = format!("{}\n", memo[n]);
    io::stdout().write_all(out.as_bytes()).unwrap();
}
```