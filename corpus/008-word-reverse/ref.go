// Reverse the order of words on a line, Go reference.

package main

import (
	"bufio"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	line = strings.TrimRight(line, "\n")
	parts := strings.Split(line, " ")
	words := parts[:0]
	for _, w := range parts {
		if w != "" {
			words = append(words, w)
		}
	}
	if len(words) == 0 {
		return
	}
	var b strings.Builder
	for i := len(words) - 1; i >= 0; i-- {
		if i != len(words)-1 {
			b.WriteByte(' ')
		}
		b.WriteString(words[i])
	}
	b.WriteByte('\n')
	os.Stdout.WriteString(b.String())
}
