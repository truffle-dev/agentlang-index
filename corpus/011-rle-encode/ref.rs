// Run-length encode the input, Rust reference.

use std::io::{self, Read, Write};

fn main() {
    let mut data = Vec::new();
    io::stdin().read_to_end(&mut data).expect("read stdin");
    if data.is_empty() {
        return;
    }
    let stdout = io::stdout();
    let mut stdout = stdout.lock();
    let mut cur_byte: u8 = data[0];
    let mut cur_count: u32 = 1;
    for &b in &data[1..] {
        if b == cur_byte {
            cur_count += 1;
        } else {
            writeln!(stdout, "{} {}", cur_count, cur_byte).expect("write");
            cur_byte = b;
            cur_count = 1;
        }
    }
    writeln!(stdout, "{} {}", cur_count, cur_byte).expect("write");
}
