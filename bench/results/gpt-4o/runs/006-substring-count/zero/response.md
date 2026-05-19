```zero
use std

fn main() {
    let args = std.args
    if args.len() != 3 {
        check world.out.write("error\n")
        return
    }

    let pattern = args[1]
    let text = args[2]

    let pattern_len = pattern.len()
    let text_len = text.len()

    if pattern_len == 0 || text_len == 0 || pattern_len > text_len {
        check world.out.write("0\n")
        return
    }

    let mut count = 0
    let mut i = 0

    while i <= text_len - pattern_len {
        let mut match = true
        let mut j = 0
        while j < pattern_len {
            if text[i + j] != pattern[j] {
                match = false
                break
            }
            j += 1
        }
        if match {
            count += 1
            i += pattern_len
        } else {
            i += 1
        }
    }

    let count_str = std.str.from_int(count)
    check world.out.write(count_str)
    check world.out.write("\n")
    return
}
```