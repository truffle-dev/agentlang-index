// Non-overlapping substring count, Rust reference.
// Reads pattern P from line 1 of stdin and text T from line 2.

use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.split('\n');
    let p = lines.next().unwrap_or("");
    let t = lines.next().unwrap_or("");
    let mut count: u64 = 0;
    if !p.is_empty() {
        let pb = p.as_bytes();
        let tb = t.as_bytes();
        let m = pb.len();
        let n = tb.len();
        if m <= n {
            let mut i = 0;
            while i + m <= n {
                if &tb[i..i + m] == pb {
                    count += 1;
                    i += m;
                } else {
                    i += 1;
                }
            }
        }
    }
    let out = io::stdout();
    let mut h = out.lock();
    writeln!(h, "{}", count).unwrap();
}
