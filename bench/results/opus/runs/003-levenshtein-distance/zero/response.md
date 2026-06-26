```zero
let std = @import("std")

let main = fn(world: std.World): void {
    let args = std.args(world)
    let a: []u8 = if args.len > 1 { args[1] } else { "" }
    let b: []u8 = if args.len > 2 { args[2] } else { "" }
    let a_len = a.len
    let b_len = b.len

    // prev and curr rows for DP
    var prev: [51]u32 = undefined
    var curr: [51]u32 = undefined

    // Initialize prev row
    var j: u32 = 0
    while j <= b_len {
        prev[j] = j
        j = j + 1
    }

    var i: u32 = 1
    while i <= a_len {
        curr[0] = i
        j = 1
        while j <= b_len {
            let cost: u32 = if a[i - 1] == b[j - 1] { 0 } else { 1 }
            let del = prev[j] + 1
            let ins = curr[j - 1] + 1
            let sub = prev[j - 1] + cost
            let min1 = if del < ins { del } else { ins }
            let min2 = if min1 < sub { min1 } else { sub }
            curr[j] = min2
            j = j + 1
        }
        // copy curr to prev
        j = 0
        while j <= b_len {
            prev[j] = curr[j]
            j = j + 1
        }
        i = i + 1
    }

    let result = prev[b_len]

    // Convert result to decimal string
    var buf: [12]u8 = undefined
    var pos: u32 = 0
    if result == 0 {
        buf[0] = 48
        pos = 1
    } else {
        var tmp: [12]u8 = undefined
        var tmp_pos: u32 = 0
        var val = result
        while val > 0 {
            tmp[tmp_pos] = @intCast(u8, val % 10 + 48)
            tmp_pos = tmp_pos + 1
            val = val / 10
        }
        // reverse
        var k: u32 = 0
        while k < tmp_pos {
            buf[k] = tmp[tmp_pos - 1 - k]
            k = k + 1
        }
        pos = tmp_pos
    }
    buf[pos] = 10
    pos = pos + 1

    check world.out.write(buf[0..pos])
    return
}
```