// Count whitespace-separated tokens in input, Rust reference.

use std::io::{self, Read, Write};

fn main() {
    let mut data = Vec::new();
    io::stdin().read_to_end(&mut data).expect("read stdin");
    let mut count: u32 = 0;
    let mut in_word = false;
    for &b in &data {
        let is_ws = b == 32 || b == 9 || b == 10 || b == 13;
        if is_ws {
            in_word = false;
        } else if !in_word {
            count += 1;
            in_word = true;
        }
    }
    let mut stdout = io::stdout();
    writeln!(stdout, "{}", count).expect("write stdout");
}
