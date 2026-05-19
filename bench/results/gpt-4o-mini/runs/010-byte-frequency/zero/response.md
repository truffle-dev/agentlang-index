```zero
const world = import("world")

fn main() {
    let args = std.args
    let input = args[1]
    let counts = [0u64; 256]

    for i in 0..input.len() {
        let byte = input[i]
        counts[byte as usize] += 1
    }

    for i in 0..256 {
        if counts[i] > 0 {
            check world.out.write(i.to_string() + " " + counts[i].to_string() + "\n")
        }
    }

    return
}
```