```zero
import std

fn count_words(s: Span<u8>) -> u64:
    let mut count: u64 = 0
    let mut in_word: bool = false
    let mut i: u64 = 0
    while i < s.len:
        if s[i] != 32:
            in_word = true
        else:
            if in_word:
                count = count + 1
                in_word = false
        i = i + 1
    if in_word:
        count = count + 1
    return count

fn find_word(s: Span<u8>, k: u64) -> Span<u8>:
    let mut count: u64 = 0
    let mut in_word: bool = false
    let mut i: u64 = 0
    let mut word_start: u64 = 0
    while i < s.len:
        if s[i] != 32:
            if !in_word:
                word_start = i
                in_word = true
        else:
            if in_word:
                in_word = false
                if count == k:
                    return s[word_start..i]
                count = count + 1
        i = i + 1
    if in_word:
        if count == k:
            return s[word_start..s.len]
    return s[0..0]

fn main():
    let args = std.args()
    if args.len < 2:
        return
    let s: Span<u8> = args[1]
    let wc = count_words(s)
    if wc == 0:
        return
    let mut j: u64 = wc
    while j > 0:
        j = j - 1
        let word = find_word(s, j)
        check world.out.write(word)
        if j > 0:
            check world.out.write(" ")
    check world.out.write("\n")
    return
```