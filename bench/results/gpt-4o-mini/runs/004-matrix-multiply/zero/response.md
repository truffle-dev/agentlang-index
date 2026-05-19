```zero
const N = 5

func main() {
    let n = check parseInt(std.args[0])
    let a = new Array[N][N]
    let b = new Array[N][N]
    let c = new Array[N][N]

    for i in 0..n {
        let row = std.args[i + 1].split(" ")
        for j in 0..n {
            a[i][j] = check parseInt(row[j])
        }
    }

    for i in 0..n {
        let row = std.args[i + 1 + n].split(" ")
        for j in 0..n {
            b[i][j] = check parseInt(row[j])
        }
    }

    for i in 0..n {
        for j in 0..n {
            c[i][j] = 0
            for k in 0..n {
                c[i][j] += a[i][k] * b[k][j]
            }
        }
    }

    for i in 0..n {
        let line = new Array[N * 4]
        let mut pos = 0
        for j in 0..n {
            pos += check writeInt(line[pos..], c[i][j])
            if j < n - 1 {
                line[pos] = ' '
                pos += 1
            }
        }
        line[pos] = '\n'
        check world.out.write(line[0..pos + 1])
    }

    return
}
```