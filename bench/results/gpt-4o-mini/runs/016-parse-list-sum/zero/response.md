```zero
const u32_max = 4294967295

fn parse_u32(s: &str) -> Option<u32> {
    let mut value = 0u32
    for c in s.chars() {
        if c < '0' || c > '9' {
            return none
        }
        value = value * 10 + (c as u32 - '0' as u32)
        if value > u32_max {
            return none
        }
    }
    some(value)
}

fn main() {
    let args = std.args
    let n_str = args[1].trim()
    let n_opt = parse_u32(n_str)
    if n_opt.is_none() {
        check world.out.write("error\n")
        return
    }
    let n = n_opt.unwrap()
    if n > 1000 {
        check world.out.write("error\n")
        return
    }
    let mut sum = 0u32
    for i in 2..(2 + n) {
        if i >= args.len() {
            check world.out.write("error\n")
            return
        }
        let value_str = args[i].trim()
        let value_opt = parse_u32(value_str)
        if value_opt.is_none() {
            check world.out.write("error\n")
            return
        }
        let value = value_opt.unwrap()
        if sum > u32_max - value {
            check world.out.write("error\n")
            return
        }
        sum += value
    }
    check world.out.write((sum.to_string() + "\n").as_str())
    return
}
```