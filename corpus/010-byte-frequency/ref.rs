// Per-byte frequency table, Rust reference.

use std::io::{self, Read, Write};

fn main() {
    let mut data = Vec::new();
    io::stdin().read_to_end(&mut data).expect("read stdin");
    let mut counts = [0u32; 256];
    for &b in &data {
        counts[b as usize] += 1;
    }
    let stdout = io::stdout();
    let mut stdout = stdout.lock();
    for (b, &c) in counts.iter().enumerate() {
        if c > 0 {
            writeln!(stdout, "{} {}", b, c).expect("write stdout");
        }
    }
}
