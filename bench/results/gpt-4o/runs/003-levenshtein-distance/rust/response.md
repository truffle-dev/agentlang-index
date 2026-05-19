```rust
use std::io::{self, Read, Write};

fn levenshtein_distance(a: &str, b: &str) -> usize {
    let a_len = a.len();
    let b_len = b.len();
    let mut dp = vec![vec![0; b_len + 1]; a_len + 1];

    for i in 0..=a_len {
        dp[i][0] = i;
    }
    for j in 0..=b_len {
        dp[0][j] = j;
    }

    for i in 1..=a_len {
        for j in 1..=b_len {
            let cost = if a.as_bytes()[i - 1] == b.as_bytes()[j - 1] { 0 } else { 1 };
            dp[i][j] = *[
                dp[i - 1][j] + 1,    // Deletion
                dp[i][j - 1] + 1,    // Insertion
                dp[i - 1][j - 1] + cost, // Substitution
            ]
            .iter()
            .min()
            .unwrap();
        }
    }

    dp[a_len][b_len]
}

fn main() -> io::Result<()> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let mut lines = input.lines();
    let a = lines.next().unwrap_or("");
    let b = lines.next().unwrap_or("");

    let distance = levenshtein_distance(a, b);
    writeln!(io::stdout(), "{}", distance)?;

    Ok(())
}
```