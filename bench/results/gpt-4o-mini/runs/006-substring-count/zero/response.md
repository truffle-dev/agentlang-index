```zero
let main = 
    let args = std.args
    let pattern = args[1]
    let text = args[2]
    let pattern_len = pattern.len()
    let text_len = text.len()
    let mut count = 0
    let mut i = 0

    while i <= text_len - pattern_len 
        if text[i..i + pattern_len] == pattern 
            count += 1
            i += pattern_len 
        else 
            i += 1

    check world.out.write(count.to_string().bytes())
    check world.out.write("\n".bytes())
    return
```