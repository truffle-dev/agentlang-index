// Reverse the order of words on a line, Rust reference.

use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    if input.ends_with('\n') {
        input.pop();
    }
    let words: Vec<&str> = input.split(' ').filter(|w| !w.is_empty()).collect();
    if words.is_empty() {
        return;
    }
    let mut out = String::with_capacity(input.len() + 1);
    for (i, w) in words.iter().rev().enumerate() {
        if i > 0 {
            out.push(' ');
        }
        out.push_str(w);
    }
    out.push('\n');
    let stdout = io::stdout();
    let mut h = stdout.lock();
    h.write_all(out.as_bytes()).unwrap();
}
