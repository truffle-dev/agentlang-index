```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    if let Err(_) = io::stdin().read_to_string(&mut input) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let lines: Vec<&str> = input.lines().collect();
    if lines.len() < 2 {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let shift_str = lines[0].trim();
    let plaintext = lines[1];

    let shift: usize = match shift_str.parse() {
        Ok(num) if num <= 25 => num,
        _ => {
            let _ = io::stdout().write_all(b"error\n");
            return;
        }
    };

    if plaintext.is_empty() || !plaintext.chars().all(|c| c.is_ascii_lowercase()) {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }

    let ciphertext: String = plaintext
        .chars()
        .map(|c| {
            let shifted = ((c as usize - 'a' as usize + shift) % 26) + 'a' as usize;
            shifted as u8 as char
        })
        .collect();

    let _ = io::stdout().write_all(ciphertext.as_bytes());
    let _ = io::stdout().write_all(b"\n");
}
```