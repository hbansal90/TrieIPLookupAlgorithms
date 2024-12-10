# IP Lookup Algorithms and Trie Implementations

This project implements and analyzes various algorithms for IP lookup using trie-based data structures. These algorithms provide a structured way to manage and search IP prefixes efficiently.

## Features

- **Binary Trie**: Standard binary trie for prefix matching.
- **Multibit Trie**: Optimized trie with configurable stride for efficient traversal.
- **Linear Search**: Simple, brute-force prefix lookup.
- **Path Compressed Trie**: Trie with path compression to reduce storage and improve lookup time.
- **Performance Benchmarking**: Compare algorithm performance using synthetic datasets.
- **Visualization**: Outputs trie structures to text files for inspection.

## Installation and Usage

1. **Prerequisites**:
   - Python 3.7+
   - Standard Python libraries: `ipaddress`, `random`, `time`, `csv`

2. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

3. **Run the Main Script**:
   ```bash
   python main.py
   ```
   
   This will generate benchmarking results and save trie visualizations.

4. **Benchmark Results**:
   - Results are saved in `ip_lookup_benchmark.csv`.

5. **Visualization Files**:
   - Binary Trie: `binary_trie_visualization.txt`
   - Multibit Trie: `multibit_trie_visualization.txt`
   - Path Compressed Trie: `path_compressed_trie_visualization.txt`

## Code Structure

- **`BinaryTrie`**
  - Implements a binary trie for prefix insertion and lookup.
- **`MultibitTrie`**
  - Optimized trie with customizable stride for faster traversal.
- **`LinearSearchLookup`**
  - Linear search for prefix matching.
- **`PathCompressedTrie`**
  - A trie with path compression to reduce height.
- **`benchmark_algorithms()`**
  - Benchmarks algorithms using synthetic datasets.
- **`generate_test_dataset()`**
  - Creates random IP prefixes and lookups for testing.

## How It Works

1. **Trie Construction**:
   - Insert prefixes and next-hop information into the selected data structure.
2. **Lookup**:
   - Perform IP address lookups to determine the next-hop using the trie.
3. **Performance Evaluation**:
   - Measure total lookup time, average lookup time, and unmatched lookups for each algorithm.

## Performance Metrics

- **Total Time**: Time taken for all lookups.
- **Average Lookup Time**: Average time per lookup.
- **Unmatched Lookups**: Number of IPs not matched with any prefix.

## Example Output

### Benchmark Results

| Algorithm          | Total Time (s) | Average Lookup Time (s) | Unmatched Lookups |
|--------------------|----------------|--------------------------|--------------------|
| Linear Search      | 1.2345         | 0.000123                | 12                 |
| Binary Trie        | 0.5678         | 0.000057                | 10                 |
| Multibit Trie      | 0.3456         | 0.000035                | 8                  |
| Path Compressed Trie | 0.2345       | 0.000023                | 5                  |

### Trie Visualization Example

#### Binary Trie
```
Binary Trie Structure:
Prefix: 192.168.0.0/16, Next Hop: NH_192.168.0.0/16
  0 ->
    1 ->
      Prefix: 192.168.1.0/24, Next Hop: NH_192.168.1.0/24
```

#### Multibit Trie
```
Multibit Trie Structure:
110 ->
  Prefix: 192.168.1.0/24, Next Hop: NH_192.168.1.0/24
```

#### Path Compressed Trie
```
Path Compressed Trie Structure:
Prefix: 192.168.0.0/16, Next Hop: NH_192.168.0.0/16, Skip: 0
  0 ->
    Prefix: 192.168.1.0/24, Next Hop: NH_192.168.1.0/24, Skip: 8
```

## Future Enhancements

- Implement additional IP lookup techniques.
- Add visualization tools for graphical trie representations.
- Extend benchmarks with real-world datasets.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

