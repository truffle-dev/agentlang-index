use std::io::{self, Read, Write};

fn is_lowercase_letter(b: u8) -> bool {
    (b'a'..=b'z').contains(&b)
}

fn shift_letter(b: u8, shift: u8) -> u8 {
    let zero_based = b - b'a';
    b'a' + ((zero_based + shift) % 26)
}

fn parse_shift(s: &str) -> Option<u8> {
    let t = s.trim();
    if t.is_empty() {
        return None;
    }
    for b in t.bytes() {
        if !(b'0'..=b'9').contains(&b) {
            return None;
        }
    }
    let v: u32 = t.parse().ok()?;
    if v > 25 {
        return None;
    }
    Some(v as u8)
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let mut lines = input.split('\n');
    let line_shift = lines.next();
    let line_text = lines.next();
    let (Some(ls), Some(lt)) = (line_shift, line_text) else {
        let _ = io::stdout().write_all(b"error\n");
        return;
    };
    let shift = match parse_shift(ls) {
        Some(v) => v,
        None => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };
    let text_bytes = lt.as_bytes();
    if text_bytes.is_empty() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let mut out = Vec::with_capacity(text_bytes.len() + 1);
    for &b in text_bytes {
        if !is_lowercase_letter(b) {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
        out.push(shift_letter(b, shift));
    }
    out.push(b'\n');
    let _ = io::stdout().write_all(&out);
}
