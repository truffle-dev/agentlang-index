```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	data, err := io.ReadAll(r)
	if err != nil || len(data) == 0 {
		return
	}

	cur := data[0]
	count := 1
	for _, b := range data[1:] {
		if b == cur {
			count++
		} else {
			fmt.Fprintf(w, "%d %d\n", count, cur)
			cur = b
			count = 1
		}
	}
	fmt.Fprintf(w, "%d %d\n", count, cur)
}
```