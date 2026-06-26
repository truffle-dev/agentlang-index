```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, err := reader.ReadString('\n')
	if err != nil {
		fmt.Print("error\n")
		return
	}
	line = line[:len(line)-1] // strip \n

	if len(line) == 0 {
		fmt.Print("error\n")
		return
	}

	for _, b := range []byte(line) {
		if b < 'a' || b > 'z' {
			fmt.Print("error\n")
			return
		}
	}

	w := bufio.NewWriter(os.Stdout)
	bytes := []byte(line)
	i := 0
	for i < len(bytes) {
		ch := bytes[i]
		count := 1
		for i+count < len(bytes) && bytes[i+count] == ch {
			count++
		}
		fmt.Fprintf(w, "%c%d", ch, count)
		i += count
	}
	w.WriteByte('\n')
	w.Flush()
}
```