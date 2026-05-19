```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();

    let shift_line = lines.next().unwrap_or("");
    let plaintext = lines.next().unwrap_or("");

    if let Ok(shift) = shift_line.trim().parse::<u32>() {
        if shift <= 25 && !plaintext.is_empty() && plaintext.chars().all(|c| c.is_ascii_lowercase()) {
            let ciphertext: String = plaintext.chars()
                .map(|c| ((c as u8 - b'a' + shift as u8) % 26 + b'a') as char)
                .collect();
            io::stdout().write_all(ciphertext.as_bytes()).unwrap();
            io::stdout().write_all(b"\n").unwrap();
            return;
        }
    }

    io::stdout().write_all(b"error\n").unwrap();
}
```