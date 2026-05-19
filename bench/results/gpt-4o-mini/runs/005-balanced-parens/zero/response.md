```zero
const openers = "([{"
const closers = ")]}"
const matching = { '(': ')', '[': ']', '{': '}' }

fn is_balanced(s: Span<u8>) -> bool
    let stack = []
    for c in s
        if openers.contains(c)
            stack.push(c)
        else if closers.contains(c)
            if stack.is_empty() or matching[stack.pop()] != c
                return false
    return stack.is_empty()

fn main() -> i32
    let input = std.args[1]
    let result = is_balanced(input)
    if result
        check world.out.write("yes\n")
    else
        check world.out.write("no\n")
    return 0
```