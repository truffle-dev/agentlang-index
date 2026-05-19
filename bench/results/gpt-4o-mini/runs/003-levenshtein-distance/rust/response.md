```rust
use std::io::{self, Read, Write};

fn levenshtein_distance(a: &str, b: &str) -> usize {
    let m = a.len();
    let n = b.len();
    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if a.chars().nth(i - 1) == b.chars().nth(j - 1) { 0 } else { 1 };
            dp[i][j] = *[
                dp[i - 1][j] + 1,    // deletion
                dp[i][j - 1] + 1,    // insertion
                dp[i - 1][j - 1] + cost, // substitution
            ].iter().min().unwrap();
        }
    }

    dp[m][n]
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let lines: Vec<&str> = input.lines().collect();
    
    let a = lines.get(0).unwrap_or(&"");
    let b = lines.get(1).unwrap_or(&"");
    
    let distance = levenshtein_distance(a, b);
    let output = format!("{}\n", distance);
    io::stdout().write_all(output.as_bytes()).unwrap();
}
```