// CSV line tokenizer (RFC 4180 subset), Go reference.

package main

import (
	"bufio"
	"os"
	"strings"
)

const (
	fieldStart        = 0
	inUnquoted        = 1
	inQuoted          = 2
	afterClosingQuote = 3
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, _ := reader.ReadString('\n')
	line = strings.TrimRight(line, "\n")
	var out strings.Builder
	state := fieldStart
	if len(line) > 0 {
		for i := 0; i < len(line); i++ {
			ch := line[i]
			switch state {
			case fieldStart:
				if ch == '"' {
					state = inQuoted
				} else if ch == ',' {
					out.WriteByte('\n')
				} else {
					out.WriteByte(ch)
					state = inUnquoted
				}
			case inUnquoted:
				if ch == ',' {
					out.WriteByte('\n')
					state = fieldStart
				} else {
					out.WriteByte(ch)
				}
			case inQuoted:
				if ch == '"' {
					state = afterClosingQuote
				} else {
					out.WriteByte(ch)
				}
			case afterClosingQuote:
				if ch == '"' {
					out.WriteByte('"')
					state = inQuoted
				} else if ch == ',' {
					out.WriteByte('\n')
					state = fieldStart
				}
			}
		}
		out.WriteByte('\n')
	}
	os.Stdout.WriteString(out.String())
}
