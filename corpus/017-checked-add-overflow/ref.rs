use std::io::{self, Read, Write};

fn parse_u32(s: &str) -> Option<u32> {
    let t = s.trim();
    if t.is_empty() {
        return None;
    }
    for b in t.bytes() {
        if !(b'0'..=b'9').contains(&b) {
            return None;
        }
    }
    t.parse::<u32>().ok()
}

fn main() {
    let mut input = String::new();
    if io::stdin().read_to_string(&mut input).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let mut lines = input.split('\n');
    let line_a = lines.next();
    let line_b = lines.next();
    let (Some(la), Some(lb)) = (line_a, line_b) else {
        let _ = io::stdout().write_all(b"error\n");
        return;
    };
    let a = parse_u32(la);
    let b = parse_u32(lb);
    match (a, b) {
        (Some(av), Some(bv)) => match av.checked_add(bv) {
            Some(sum) => {
                let _ = writeln!(io::stdout(), "{}", sum);
            }
            None => {
                let _ = io::stdout().write_all(b"error\n");
            }
        },
        _ => {
            let _ = io::stdout().write_all(b"error\n");
        }
    }
}
