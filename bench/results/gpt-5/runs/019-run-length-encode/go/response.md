```go
package main

import (
	"bufio"
	"os"
	"strconv"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	line, err := r.ReadBytes('\n')
	if err != nil {
		w.WriteString("error\n")
		return
	}

	if len(line) == 0 || line[len(line)-1] != '\n' {
		w.WriteString("error\n")
		return
	}
	s := line[:len(line)-1]

	if len(s) == 0 {
		w.WriteString("error\n")
		return
	}

	for _, b := range s {
		if b < 'a' || b > 'z' {
			w.WriteString("error\n")
			return
		}
	}

	cur := s[0]
	count := 1
	for i := 1; i < len(s); i++ {
		b := s[i]
		if b == cur {
			count++
		} else {
			w.WriteByte(cur)
			w.WriteString(strconv.Itoa(count))
			cur = b
			count = 1
		}
	}
	w.WriteByte(cur)
	w.WriteString(strconv.Itoa(count))
	w.WriteByte('\n')
}
```