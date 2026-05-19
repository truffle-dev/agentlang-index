```zero
use std

fn levenshtein_distance(a: Span<u8>, b: Span<u8>) -> u32 {
    let len_a = a.len()
    let len_b = b.len()

    if len_a == 0 {
        return len_b as u32
    }
    if len_b == 0 {
        return len_a as u32
    }

    let mut dp = std.heap.alloc((len_a + 1) * (len_b + 1) * std.mem.size_of::<u32>()) as *mut u32

    for i in 0..=len_a {
        unsafe { *dp.add(i * (len_b + 1)) = i as u32 }
    }
    for j in 0..=len_b {
        unsafe { *dp.add(j) = j as u32 }
    }

    for i in 1..=len_a {
        for j in 1..=len_b {
            let cost = if a[i - 1] == b[j - 1] { 0 } else { 1 }
            let deletion = unsafe { *dp.add((i - 1) * (len_b + 1) + j) } + 1
            let insertion = unsafe { *dp.add(i * (len_b + 1) + (j - 1)) } + 1
            let substitution = unsafe { *dp.add((i - 1) * (len_b + 1) + (j - 1)) } + cost

            unsafe {
                *dp.add(i * (len_b + 1) + j) = std.math.min(deletion, std.math.min(insertion, substitution))
            }
        }
    }

    let result = unsafe { *dp.add(len_a * (len_b + 1) + len_b) }
    std.heap.dealloc(dp)
    return result
}

fn main() -> u32 {
    let args = std.args()
    if args.len() != 3 {
        check world.out.write("error\n")
        return 0
    }

    let a = args[1]
    let b = args[2]

    let distance = levenshtein_distance(a, b)
    let mut buf = [0u8; 12]
    let n = std.fmt.utoa(distance, &mut buf)
    check world.out.write(buf[0..n])
    check world.out.write("\n")
    return 0
}
```