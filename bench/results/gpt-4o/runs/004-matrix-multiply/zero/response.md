```zero
use std

fn main() {
    let args = std.args
    if args.len() < 2 {
        check world.out.write("error\n")
        return
    }

    let n = std.ascii.to_i32(args[1])
    if n < 1 || n > 5 {
        check world.out.write("error\n")
        return
    }

    let mut a = [0; 25]
    let mut b = [0; 25]
    let mut c = [0; 25]

    let mut index = 2
    for i in 0..n {
        for j in 0..n {
            if index >= args.len() {
                check world.out.write("error\n")
                return
            }
            a[i * n + j] = std.ascii.to_i32(args[index])
            index += 1
        }
    }

    for i in 0..n {
        for j in 0..n {
            if index >= args.len() {
                check world.out.write("error\n")
                return
            }
            b[i * n + j] = std.ascii.to_i32(args[index])
            index += 1
        }
    }

    for i in 0..n {
        for j in 0..n {
            let mut sum = 0
            for k in 0..n {
                sum += a[i * n + k] * b[k * n + j]
            }
            c[i * n + j] = sum
        }
    }

    for i in 0..n {
        for j in 0..n {
            check world.out.write(std.ascii.from_i32(c[i * n + j]))
            if j < n - 1 {
                check world.out.write(" ")
            }
        }
        check world.out.write("\n")
    }

    return
}
```