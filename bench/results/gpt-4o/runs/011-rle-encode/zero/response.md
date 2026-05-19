```zero
use std

fn main() {
    let args = std.args
    if args.len() != 2 {
        check world.out.write("error\n")
        return
    }

    let input = args[1]
    let mut i = 0
    let len = input.len()

    while i < len {
        let current_byte = input[i]
        let mut count = 1
        i += 1

        while i < len && input[i] == current_byte {
            count += 1
            i += 1
        }

        let mut buf = [0u8; 20]
        let mut n = 0

        n += std.fmt.u64_to_decimal(buf[n..], count as u64)
        buf[n] = 0x20
        n += 1
        n += std.fmt.u64_to_decimal(buf[n..], current_byte as u64)
        buf[n] = 0x0A
        n += 1

        check world.out.write(buf[0..n])
    }

    return
}
```