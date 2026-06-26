```zero
const std = @import("std")

pub fn main() void {
    const args = std.args()
    if args.len() < 3 {
        check world.out.write("error\n")
        return
    }
    const a_str = args[1].trim()
    const b_str = args[2].trim()
    const a = parse_u32(a_str)
    const b = parse_u32(b_str)
    if a == null {
        check world.out.write("error\n")
        return
    }
    if b == null {
        check world.out.write("error\n")
        return
    }
    const av = a.?
    const bv = b.?
    if bv == 0 {
        check world.out.write("error\n")
        return
    }
    const result = av / bv
    var buf: [20]u8 = undefined
    const n = u32_to_str(result, &buf)
    check world.out.write(buf[0..n])
    check world.out.write("\n")
    return
}

fn parse_u32(s: []const u8) ?u32 {
    if s.len() == 0 {
        return null
    }
    var result: u64 = 0
    var i: usize = 0
    while i < s.len() {
        const c = s[i]
        if c < 48 {
            return null
        }
        if c > 57 {
            return null
        }
        result = result * 10 + @as(u64, c - 48)
        if result > 4294967295 {
            return null
        }
        i = i + 1
    }
    return @as(u32, @truncate(result))
}

fn u32_to_str(val: u32, buf: *[20]u8) usize {
    if val == 0 {
        buf[0] = 48
        return 1
    }
    var v = val
    var i: usize = 0
    while v > 0 {
        buf[i] = @as(u8, @truncate(v % 10)) + 48
        v = v / 10
        i = i + 1
    }
    var lo: usize = 0
    var hi: usize = i - 1
    while lo < hi {
        const tmp = buf[lo]
        buf[lo] = buf[hi]
        buf[hi] = tmp
        lo = lo + 1
        hi = hi - 1
    }
    return i
}
```