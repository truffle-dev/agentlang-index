```zero
const world = import("world")
const std = import("std")

fn main() {
    let line = std.args[1]
    let n = line.len()
    let mut fields = []
    let mut i = 0
    let mut in_quotes = false
    let mut field_start = 0

    while i < n {
        let c = line[i]
        if c == '"' {
            in_quotes = !in_quotes
        } else if c == ',' && !in_quotes {
            fields.push(line[field_start..i])
            field_start = i + 1
        }
        i += 1
    }
    fields.push(line[field_start..n])

    for field in fields {
        check world.out.write(field)
        check world.out.write("\n")
    }
    return
}
```