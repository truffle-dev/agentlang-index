```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	line1, _ := reader.ReadString('\n')
	line1 = strings.TrimRight(line1, "\r\n")
	line1 = strings.TrimRight(line1, " \t")

	if line1 == "" {
		fmt.Fprintln(w, "error")
		return
	}

	shift := 0
	for _, b := range []byte(line1) {
		if b < '0' || b > '9' {
			fmt.Fprintln(w, "error")
			return
		}
		shift = shift*10 + int(b-'0')
		if shift > 25 {
			fmt.Fprintln(w, "error")
			return
		}
	}

	line2, _ := reader.ReadString('\n')
	line2 = strings.TrimRight(line2, "\r\n")

	if len(line2) == 0 {
		fmt.Fprintln(w, "error")
		return
	}

	out := make([]byte, len(line2))
	for i, b := range []byte(line2) {
		if b < 'a' || b > 'z' {
			fmt.Fprintln(w, "error")
			return
		}
		out[i] = 'a' + (b-'a'+byte(shift))%26
	}

	fmt.Fprintln(w, string(out))
}
```