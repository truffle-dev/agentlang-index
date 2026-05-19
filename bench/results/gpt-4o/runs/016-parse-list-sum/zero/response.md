```zero
use std.conv
use std.args
use std.u32
use std.str

fn main() {
    let args = args.collect()
    if args.len() < 2 {
        check world.out.write("error\n")
        return
    }

    let n_result = parse_u32(args[1])
    if n_result.is_none() {
        check world.out.write("error\n")
        return
    }

    let n = n_result.unwrap()
    if n > 1000 || args.len() != n + 2 {
        check world.out.write("error\n")
        return
    }

    let mut sum: u64 = 0
    for i in 2..(n + 2) {
        let value_result = parse_u32(args[i])
        if value_result.is_none() {
            check world.out.write("error\n")
            return
        }

        let value = value_result.unwrap()
        sum += value as u64
        if sum > 4294967295 {
            check world.out.write("error\n")
            return
        }
    }

    let sum_str = u32_to_str(sum as u32)
    check world.out.write(sum_str)
    check world.out.write("\n")
    return
}

fn parse_u32(s: str) -> Option<u32> {
    let trimmed = str.trim(s)
    if trimmed.len() == 0 {
        return none
    }

    let mut result: u64 = 0
    for c in trimmed.bytes() {
        if c < '0' as u8 || c > '9' as u8 {
            return none
        }
        result = result * 10 + (c - '0' as u8) as u64
        if result > 4294967295 {
            return none
        }
    }

    return some(result as u32)
}

fn u32_to_str(value: u32) -> str {
    let mut buf = [0u8; 10]
    let mut i = 10
    let mut v = value
    while v > 0 {
        i -= 1
        buf[i] = '0' as u8 + (v % 10) as u8
        v /= 10
    }
    if value == 0 {
        i -= 1
        buf[i] = '0' as u8
    }
    return str.from_utf8(buf[i..10])
}
```