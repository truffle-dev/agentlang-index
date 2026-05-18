// Square integer matrix multiply, Rust reference.
// Reads N, then N rows of A, then N rows of B, prints C = A * B.
use std::io::{self, Read, Write};
use std::process::ExitCode;

fn main() -> ExitCode {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = writeln!(io::stderr(), "failed to read stdin");
        return ExitCode::from(1);
    }
    let mut iter = input.split_ascii_whitespace();
    let n: i64 = match iter.next().and_then(|t| t.parse().ok()) {
        Some(v) if (1..=5).contains(&v) => v,
        _ => {
            let _ = writeln!(io::stderr(), "N must be in [1, 5]");
            return ExitCode::from(1);
        }
    };
    let n = n as usize;
    let read_matrix = |it: &mut std::str::SplitAsciiWhitespace| -> Option<Vec<Vec<i32>>> {
        let mut m = vec![vec![0i32; n]; n];
        for i in 0..n {
            for j in 0..n {
                let v: i32 = it.next()?.parse().ok()?;
                m[i][j] = v;
            }
        }
        Some(m)
    };
    let a = match read_matrix(&mut iter) {
        Some(m) => m,
        None => {
            let _ = writeln!(io::stderr(), "failed to read A");
            return ExitCode::from(1);
        }
    };
    let b = match read_matrix(&mut iter) {
        Some(m) => m,
        None => {
            let _ = writeln!(io::stderr(), "failed to read B");
            return ExitCode::from(1);
        }
    };
    let mut out = String::new();
    for i in 0..n {
        for j in 0..n {
            let mut s: i32 = 0;
            for k in 0..n {
                s += a[i][k] * b[k][j];
            }
            if j > 0 {
                out.push(' ');
            }
            out.push_str(&s.to_string());
        }
        out.push('\n');
    }
    let _ = io::stdout().write_all(out.as_bytes());
    ExitCode::SUCCESS
}
