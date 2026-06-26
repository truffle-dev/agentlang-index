```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let a: Vec<u8> = lines.next().unwrap_or("").as_bytes().to_vec();
    let b: Vec<u8> = lines.next().unwrap_or("").as_bytes().to_vec();
    let n = a.len();
    let m = b.len();
    let mut prev = (0..=m).collect::<Vec<usize>>();
    let mut curr = vec![0usize; m + 1];
    for i in 1..=n {
        curr[0] = i;
        for j in 1..=m {
            let cost = if a[i - 1] == b[j - 1] { 0 } else { 1 };
            curr[j] = (prev[j] + 1).min(curr[j - 1] + 1).min(prev[j - 1] + cost);
        }
        std::mem::swap(&mut prev, &mut curr);
    }
    io::stdout().write_all(format!("{}\n", prev[m]).as_bytes()).unwrap();
}
```