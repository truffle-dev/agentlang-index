```zero
fn main() void {
    let args = std.args()
    let argc = args.len
    if argc < 2 {
        check world.out.write("error\n")
        return
    }
    let n_str = args[1]
    let n_res = parse_u32(n_str)
    if n_res.err {
        check world.out.write("error\n")
        return
    }
    let n = n_res.val
    if n > 1000 {
        check world.out.write("error\n")
        return
    }
    if argc < n + 2 {
        check world.out.write("error\n")
        return
    }
    let sum: u32 = 0
    let i: u32 = 0
    while i < n {
        let v_str = args[i + 2]
        let v_res = parse_u32(v_str)
        if v_res.err {
            check world.out.write("error\n")
            return
        }
        let v = v_res.val
        if sum > 4294967295 - v {
            check world.out.write("error\n")
            return
        }
        sum = sum + v
        i = i + 1
    }
    check world.out.write(u32_to_str(sum))
    check world.out.write("\n")
    return
}

struct ParseResult {
    val: u32
    err: bool
}

fn parse_u32(s: []u8) ParseResult {
    let len = s.len
    let start = 0
    let end = len
    while end > start {
        if s[end - 1] == 32 {
            end = end - 1
        } else if s[end - 1] == 9 {
            end = end - 1
        } else if s[end - 1] == 13 {
            end = end - 1
        } else if s[end - 1] == 10 {
            end = end - 1
        } else {
            break
        }
    }
    if end == start {
        return ParseResult { .val = 0, .err = true }
    }
    let result: u32 = 0
    let j = start
    while j < end {
        let c = s[j]
        if c < 48 {
            return ParseResult { .val = 0, .err = true }
        }
        if c > 57 {
            return ParseResult { .val = 0, .err = true }
        }
        let digit: u32 = c - 48
        if result > 429496729 {
            return ParseResult { .val = 0, .err = true }
        }
        if result == 429496729 {
            if digit > 5 {
                return ParseResult { .val = 0, .err = true }
            }
        }
        result = result * 10 + digit
        j = j + 1
    }
    return ParseResult { .val = result, .err = false }
}

fn u32_to_str(v: u32) []u8 {
    if v == 0 {
        return "0"
    }
    var buf: [10]u8 = undefined
    let pos = 10
    let n = v
    while n > 0 {
        pos = pos - 1
        buf[pos] = 48 + (n % 10)
        n = n / 10
    }
    return buf[pos..10]
}
```