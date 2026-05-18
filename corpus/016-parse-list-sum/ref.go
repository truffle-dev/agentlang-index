package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const u32MaxU64 uint64 = 4294967295
const nMax uint32 = 1000

func parseU32(s string) (uint32, bool) {
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
	return uint32(v), true
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

func run(data string) (uint64, bool) {
	lines := strings.Split(data, "\n")
	if len(lines) < 1 {
		return 0, false
	}
	n, ok := parseU32(lines[0])
	if !ok || n > nMax {
		return 0, false
	}
	if uint32(len(lines)) < n+1 {
		return 0, false
	}
	var total uint64 = 0
	for i := uint32(1); i <= n; i++ {
		v, ok := parseU32(lines[i])
		if !ok {
			return 0, false
		}
		total += uint64(v)
		if total > u32MaxU64 {
			return 0, false
		}
	}
	return total, true
}

func main() {
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	data := readAll(bufio.NewReader(os.Stdin))
	total, ok := run(data)
	if !ok {
		fmt.Fprint(w, "error\n")
		return
	}
	fmt.Fprintf(w, "%d\n", total)
}
