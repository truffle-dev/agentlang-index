```zero
const N = std.args[0].parse_int()
const max_n = 10000

var is_prime = [true] * (max_n + 1)
is_prime[0] = false
is_prime[1] = false

for i in 2..(max_n.sqrt() + 1)
    if is_prime[i]
        for j in (i * i)..(max_n + 1) step i
            is_prime[j] = false

var count = 0
for i in 2..(N + 1)
    if is_prime[i]
        count += 1

check world.out.write(count.to_string() + "\n")
return
```