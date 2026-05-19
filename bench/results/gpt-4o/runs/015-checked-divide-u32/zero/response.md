```zero
use std

fn parse_u32(s: Span<u8>) -> Option<u32> {
    let trimmed = s.trim()
    if trimmed.len() == 0 {
        return none
    }
    let mut value: u32 = 0
    for byte in trimmed {
        if byte < '0' as u8 || byte > '9' as u8 {
            return none
        }
        let digit = (byte - '0' as u8) as u32
        match value.checked_mul(10) {
            some(v) => match v.checked_add(digit) {
                some(v2) => value = v2
                none => return none
            }
            none => return none
        }
    }
    some(value)
}

fn main() -> i32 {
    let args = std.args()
    if args.len() != 3 {
        check world.out.write("error\n")
        return 0
    }

    let a_opt = parse_u32(args[1])
    let b_opt = parse_u32(args[2])

    match (a_opt, b_opt) {
        (some(a), some(b)) => {
            if b == 0 {
                check world.out.write("error\n")
            } else {
                let result = a / b
                check world.out.write_fmt("{}\n", result)
            }
        }
        _ => check world.out.write("error\n")
    }

    return 0
}
```