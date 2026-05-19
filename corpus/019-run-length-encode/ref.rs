use std::io::{self, Read, Write};

fn is_lowercase_letter(b: u8) -> bool {
    (b'a'..=b'z').contains(&b)
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let mut lines = input.split('\n');
    let line_text = lines.next();
    let Some(lt) = line_text else {
        let _ = io::stdout().write_all(b"error\n");
        return;
    };
    let text_bytes = lt.as_bytes();
    if text_bytes.is_empty() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    for &b in text_bytes {
        if !is_lowercase_letter(b) {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    }
    let mut out: Vec<u8> = Vec::with_capacity(text_bytes.len() * 2 + 1);
    let mut i = 0usize;
    while i < text_bytes.len() {
        let run_byte = text_bytes[i];
        let mut run_len = 1usize;
        let mut j = i + 1;
        while j < text_bytes.len() && text_bytes[j] == run_byte {
            run_len += 1;
            j += 1;
        }
        out.push(run_byte);
        out.extend_from_slice(run_len.to_string().as_bytes());
        i = j;
    }
    out.push(b'\n');
    let _ = io::stdout().write_all(&out);
}
