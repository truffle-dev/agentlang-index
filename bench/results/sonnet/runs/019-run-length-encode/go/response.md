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

	line, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		return
	}

	// Strip trailing newline
	if len(line) > 0 && line[len(line)-1] == '\n' {
		line = line[:len(line)-1]
	}

	if len(line) == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}

	for i := 0; i < len(line); i++ {
		if line[i] < 'a' || line[i] > 'z' {
			fmt.Fprint(writer, "error\n")
			return
		}
	}

	i := 0
	for i < len(line) {
		ch := line[i]
		count := 1
		for i+count < len(line) && line[i+count] == ch {
			count++
		}
		fmt.Fprintf(writer, "%c%d", ch, count)
		i += count
	}
	fmt.Fprint(writer, "\n")
}
```