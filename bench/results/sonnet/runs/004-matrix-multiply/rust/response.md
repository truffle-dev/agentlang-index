```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut iter = input.split_whitespace();

    let n: usize = iter.next().unwrap().parse().unwrap();

    let mut a = vec![vec![0i64; n]; n];
    let mut b = vec![vec![0i64; n]; n];

    for i in 0..n {
        for j in 0..n {
            a[i][j] = iter.next().unwrap().parse().unwrap();
        }
    }
    for i in 0..n {
        for j in 0..n {
            b[i][j] = iter.next().unwrap().parse().unwrap();
        }
    }

    let mut c = vec![vec![0i64; n]; n];
    for i in 0..n {
        for j in 0..n {
            for k in 0..n {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    let mut out = Vec::new();
    for i in 0..n {
        for j in 0..n {
            if j > 0 {
                out.push(b' ');
            }
            write!(out, "{}", c[i][j]).unwrap();
        }
        out.push(b'\n');
    }
    io::stdout().write_all(&out).unwrap();
}
```