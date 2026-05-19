```rust
use std::io::{self, Read, Write};

const BASE: u32 = 1_000_000_000;

fn add_big(a: &[u32], b: &[u32]) -> Vec<u32> {
    let mut res = Vec::with_capacity(a.len().max(b.len()) + 1);
    let mut carry: u64 = 0;
    let mut i = 0usize;
    while i < a.len() || i < b.len() || carry != 0 {
        let av = if i < a.len() { a[i] as u64 } else { 0 };
        let bv = if i < b.len() { b[i] as u64 } else { 0 };
        let sum = av + bv + carry;
        res.push((sum % (BASE as u64)) as u32);
        carry = sum / (BASE as u64);
        i += 1;
    }
    // Ensure zero is represented as empty vector.
    if res.len() == 1 && res[0] == 0 {
        res.clear();
    }
    res
}

fn big_to_string(v: &[u32]) -> String {
    if v.is_empty() {
        return "0".to_string();
    }
    let mut s = String::new();
    let mut it = v.iter().rev();
    if let Some(&first) = it.next() {
        s.push_str(&first.to_string());
        for &chunk in it {
            s.push_str(&format!("{:09}", chunk));
        }
    }
    s
}

fn fib_str(n: usize) -> String {
    let mut memo: Vec<Vec<u32>> = Vec::with_capacity(n + 1);
    // fib(0) = 0 -> empty vec represents 0
    memo.push(Vec::new());
    if n >= 1 {
        memo.push(vec![1]); // fib(1) = 1
    }
    for i in 2..=n {
        let next = add_big(&memo[i - 1], &memo[i - 2]);
        memo.push(next);
    }
    big_to_string(&memo[n])
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let s = input.trim();
    let n: usize = match s.parse() {
        Ok(v) => v,
        Err(_) => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    let mut out = fib_str(n);
    out.push('\n');
    let _ = io::stdout().write_all(out.as_bytes());
}
```