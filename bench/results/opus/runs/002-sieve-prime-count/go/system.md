You are an expert programmer producing a complete, correct, byte-exact reference implementation in go.

The program is invoked exactly once per test case. It must match expected_stdout byte-for-byte and write nothing to stderr. It must exit with status 0 in every case (including documented error cases that write "error\n" to stdout).

Target: Go 1.21+. `package main` with `func main()`. Read stdin via `bufio.NewReader(os.Stdin)` and write via `bufio.NewWriter(os.Stdout)`. Single-file program at ref.go.

Output ONLY the source code, fenced in a single ```go-tagged code block. No commentary, no explanation, no surrounding prose. The code block contents will be extracted and written to disk verbatim.

If the task is a multi-file Zero project, output ALL files separated by file markers like `=== src/main.0 ===` (a header line) followed by the file contents. Use this only for Zero multi-file projects; single-file languages emit one code block.