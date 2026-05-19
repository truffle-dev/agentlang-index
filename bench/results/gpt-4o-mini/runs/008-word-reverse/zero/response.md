```zero
const world = check world.out

fn main() {
    let args = std.args
    let input = args[1]
    let len = input.len()
    let mut words = []
    let mut start = 0
    let mut in_word = false

    while start < len {
        if input[start] != 0x20 {
            if !in_word {
                in_word = true
                let mut end = start
                while end < len && input[end] != 0x20 {
                    end += 1
                }
                words.push(input[start..end])
                start = end
            } else {
                start += 1
            }
        } else {
            if in_word {
                in_word = false
            }
            start += 1
        }
    }

    let word_count = words.len()
    if word_count > 0 {
        for i in (0..word_count).rev() {
            check world.write(words[i])
            if i > 0 {
                check world.write(" ")
            }
        }
        check world.write("\n")
    }
    return
}
```