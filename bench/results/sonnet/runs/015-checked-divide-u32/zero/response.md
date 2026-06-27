```zero
fn main() {
    let args = std.args
    if args.len < 3 {
        check world.out.write("error\n")
        return
    }
    let a_str = args[1]
    let b_str = args[2]
    let a_res = u32.parse(a_str)
    let b_res = u32.parse(b_str)
    if a_res.is_err {
        check world.out.write("error\n")
        return
    }
    if b_res.is_err {
        check world.out.write("error\n")
        return
    }
    let a = a_res.value
    let b = b_res.value
    if b == 0 {
        check world.out.write("error\n")
        return
    }
    let q = a / b
    let buf = [16]u8
    let n = u32.format(q, buf[0..16])
    check world.out.write(buf[0..n])
    check world.out.write("\n")
    return
}
```