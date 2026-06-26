```zero
use std

fun main() void
  let url = std.args(1)
  let header_name = std.args(2)

  let trimmed_url = trim(url)
  let trimmed_header = trim(header_name)

  let resp = std.http.get(trimmed_url, .{.timeout = 5000})
  if resp.status != 200
    check world.out.write("error\n")
    return
  end

  let val = resp.headers.get_insensitive(trimmed_header)
  if val == null
    check world.out.write("error\n")
    return
  end

  check world.out.write(val)
  check world.out.write("\n")
  return
end

fun trim(s: []u8) []u8
  let start = 0
  let end_ = s.len
  loop
    if start >= end_
      break
    end
    if s[start] == ' ' or s[start] == '\t' or s[start] == '\n' or s[start] == '\r'
      start = start + 1
    else
      break
    end
  end
  loop
    if end_ <= start
      break
    end
    if s[end_ - 1] == ' ' or s[end_ - 1] == '\t' or s[end_ - 1] == '\n' or s[end_ - 1] == '\r'
      end_ = end_ - 1
    else
      break
    end
  end
  return s[start..end_]
end
```