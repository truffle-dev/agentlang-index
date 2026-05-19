```go
package main

import (
	"bufio"
	"io"
	"math/big"
	"os"
	"strconv"
	"strings"
)

func main() {
	r := bufio.NewReader(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	data, _ := io.ReadAll(r)
	s := strings.TrimSpace(string(data))
	if s == "" {
		w.WriteString("error\n")
		return
	}

	nVal, err := strconv.ParseInt(s, 10, 64)
	if err != nil || nVal < 0 {
		w.WriteString("error\n")
		return
	}

	memo := map[int64]*big.Int{
		0: big.NewInt(0),
		1: big.NewInt(1),
	}

	var fib func(int64) *big.Int
	fib = func(n int64) *big.Int {
		if v, ok := memo[n]; ok {
			return v
		}
		res := new(big.Int).Add(fib(n-1), fib(n-2))
		memo[n] = res
		return res
	}

	result := fib(nVal)
	w.WriteString(result.String())
	w.WriteByte('\n')
}
```