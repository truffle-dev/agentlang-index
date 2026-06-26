```zero
let world = @import("world")
let std = @import("std")

let main = fn(): void {
  let args = std.args()
  if args.len == 0 {
    return
  }
  let input = args[0]
  let len = input.len
  if len == 0 {
    return
  }

  let words: [1000][]u8 = undefined
  let count: u32 = 0
  let in_word = false
  let word_start: u32 = 0
  let i: u32 = 0

  while i < len {
    if input[i] != ' ' {
      if !in_word {
        word_start = i
        in_word = true
      }
    } else {
      if in_word {
        words[count] = input[word_start..i]
        count = count + 1
        in_word = false
      }
    }
    i = i + 1
  }
  if in_word {
    words[count] = input[word_start..len]
    count = count + 1
  }

  if count == 0 {
    return
  }

  let j: u32 = count
  while j > 0 {
    j = j - 1
    check world.out.write(words[j])
    if j > 0 {
      check world.out.write(" ")
    }
  }
  check world.out.write("\n")
  return
}
```