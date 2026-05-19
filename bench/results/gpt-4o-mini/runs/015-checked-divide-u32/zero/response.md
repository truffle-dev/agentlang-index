```zero
const u32_max = 4294967295

fn parse_u32(s: &str) -> Option<u32> 
    let trimmed = s.trim()
    if trimmed.len() == 0 
        return None
    let mut value = 0u32
    for c in trimmed.chars() 
        if c < '0' || c > '9' 
            return None
        value = value * 10 + (c as u32 - '0' as u32)
        if value > u32_max 
            return None
    return Some(value)

fn main() 
    let args = std.args
    if args.len() != 3 
        check world.out.write("error\n")
        return
    let a_str = args[1]
    let b_str = args[2]
    let a_opt = parse_u32(a_str)
    let b_opt = parse_u32(b_str)
    if a_opt.is_none() || b_opt.is_none() 
        check world.out.write("error\n")
        return
    let a = a_opt.unwrap()
    let b = b_opt.unwrap()
    if b == 0 
        check world.out.write("error\n")
        return
    let result = a / b
    check world.out.write(result.to_string() + "\n")
    return
```