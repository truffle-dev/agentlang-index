package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

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

func main() {
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	r := bufio.NewReader(os.Stdin)
	data, _ := readAll(r)
	parts := strings.SplitN(data, "\n", 3)
	if len(parts) < 2 {
		fmt.Fprint(w, "error\n")
		return
	}
	a, okA := parseU32(parts[0])
	b, okB := parseU32(parts[1])
	if !okA || !okB {
		fmt.Fprint(w, "error\n")
		return
	}
	sum := uint64(a) + uint64(b)
	if sum > math.MaxUint32 {
		fmt.Fprint(w, "error\n")
		return
	}
	fmt.Fprintf(w, "%d\n", uint32(sum))
}

func readAll(r *bufio.Reader) (string, error) {
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
	return sb.String(), nil
}
