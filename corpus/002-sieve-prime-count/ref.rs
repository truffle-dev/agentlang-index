// Prime count via Sieve of Eratosthenes, Rust reference.
// Reads N from stdin, runs a byte-flag sieve, counts unmarked [2, N].
use std::io::{self, Read, Write};
use std::process::ExitCode;

fn main() -> ExitCode {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = writeln!(io::stderr(), "failed to read stdin");
        return ExitCode::from(1);
    }
    let n: i64 = match input.trim().parse() {
        Ok(v) if v >= 0 => v,
        _ => {
            let _ = writeln!(io::stderr(), "N must be a non-negative integer");
            return ExitCode::from(1);
        }
    };
    let n_usize = n as usize;
    let count = if n < 2 {
        0
    } else {
        let mut composite = vec![0u8; n_usize + 1];
        let mut i: usize = 2;
        while i * i <= n_usize {
            if composite[i] == 0 {
                let mut j = i * i;
                while j <= n_usize {
                    composite[j] = 1;
                    j += i;
                }
            }
            i += 1;
        }
        (2..=n_usize).filter(|&k| composite[k] == 0).count()
    };
    let _ = writeln!(io::stdout(), "{}", count);
    ExitCode::SUCCESS
}
