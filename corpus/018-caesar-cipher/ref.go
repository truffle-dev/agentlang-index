package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func isLowercaseLetter(b byte) bool {
	return b >= 'a' && b <= 'z'
}

func shiftLetter(b, shift byte) byte {
	zeroBased := b - 'a'
	return 'a' + ((zeroBased + shift) % 26)
}

func parseShift(s string) (byte, bool) {
	t := strings.TrimSpace(s)
	if t == "" {
		return 0, false
	}
	for _, c := range t {
		if c < '0' || c > '9' {
			return 0, false
		}
	}
	v, err := strconv.ParseUint(t, 10, 32)
	if err != nil {
		return 0, false
	}
	if v > 25 {
		return 0, false
	}
	return byte(v), true
}

func readAll(r *bufio.Reader) string {
	var sb strings.Builder
	buf := make([]byte, 4096)
	for {
		n, err := r.Read(buf)
		if n > 0 {
			sb.Write(buf[:n])
		}
		if err != nil {
			break
		}
	}
	return sb.String()
}

func main() {
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	r := bufio.NewReader(os.Stdin)
	data := readAll(r)
	parts := strings.SplitN(data, "\n", 3)
	if len(parts) < 2 {
		fmt.Fprint(w, "error\n")
		return
	}
	shift, ok := parseShift(parts[0])
	if !ok {
		fmt.Fprint(w, "error\n")
		return
	}
	text := parts[1]
	if len(text) == 0 {
		fmt.Fprint(w, "error\n")
		return
	}
	out := make([]byte, 0, len(text)+1)
	for i := 0; i < len(text); i++ {
		b := text[i]
		if !isLowercaseLetter(b) {
			fmt.Fprint(w, "error\n")
			return
		}
		out = append(out, shiftLetter(b, shift))
	}
	out = append(out, '\n')
	w.Write(out)
}
