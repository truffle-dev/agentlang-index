```
=== zero.json ===
{
  "package": { "name": "t_018_caesar_cipher", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/main.0 ===
use lib

export fn main(argv: [[u8]]) -> void {
    if argv.len() != 3 {
        check world.out.write("error\n")
        return
    }

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

    let mut ciphertext = alloc(plaintext.len())
    for byte in plaintext {
        if !lib.is_lowercase_letter(byte) {
            check world.out.write("error\n")
            return
        }
        let shifted = lib.shift_letter(byte, shift)
        check ciphertext.push(shifted)
    }

    check ciphertext.push('\n' as u8)
    check world.out.write(ciphertext)
}

fn parse_shift(shift_str: [u8]) -> i32 {
    let trimmed = shift_str.trim()
    if trimmed.len() == 0 {
        return -1
    }

    let mut shift = 0
    for byte in trimmed {
        if byte < '0' as u8 || byte > '9' as u8 {
            return -1
        }
        shift = shift * 10 + (byte - '0' as u8) as i32
        if shift > 25 {
            return -1
        }
    }
    return shift
}

=== src/lib.0 ===
export fn is_lowercase_letter(byte: u8) -> bool {
    return byte >= 'a' as u8 && byte <= 'z' as u8
}

export fn shift_letter(byte: u8, shift: i32) -> u8 {
    return ((byte - 'a' as u8 + shift as u8) % 26) + 'a' as u8
}
```