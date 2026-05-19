```zero
use std

fn is_balanced(input: Span<u8>) -> bool {
    let mut stack = std.vec.new<u8>()
    let mut i = 0
    while i < input.len() {
        let ch = input[i]
        if ch == b'(' || ch == b'[' || ch == b'{' {
            check stack.push(ch)
        } else if ch == b')' || ch == b']' || ch == b'}' {
            if stack.len() == 0 {
                return false
            }
            let top = stack.pop().unwrap()
            if (ch == b')' && top != b'(') || 
               (ch == b']' && top != b'[') || 
               (ch == b'}' && top != b'{') {
                return false
            }
        }
        i += 1
    }
    return stack.len() == 0
}

fn main() {
    let args = std.args()
    if args.len() != 2 {
        check world.out.write("error\n")
        return
    }
    let input = args[1]
    if is_balanced(input) {
        check world.out.write("yes\n")
    } else {
        check world.out.write("no\n")
    }
    return
}
```