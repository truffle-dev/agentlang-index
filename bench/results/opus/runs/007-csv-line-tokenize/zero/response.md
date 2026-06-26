```zero
const std = @import("std")

const main = fn(world: std.World) void {
  const args = std.args(world)
  if args.len() <= 1 {
    return
  }
  const input = args[1]
  if input.len() == 0 {
    return
  }
  var i: u32 = 0
  const len = input.len()
  var field_start = true
  while i < len {
    if field_start {
      field_start = false
      if input[i] == 34 {
        i = i + 1
        while i < len {
          if input[i] == 34 {
            if i + 1 < len and input[i + 1] == 34 {
              check world.out.write("\"")
              i = i + 2
            } else {
              i = i + 1
              break
            }
          } else {
            var buf: [1]u8 = undefined
            buf[0] = input[i]
            check world.out.write(buf[0..1])
            i = i + 1
          }
        }
      }
    } else if input[i] == 44 {
      check world.out.write("\n")
      i = i + 1
      field_start = true
    } else {
      var buf: [1]u8 = undefined
      buf[0] = input[i]
      check world.out.write(buf[0..1])
      i = i + 1
    }
  }
  check world.out.write("\n")
  return
}
```