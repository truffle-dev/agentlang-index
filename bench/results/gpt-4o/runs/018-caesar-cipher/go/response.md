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

	// Read the shift value
	shiftLine, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		return
	}
	shiftLine = strings.TrimSpace(shiftLine)
	shift, err := strconv.Atoi(shiftLine)
	if err != nil || shift < 0 || shift > 25 {
		fmt.Fprint(writer, "error\n")
		return
	}

	// Read the plaintext
	plaintext, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprint(writer, "error\n")
		return
	}
	plaintext = strings.TrimSuffix(plaintext, "\n")

	if len(plaintext) == 0 {
		fmt.Fprint(writer, "error\n")
		return
	}

	// Validate and shift the plaintext
	var ciphertext strings.Builder
	for _, ch := range plaintext {
		if ch < 'a' || ch > 'z' {
			fmt.Fprint(writer, "error\n")
			return
		}
		shifted := (ch-'a'+rune(shift))%26 + 'a'
		ciphertext.WriteRune(shifted)
	}

	fmt.Fprintf(writer, "%s\n", ciphertext.String())
}
```