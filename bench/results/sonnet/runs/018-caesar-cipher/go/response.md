```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	line1, err := reader.ReadString('\n')
	if err != nil && len(line1) == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}
	line1 = strings.TrimRight(line1, "\r\n")
	line1 = strings.TrimRight(line1, " \t")

	line2, err := reader.ReadString('\n')
	if err != nil && len(line2) == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}
	line2 = strings.TrimRight(line2, "\r\n")

	// Validate and parse shift
	if strings.TrimSpace(line1) == "" {
		fmt.Fprint(writer, "error\n")
		return
	}
	for _, c := range line1 {
		if c < '0' || c > '9' {
			fmt.Fprint(writer, "error\n")
			return
		}
	}
	shift, err := strconv.Atoi(line1)
	if err != nil || shift > 25 {
		fmt.Fprint(writer, "error\n")
		return
	}

	// Validate plaintext
	if len(line2) == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}
	for i := 0; i < len(line2); i++ {
		if line2[i] < 'a' || line2[i] > 'z' {
			fmt.Fprint(writer, "error\n")
			return
		}
	}

	// Encrypt
	result := make([]byte, len(line2))
	for i := 0; i < len(line2); i++ {
		result[i] = byte((int(line2[i]-'a')+shift)%26) + 'a'
	}
	fmt.Fprintf(writer, "%s\n", result)
}
```