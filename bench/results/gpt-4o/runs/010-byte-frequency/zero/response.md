```zero
use std.args
use std.conv
use std.mem
use std.os

fn main() {
    let args = args.collect()
    if args.len() != 2 {
        check world.out.write("error\n")
        return
    }

    let input = args[1]
    let mut counts = [0u64; 256]

    let mut i = 0
    while i < input.len() {
        let byte = input[i]
        counts[byte as usize] += 1
        i += 1
    }

    let mut buf = [0u8; 32]
    let mut j = 0
    while j < 256 {
        if counts[j] > 0 {
            let n = itoa(j, &mut buf)
            check world.out.write(buf[0..n])
            check world.out.write(" ")
            let n = itoa(counts[j], &mut buf)
            check world.out.write(buf[0..n])
            check world.out.write("\n")
        }
        j += 1
    }

    return
}

fn itoa(mut num: u64, buf: &mut [u8]) -> usize {
    let mut i = buf.len()
    if num == 0 {
        i -= 1
        buf[i] = '0' as u8
    } else {
        while num > 0 {
            i -= 1
            buf[i] = (num % 10 + '0' as u64) as u8
            num /= 10
        }
    }
    let len = buf.len() - i
    let mut j = 0
    while j < len {
        buf[j] = buf[i + j]
        j += 1
    }
    len
}
```