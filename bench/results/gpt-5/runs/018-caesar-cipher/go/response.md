```go
package main

import (
	"bufio"
	"io"
	"os"
	"strings"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	// Read first line (shift)
	shiftLine, err := in.ReadString('\n')
	if err != nil && err != io.EOF {
		out.WriteString("error\n")
		return
	}
	if len(shiftLine) > 0 && shiftLine[len(shiftLine)-1] == '\n' {
		shiftLine = shiftLine[:len(shiftLine)-1]
	}
	shiftStr := strings.TrimSpace(shiftLine)
	if shiftStr == "" {
		out.WriteString("error\n")
		return
	}
	// Parse shift ensuring only digits and value <= 25 without overflow
	shift := 0
	tooBig := false
	for i := 0; i < len(shiftStr); i++ {
		c := shiftStr[i]
		if c < '0' || c > '9' {
			out.WriteString("error\n")
			return
		}
		if !tooBig {
			d := int(c - '0')
			// Only compute while shift <= 25 to avoid overflow
			newVal := shift*10 + d
			if newVal > 25 {
				tooBig = true
			} else {
				shift = newVal
			}
		}
	}
	if tooBig {
		out.WriteString("error\n")
		return
	}

	// Read second line (plaintext)
	plain, err := in.ReadString('\n')
	if err != nil && err != io.EOF {
		out.WriteString("error\n")
		return
	}
	if len(plain) > 0 && plain[len(plain)-1] == '\n' {
		plain = plain[:len(plain)-1]
	}
	if len(plain) == 0 {
		out.WriteString("error\n")
		return
	}
	// Validate plaintext and apply shift
	b := []byte(plain)
	for i := 0; i < len(b); i++ {
		c := b[i]
		if c < 'a' || c > 'z' {
			out.WriteString("error\n")
			return
		}
		// Shift within 'a'..'z'
		b[i] = byte('a' + (int(c-'a')+shift)%26)
	}

	out.Write(b)
	out.WriteByte('\n')
}
```