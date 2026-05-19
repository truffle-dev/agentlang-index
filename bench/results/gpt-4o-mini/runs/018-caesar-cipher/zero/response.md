```zero
=== zero.json ===
{
  "package": { "name": "t_018_caesar_cipher", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/main.0 ===
use lib
import "src/lib.0"

fn main() {
    let shift_str = argv[1]
    let plaintext = argv[2]

    let shift = parse_shift(shift_str)
    if shift == -1 {
        check world.out.write("error\n")
        return
    }

    if plaintext.len() == 0 {
        check world.out.write("error\n")
        return
    }

    let ciphertext = encode(plaintext, shift)
    check world.out.write(ciphertext)
    check world.out.write("\n")
    return
}

fn parse_shift(shift_str: &str) -> i32 {
    let trimmed = shift_str.trim()
    if trimmed.len() == 0 {
        return -1
    }

    let mut value = 0
    for c in trimmed.chars() {
        if c < '0' || c > '9' {
            return -1
        }
        value = value * 10 + (c as i32 - '0' as i32)
    }

    if value < 0 || value > 25 {
        return -1
    }
    return value
}

fn encode(plaintext: &str, shift: i32) -> &str {
    let mut result = ""
    for c in plaintext.chars() {
        if !is_lowercase_letter(c) {
            return "error"
        }
        let shifted = shift_letter(c, shift)
        result.push(shifted)
    }
    return result
}

=== src/lib.0 ===
fn is_lowercase_letter(c: char) -> bool {
    return c >= 'a' && c <= 'z'
}

fn shift_letter(c: char, shift: i32) -> char {
    let base = 'a' as i32
    let new_pos = (c as i32 - base + shift) % 26 + base
    return new_pos as char
}
```