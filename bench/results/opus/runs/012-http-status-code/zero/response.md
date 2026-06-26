```zero
const std = @import("std")

const main = fn(): void {
  const world = std.world()
  const args = std.args()

  if args.len <= 1 {
    check world.out.write("error\n")
    return
  }

  const raw_url = args[1]

  const url = if raw_url.len > 0 and raw_url[raw_url.len - 1] == '\n' {
    raw_url[0..raw_url.len - 1]
  } else {
    raw_url
  }

  const http = std.http()

  if http == error {
    check world.out.write("error\n")
    return
  }

  const resp = http.get(url, .{ .timeout = 5000 })

  if resp == error {
    check world.out.write("error\n")
    return
  }

  const code = resp.status

  check world.out.write(std.fmt.int(code))
  check world.out.write("\n")

  return
}
```