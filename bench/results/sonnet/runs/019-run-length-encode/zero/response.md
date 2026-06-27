Looking at this task:
- Read argv[1] as the input (verbatim, may include trailing `\n`)
- Strip `\n`, validate non-empty and all `a`-`z`, then run-length encode
- Lib exports scalar-only functions per the module boundary restriction

```zero
=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/lib.0 ===
pub fn is_lowercase_letter(b: u8) -> bool {
    return b >= 97 && b <= 122
}

pub fn digit_byte(d: u32) -> u8 {
    return (48 + d) as u8
}

pub fn decimal_length(n: u32) -> u32 {
    if n == 0 {
        return 1
    }
    let count: u32 = 0
    let rem: u32 = n
    while rem > 0 {
        count = count + 1
        rem = rem / 10
    }
    return count
}

=== src/main.0 ===
use lib

fn main(world: &World) {
    let args = world.args
    if args.len < 2 {
        check world.out.write("error\n")
        return
    }

    let input = args[1]
    let len: u32 = input.len

    let actual_len: u32 = len
    if len > 0 {
        if input[len - 1] == 10 {
            actual_len = len - 1
        }
    }

    if actual_len == 0 {
        check world.out.write("error\n")
        return
    }

    let vi: u32 = 0
    let valid: bool = true
    while vi < actual_len {
        if !is_lowercase_letter(input[vi]) {
            valid = false
        }
        vi = vi + 1
    }
    if !valid {
        check world.out.write("error\n")
        return
    }

    let buf: [u8; 16384]
    let tmp: [u8; 12]
    let pos: u32 = 0

    let i: u32 = 0
    while i < actual_len {
        let current: u8 = input[i]
        let count: u32 = 1
        i = i + 1
        while i < actual_len && input[i] == current {
            count = count + 1
            i = i + 1
        }

        buf[pos] = current
        pos = pos + 1

        let ti: u32 = 0
        let rem: u32 = count
        while rem > 0 {
            tmp[ti] = digit_byte(rem % 10)
            ti = ti + 1
            rem = rem / 10
        }
        let di: u32 = 0
        while di < ti {
            buf[pos] = tmp[ti - 1 - di]
            pos = pos + 1
            di = di + 1
        }
    }

    buf[pos] = 10
    pos = pos + 1

    check world.out.write(buf[0..pos])
    return
}
```