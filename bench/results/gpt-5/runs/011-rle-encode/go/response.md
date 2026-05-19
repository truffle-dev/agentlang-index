```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	buf := make([]byte, 32768)
	var havePrev bool
	var prev byte
	var count int64

	for {
		n, err := r.Read(buf)
		if n > 0 {
			for i := 0; i < n; i++ {
				b := buf[i]
				if !havePrev {
					prev = b
					count = 1
					havePrev = true
				} else if b == prev {
					count++
				} else {
					out := make([]byte, 0, 32)
					out = strconv.AppendInt(out, count, 10)
					out = append(out, ' ')
					out = strconv.AppendInt(out, int64(prev), 10)
					out = append(out, '\n')
					if _, e := w.Write(out); e != nil {
						return
					}
					prev = b
					count = 1
				}
			}
		}
		if err != nil {
			if err == io.EOF {
				break
			}
			break
		}
	}

	if havePrev {
		out := make([]byte, 0, 32)
		out = strconv.AppendInt(out, count, 10)
		out = append(out, ' ')
		out = strconv.AppendInt(out, int64(prev), 10)
		out = append(out, '\n')
		w.Write(out)
	}
}
```