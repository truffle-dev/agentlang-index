```zero
const whitespace = [0x20, 0x09, 0x0A, 0x0D]

fn is_whitespace(b: u8) -> bool
    for w in whitespace
        if b == w
            return true
    return false

fn main()
    let args = std.args
    let input = args[1]
    let len = input.len
    let mut count = 0
    let mut in_word = false

    for i in 0..len
        if is_whitespace(input[i])
            if in_word
                in_word = false
        else
            if not in_word
                count += 1
                in_word = true

    check world.out.write(count.to_string().bytes())
    check world.out.write([0x0A])
    return
```