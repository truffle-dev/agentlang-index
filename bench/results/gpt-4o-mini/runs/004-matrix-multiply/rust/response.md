```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    
    let mut lines = input.lines();
    let n: usize = lines.next().unwrap().parse().unwrap();
    
    let mut a = vec![vec![0; n]; n];
    let mut b = vec![vec![0; n]; n];
    
    for i in 0..n {
        a[i] = lines.next().unwrap().split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
    }
    
    for i in 0..n {
        b[i] = lines.next().unwrap().split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
    }
    
    let mut c = vec![vec![0; n]; n];
    
    for i in 0..n {
        for j in 0..n {
            for k in 0..n {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    
    let mut output = String::new();
    for row in c {
        output.push_str(&row.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" "));
        output.push('\n');
    }
    
    io::stdout().write_all(output.as_bytes()).unwrap();
}
```