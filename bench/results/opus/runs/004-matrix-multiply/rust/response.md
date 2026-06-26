```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_whitespace();
    let n: usize = it.next().unwrap().parse().unwrap();
    let mut a = vec![0i64; n * n];
    let mut b = vec![0i64; n * n];
    for v in a.iter_mut() { *v = it.next().unwrap().parse().unwrap(); }
    for v in b.iter_mut() { *v = it.next().unwrap().parse().unwrap(); }
    let mut out = Vec::new();
    for i in 0..n {
        for j in 0..n {
            if j > 0 { out.push(b' '); }
            let mut s: i64 = 0;
            for k in 0..n { s += a[i * n + k] * b[k * n + j]; }
            write!(out, "{}", s).unwrap();
        }
        out.push(b'\n');
    }
    io::stdout().write_all(&out).unwrap();
}
```