```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let a: Vec<char> = lines.next().unwrap_or("").chars().collect();
    let b: Vec<char> = lines.next().unwrap_or("").chars().collect();
    let m = a.len();
    let n = b.len();
    let mut dp = vec![vec![0usize; n + 1]; m + 1];
    for i in 0..=m { dp[i][0] = i; }
    for j in 0..=n { dp[0][j] = j; }
    for i in 1..=m {
        for j in 1..=n {
            dp[i][j] = if a[i-1] == b[j-1] {
                dp[i-1][j-1]
            } else {
                1 + dp[i-1][j-1].min(dp[i-1][j]).min(dp[i][j-1])
            };
        }
    }
    let out = format!("{}\n", dp[m][n]);
    io::stdout().write_all(out.as_bytes()).unwrap();
}
```