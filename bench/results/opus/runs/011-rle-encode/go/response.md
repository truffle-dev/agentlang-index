```go
package main

import (
	"bufio"
	"io"
	"os"
	"strconv"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	data, _ := io.ReadAll(reader)
	if len(data) == 0 {
		return
	}

	count := 1
	for i := 1; i < len(data); i++ {
		if data[i] == data[i-1] {
			count++
		} else {
			writer.WriteString(strconv.Itoa(count))
			writer.WriteByte(' ')
			writer.WriteString(strconv.Itoa(int(data[i-1])))
			writer.WriteByte('\n')
			count = 1
		}
	}
	writer.WriteString(strconv.Itoa(count))
	writer.WriteByte(' ')
	writer.WriteString(strconv.Itoa(int(data[len(data)-1])))
	writer.WriteByte('\n')
}
```