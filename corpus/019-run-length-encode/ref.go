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
	lines := strings.SplitN(data, "\n", 2)
	if len(lines) < 1 {
		fmt.Fprint(w, "error\n")
		return
	}
	text := lines[0]
	if len(text) == 0 {
		fmt.Fprint(w, "error\n")
		return
	}
	for i := 0; i < len(text); i++ {
		if !isLowercaseLetter(text[i]) {
			fmt.Fprint(w, "error\n")
			return
		}
	}
	out := make([]byte, 0, len(text)*2+1)
	i := 0
	for i < len(text) {
		runByte := text[i]
		runLen := 1
		j := i + 1
		for j < len(text) && text[j] == runByte {
			runLen++
			j++
		}
		out = append(out, runByte)
		out = append(out, strconv.Itoa(runLen)...)
		i = j
	}
	out = append(out, '\n')
	w.Write(out)
}
