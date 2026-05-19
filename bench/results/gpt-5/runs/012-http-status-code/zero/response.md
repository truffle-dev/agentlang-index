```zero
use std

fn main() -> void {
  let args = std.args()
  if args.len() < 2 {
    check world.out.write("error\n")
    return
  }

  let mut url = args[1]

  // Trim trailing newline/carriage-return characters
  while url.len() > 0 {
    let last = url[url.len() - 1]
    if last == 10u8 || last == 13u8 {
      url = url[0..url.len() - 1]
    } else {
      break
    }
  }

  if url.len() == 0 {
    check world.out.write("error\n")
    return
  }

  match world.http.get(url, 5000) {
    ok(resp) => {
      let code_u32 = resp.status_code as u32
      let a = (code_u32 / 100) % 10
      let b = (code_u32 / 10) % 10
      let c = code_u32 % 10

      let mut out = [0u8, 0u8, 0u8, 10u8]
      out[0] = 48u8 + (a as u8)
      out[1] = 48u8 + (b as u8)
      out[2] = 48u8 + (c as u8)

      check world.out.write(out[0..4])
      return
    }
    err(_) => {
      check world.out.write("error\n")
      return
    }
  }
}
```