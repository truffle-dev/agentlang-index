```zero
use std

fn parse_csv_line(line: Span<u8>) -> Vec<Span<u8>> {
    let mut fields = Vec::new()
    let mut i = 0
    let mut start = 0
    let mut in_quotes = false
    let mut field = Vec::new()

    while i < line.len() {
        let c = line[i]
        if in_quotes {
            if c == '"' {
                if i + 1 < line.len() && line[i + 1] == '"' {
                    field.push(c)
                    i += 1
                } else {
                    in_quotes = false
                }
            } else {
                field.push(c)
            }
        } else {
            if c == ',' {
                fields.push(Span::from_vec(field))
                field = Vec::new()
                start = i + 1
            } else if c == '"' {
                in_quotes = true
            } else {
                field.push(c)
            }
        }
        i += 1
    }
    fields.push(Span::from_vec(field))
    return fields
}

fn main() {
    let args = std.args()
    if args.len() < 2 {
        return
    }
    let line = args[1]
    let fields = parse_csv_line(line)
    for field in fields {
        check world.out.write(field)
        check world.out.write("\n")
    }
    return
}
```