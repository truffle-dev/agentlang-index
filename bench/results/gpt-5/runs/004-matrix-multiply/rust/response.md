```rust
use std::fmt::Write as FmtWrite;
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let mut iter = input.split_whitespace();
    let n_token = match iter.next() {
        Some(t) => t,
        None => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    let n: usize = match n_token.parse() {
        Ok(x) => x,
        Err(_) => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    if n == 0 || n > 5 {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let rest: Vec<&str> = iter.collect();
    let expected = 2 * n * n;
    if rest.len() != expected {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let mut a = vec![0i32; n * n];
    let mut b = vec![0i32; n * n];

    for idx in 0..(n * n) {
        match rest[idx].parse::<i32>() {
            Ok(v) => a[idx] = v,
            Err(_) => {
                let _ = io::stdout().write_all(b"error\n");
                return;
            }
        }
    }

    for idx in 0..(n * n) {
        match rest[n * n + idx].parse::<i32>() {
            Ok(v) => b[idx] = v,
            Err(_) => {
                let _ = io::stdout().write_all(b"error\n");
                return;
            }
        }
    }

    let mut c = vec![0i32; n * n];

    for i in 0..n {
        for k in 0..n {
            let aik = a[i * n + k];
            let row = i * n;
            for j in 0..n {
                c[row + j] += aik * b[k * n + j];
            }
        }
    }

    let mut out = String::new();
    for i in 0..n {
        for j in 0..n {
            if j > 0 {
                out.push(' ');
            }
            let _ = write!(&mut out, "{}", c[i * n + j]);
        }
        out.push('\n');
    }

    let _ = io::stdout().write_all(out.as_bytes());
}
```