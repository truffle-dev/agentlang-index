```zero
const world = import("world")

fn main() {
    let input = std.args[1]
    let n = input.len()
    if n == 0 {
        return
    }
    
    let mut count = 1
    let mut byte = input[0]
    
    for i in 1..n {
        if input[i] == byte {
            count += 1
        } else {
            check world.out.write(count.to_string() + " " + byte.to_string() + "\n")
            byte = input[i]
            count = 1
        }
    }
    
    check world.out.write(count.to_string() + " " + byte.to_string() + "\n")
    return
}
```