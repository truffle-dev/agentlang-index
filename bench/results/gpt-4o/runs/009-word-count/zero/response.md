```zero
use std.args
use std.conv
use std.mem
use std.str

fn main() {
    let args = args.collect()
    if args.len() < 2 {
        check world.out.write("0\n")
        return
    }
    
    let input = args[1]
    let mut in_word = false
    let mut word_count = 0

    for byte in input {
        if byte == 0x20 || byte == 0x09 || byte == 0x0A || byte == 0x0D {
            if in_word {
                in_word = false
            }
        } else {
            if !in_word {
                in_word = true
                word_count += 1
            }
        }
    }

    let mut buf = [0; 20]
    let n = utoa(word_count, buf, 10)
    check world.out.write(buf[0..n])
    check world.out.write("\n")
    return
}
```