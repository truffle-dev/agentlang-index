// Levenshtein edit distance, Rust reference.
// Reads A and B from stdin (one per line), runs a two-row DP.
use std::io::{self, Read, Write};
use std::process::ExitCode;

fn main() -> ExitCode {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = writeln!(io::stderr(), "failed to read stdin");
        return ExitCode::from(1);
    }
    let mut lines = input.split('\n');
    let a = lines.next().unwrap_or("");
    let b = lines.next().unwrap_or("");
    if a.chars().count() > 50 || b.chars().count() > 50 {
        let _ = writeln!(io::stderr(), "each string must be at most 50 characters");
        return ExitCode::from(1);
    }
    let a_bytes = a.as_bytes();
    let b_bytes = b.as_bytes();
    let m = a_bytes.len();
    let n = b_bytes.len();
    let mut prev: Vec<u32> = (0..=n as u32).collect();
    let mut curr: Vec<u32> = vec![0; n + 1];
    for i in 0..m {
        curr[0] = (i + 1) as u32;
        for k in 0..n {
            let del_cost = prev[k + 1] + 1;
            let ins_cost = curr[k] + 1;
            let sub_cost = prev[k] + if a_bytes[i] == b_bytes[k] { 0 } else { 1 };
            curr[k + 1] = del_cost.min(ins_cost).min(sub_cost);
        }
        std::mem::swap(&mut prev, &mut curr);
    }
    let _ = writeln!(io::stdout(), "{}", prev[n]);
    ExitCode::SUCCESS
}
