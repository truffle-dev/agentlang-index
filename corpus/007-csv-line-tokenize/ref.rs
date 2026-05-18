// CSV line tokenizer (RFC 4180 subset), Rust reference.

use std::io::{self, Read, Write};

const FIELD_START: u8 = 0;
const IN_UNQUOTED: u8 = 1;
const IN_QUOTED: u8 = 2;
const AFTER_CLOSING_QUOTE: u8 = 3;

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    if input.ends_with('\n') {
        input.pop();
    }
    let mut out: Vec<u8> = Vec::with_capacity(input.len() + 64);
    let mut state = FIELD_START;
    if !input.is_empty() {
        for ch in input.bytes() {
            match state {
                FIELD_START => {
                    if ch == b'"' {
                        state = IN_QUOTED;
                    } else if ch == b',' {
                        out.push(b'\n');
                    } else {
                        out.push(ch);
                        state = IN_UNQUOTED;
                    }
                }
                IN_UNQUOTED => {
                    if ch == b',' {
                        out.push(b'\n');
                        state = FIELD_START;
                    } else {
                        out.push(ch);
                    }
                }
                IN_QUOTED => {
                    if ch == b'"' {
                        state = AFTER_CLOSING_QUOTE;
                    } else {
                        out.push(ch);
                    }
                }
                AFTER_CLOSING_QUOTE => {
                    if ch == b'"' {
                        out.push(b'"');
                        state = IN_QUOTED;
                    } else if ch == b',' {
                        out.push(b'\n');
                        state = FIELD_START;
                    }
                }
                _ => unreachable!(),
            }
        }
        out.push(b'\n');
    }
    let stdout = io::stdout();
    let mut h = stdout.lock();
    h.write_all(&out).unwrap();
}
