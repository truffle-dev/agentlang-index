use std::io::{self, Read, Write};

const U32_MAX_U64: u64 = 4294967295;
const N_MAX: u32 = 1000;

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

fn run() -> Option<u64> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok()?;
    let mut lines = input.split('\n');
    let n_line = lines.next()?;
    let n = parse_u32(n_line)?;
    if n > N_MAX {
        return None;
    }
    let mut total: u64 = 0;
    for _ in 0..n {
        let line = lines.next()?;
        let v = parse_u32(line)? as u64;
        total += v;
        if total > U32_MAX_U64 {
            return None;
        }
    }
    Some(total)
}

fn main() {
    let stdout = io::stdout();
    let mut out = stdout.lock();
    match run() {
        Some(total) => {
            let _ = writeln!(out, "{}", total);
        }
        None => {
            let _ = out.write_all(b"error\n");
        }
    }
}
