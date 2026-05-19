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

	// Read the shift value
	shiftLine, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		writer.Flush()
		return
	}
	shiftLine = strings.TrimSpace(shiftLine)

	// Parse the shift value
	shift, err := strconv.Atoi(shiftLine)
	if err != nil || shift < 0 || shift > 25 {
		fmt.Fprint(writer, "error\n")
		writer.Flush()
		return
	}

	// Read the plaintext
	plaintext, err := reader.ReadString('\n')
	if err != nil || len(plaintext) == 0 {
		fmt.Fprint(writer, "error\n")
		writer.Flush()
		return
	}
	plaintext = strings.TrimRight(plaintext, "\n")

	// Validate the plaintext
	for _, ch := range plaintext {
		if ch < 'a' || ch > 'z' {
			fmt.Fprint(writer, "error\n")
			writer.Flush()
			return
		}
	}

	// Encrypt the plaintext using the Caesar cipher
	ciphertext := make([]byte, len(plaintext))
	for i, ch := range plaintext {
		ciphertext[i] = 'a' + (ch-'a'+byte(shift))%26
	}

	// Write the result
	fmt.Fprintln(writer, string(ciphertext))
	writer.Flush()
}
```