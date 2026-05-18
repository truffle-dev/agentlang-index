// Balanced bracket checker, Rust reference.
// Reads one line of printable ASCII (up to 1000 chars), prints `yes` or `no`.

use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    if input.ends_with('\n') {
        input.pop();
    }
    let mut stack: Vec<char> = Vec::new();
    let mut balanced = true;
    for ch in input.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' => {
                if stack.pop() != Some('(') {
                    balanced = false;
                    break;
                }
            }
            ']' => {
                if stack.pop() != Some('[') {
                    balanced = false;
                    break;
                }
            }
            '}' => {
                if stack.pop() != Some('{') {
                    balanced = false;
                    break;
                }
            }
            _ => {}
        }
    }
    let out = io::stdout();
    let mut h = out.lock();
    if balanced && stack.is_empty() {
        h.write_all(b"yes\n").unwrap();
    } else {
        h.write_all(b"no\n").unwrap();
    }
}
