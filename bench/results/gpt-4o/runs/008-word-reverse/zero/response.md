```zero
use std

fn main() {
    let args = std.args()
    if args.len() != 2 {
        check world.out.write("")
        return
    }

    let input = args[1]
    let mut words = std.vec::Vec::<std.str>::new()
    let mut start = 0
    let mut in_word = false

    for i in 0..input.len() {
        if input[i] != 0x20 {
            if !in_word {
                start = i
                in_word = true
            }
        } else {
            if in_word {
                words.push(input[start..i].to_string())
                in_word = false
            }
        }
    }

    if in_word {
        words.push(input[start..input.len()].to_string())
    }

    if words.len() == 0 {
        check world.out.write("")
        return
    }

    let mut output = std.str::new()
    for i in (0..words.len()).rev() {
        if i != words.len() - 1 {
            output.push(' ')
        }
        output.push_str(words[i])
    }
    output.push('\n')

    check world.out.write(output)
    return
}
```