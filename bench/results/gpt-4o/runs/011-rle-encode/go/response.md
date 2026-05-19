```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	data, err := reader.ReadBytes(0)
	if err != nil && err.Error() != "EOF" {
		fmt.Fprintln(writer, "error")
		return
	}

	if len(data) == 0 {
		return
	}

	currentByte := data[0]
	count := 1

	for i := 1; i < len(data); i++ {
		if data[i] == currentByte {
			count++
		} else {
			fmt.Fprintf(writer, "%d %d\n", count, currentByte)
			currentByte = data[i]
			count = 1
		}
	}

	fmt.Fprintf(writer, "%d %d\n", count, currentByte)
}
```