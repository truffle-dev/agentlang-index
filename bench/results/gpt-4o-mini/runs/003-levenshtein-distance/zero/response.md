```zero
const A = std.args[1]
const B = std.args[2]

const m = A.len
const n = B.len

const dp = check world.out.alloc((m + 1) * (n + 1) * 8)

for i in 0..(m + 1)
    dp[i * (n + 1)] = i

for j in 0..(n + 1)
    dp[j] = j

for i in 1..(m + 1)
    for j in 1..(n + 1)
        cost = if A[i - 1] == B[j - 1] 0 else 1
        dp[i * (n + 1) + j] = min(
            dp[(i - 1) * (n + 1) + j] + 1,
            dp[i * (n + 1) + (j - 1)] + 1,
            dp[(i - 1) * (n + 1) + (j - 1)] + cost
        )

check world.out.write(dp[m * (n + 1) + n].to_string() + "\n")

return
```