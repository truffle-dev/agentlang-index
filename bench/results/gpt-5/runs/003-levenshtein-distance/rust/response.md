```rust
use std::io::{self, Read, Write};

fn levenshtein(a: &[u8], b: &[u8]) -> usize {
    let m = a.len();
    let n = b.len();
    if m == 0 {
        return n;
    }
    if n == 0 {
        return m;
    }

    let mut prev: Vec<usize> = (0..=n).collect();
    let mut curr: Vec<usize> = vec![0; n + 1];

    for i in 1..=m {
        curr[0] = i;
        let ai = a[i - 1];
        for j in 1..=n {
            let cost = if ai == b[j - 1] { 0 } else { 1 };
            let del = prev[j] + 1;
            let ins = curr[j - 1] + 1;
            let sub = prev[j - 1] + cost;
            curr[j] = del.min(ins).min(sub);
        }
        std::mem::swap(&mut prev, &mut curr);
    }
    prev[n]
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        input.clear();
    }

    let (mut a, mut b) = if let Some(pos) = input.find('\n') {
        let first = input[..pos].to_string();
        let rest = &input[pos + 1..];
        let second = if let Some(pos2) = rest.find('\n') {
            rest[..pos2].to_string()
        } else {
            rest.to_string()
        };
        (first, second)
    } else {
        (input, String::new())
    };

    if a.as_bytes().last() == Some(&b'\r') {
        a.pop();
    }
    if b.as_bytes().last() == Some(&b'\r') {
        b.pop();
    }

    let dist = levenshtein(a.as_bytes(), b.as_bytes());
    let out = format!("{}\n", dist);
    let _ = io::stdout().write_all(out.as_bytes());
}
```