import ipaddress
import random
import time
import csv
from typing import List, Dict, Optional, Tuple


class BinaryTrieNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.prefix = None
        self.next_hop = None


class BinaryTrie:
    def __init__(self):
        self.root = BinaryTrieNode()

    def insert(self, prefix: str, next_hop: str):
        ip_net = ipaddress.ip_network(prefix, strict=False)
        binary = bin(int(ip_net.network_address))[2:].zfill(32)
        
        node = self.root
        for bit in binary[:ip_net.prefixlen]:
            if bit == '0':
                if not node.left:
                    node.left = BinaryTrieNode()
                node = node.left
            else:
                if not node.right:
                    node.right = BinaryTrieNode()
                node = node.right
        
        node.prefix = prefix
        node.next_hop = next_hop

    def lookup(self, ip: str) -> Optional[str]:
        ip_addr = int(ipaddress.ip_address(ip))
        binary = bin(ip_addr)[2:].zfill(32)
        
        node = self.root
        best_match = None

        for bit in binary:
            if bit == '0' and node.left:
                node = node.left
            elif bit == '1' and node.right:
                node = node.right
            else:
                break
            
            if node.prefix:
                best_match = node.next_hop

        return best_match

    def print_trie(self, filename: str):
        def traverse(node, depth=0):
            if node:
                prefix_info = f"Prefix: {node.prefix}, Next Hop: {node.next_hop}" if node.prefix else "No prefix"
                file.write(f"{'  ' * depth}{prefix_info}\n")
                if node.left:
                    file.write(f"{'  ' * depth}0 ->\n")
                    traverse(node.left, depth + 1)
                if node.right:
                    file.write(f"{'  ' * depth}1 ->\n")
                    traverse(node.right, depth + 1)

        with open(filename, 'w') as file:
            file.write("Binary Trie Structure:\n")
            traverse(self.root)


class MultibitTrie:
    def __init__(self, stride=3):
        self.stride = stride
        self.root = {}

    def insert(self, prefix: str, next_hop: str):
        ip_net = ipaddress.ip_network(prefix, strict=False)
        binary = bin(int(ip_net.network_address))[2:].zfill(32)
        
        current = self.root
        for i in range(0, ip_net.prefixlen, self.stride):
            chunk = binary[i:i+self.stride].ljust(self.stride, '0')
            
            if chunk not in current:
                current[chunk] = {}
            
            current = current[chunk]
        
        current['next_hop'] = next_hop
        current['prefix'] = prefix

    def lookup(self, ip: str) -> Optional[str]:
        ip_addr = int(ipaddress.ip_address(ip))
        binary = bin(ip_addr)[2:].zfill(32)
        
        best_match = None
        current = self.root

        for i in range(0, 32, self.stride):
            chunk = binary[i:i+self.stride].ljust(self.stride, '0')
            
            if chunk in current:
                current = current[chunk]
                
                if 'next_hop' in current:
                    best_match = current['next_hop']
            else:
                break

        return best_match

    def print_trie(self, filename: str):
        def traverse(node, depth=0):
            if isinstance(node, dict):
                for key, child in node.items():
                    if key not in ('prefix', 'next_hop'):
                        file.write(f"{'  ' * depth}{key} ->\n")
                        traverse(child, depth + 1)
                    else:
                        if key == 'prefix':
                            file.write(f"{'  ' * depth}Prefix: {node.get('prefix', 'None')}, Next Hop: {node.get('next_hop', 'None')}\n")

        with open(filename, 'w') as file:
            file.write("Multibit Trie Structure:\n")
            traverse(self.root)


class LinearSearchLookup:
    def __init__(self):
        self.prefixes = []

    def add_prefix(self, prefix: str, next_hop: str):
        self.prefixes.append((ipaddress.ip_network(prefix, strict=False), next_hop))

    def lookup(self, ip: str) -> Optional[str]:
        ip_addr = ipaddress.ip_address(ip)
        best_match = None
        best_prefix_len = -1

        for prefix, next_hop in self.prefixes:
            if ip_addr in prefix:
                if prefix.prefixlen > best_prefix_len:
                    best_match = next_hop
                    best_prefix_len = prefix.prefixlen

        return best_match

class PathCompressedTrieNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.prefix = None
        self.next_hop = None
        self.skip_value = 0  # Number of bits to skip


class PathCompressedTrie:
    def __init__(self):
        self.root = PathCompressedTrieNode()

    def insert(self, prefix: str, next_hop: str):
        ip_net = ipaddress.ip_network(prefix, strict=False)
        binary = bin(int(ip_net.network_address))[2:].zfill(32)
        
        node = self.root
        current_bit_index = 0

        while current_bit_index < ip_net.prefixlen:
            # Traverse or create path based on current bit
            if binary[current_bit_index] == '0':
                if not node.left:
                    node.left = PathCompressedTrieNode()
                node = node.left
            else:
                if not node.right:
                    node.right = PathCompressedTrieNode()
                node = node.right
            
            current_bit_index += 1

            # Check if we can apply path compression
            if node.left is None and node.right is None:
                # Path compression: merge single-child nodes
                while self._is_single_child_node(node):
                    # Calculate skip value
                    child = node.left if node.left else node.right
                    node.skip_value += 1
                    node = child

            # Final node placement
            if current_bit_index == ip_net.prefixlen:
                node.prefix = prefix
                node.next_hop = next_hop

    def _is_single_child_node(self, node: PathCompressedTrieNode) -> bool:
        # Check if node has only one child
        return (node.left is not None and node.right is None) or \
               (node.left is None and node.right is not None)

    def lookup(self, ip: str) -> Optional[str]:
        ip_addr = int(ipaddress.ip_address(ip))
        binary = bin(ip_addr)[2:].zfill(32)
        
        node = self.root
        best_match = None
        current_bit_index = 0

        while current_bit_index < 32:
            # Skip bits based on skip value
            current_bit_index += node.skip_value

            if current_bit_index >= 32:
                break

            # Choose next node based on current bit
            if binary[current_bit_index] == '0':
                if not node.left:
                    break
                node = node.left
            else:
                if not node.right:
                    break
                node = node.right
            
            current_bit_index += 1

            # Update best match if prefix is found
            if node.prefix:
                best_match = node.next_hop

        return best_match

    def print_trie(self, filename: str):
        def traverse(node: PathCompressedTrieNode, depth: int = 0):
            if node:
                prefix_info = f"Prefix: {node.prefix}, Next Hop: {node.next_hop}, Skip: {node.skip_value}" \
                    if node.prefix else f"No prefix, Skip: {node.skip_value}"
                
                file.write(f"{'  ' * depth}{prefix_info}\n")
                
                if node.left:
                    file.write(f"{'  ' * depth}0 ->\n")
                    traverse(node.left, depth + 1)
                
                if node.right:
                    file.write(f"{'  ' * depth}1 ->\n")
                    traverse(node.right, depth + 1)

        with open(filename, 'w') as file:
            file.write("Path Compressed Trie Structure:\n")
            traverse(self.root)

def generate_test_dataset(num_prefixes: int = 1000, num_lookups: int = 10000) -> Dict:
    prefixes = set()
    while len(prefixes) < num_prefixes:
        prefix = ipaddress.ip_network(
            (f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}", 
             random.randint(8, 30)), strict=False)
        prefixes.add(str(prefix))
    
    lookups = [
        f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        for _ in range(num_lookups)
    ]
    
    return {"prefixes": list(prefixes), "lookups": lookups}


def benchmark_algorithms(dataset: Dict):
    algorithms = {
        "Linear Search": LinearSearchLookup(),
        "Binary Trie": BinaryTrie(),
        "Multibit Trie": MultibitTrie()
    }

    results = {}

    for name, algo in algorithms.items():
        for prefix in dataset['prefixes']:
            if hasattr(algo, 'add_prefix'):
                algo.add_prefix(prefix, f"NH_{prefix}")
            elif hasattr(algo, 'insert'):
                algo.insert(prefix, f"NH_{prefix}")

        start_time = time.time()
        unmatched = sum(1 for ip in dataset['lookups'] if algo.lookup(ip) is None)
        end_time = time.time()

        results[name] = {
            "total_time": end_time - start_time,
            "avg_lookup_time": (end_time - start_time) / len(dataset['lookups']),
            "unmatched": unmatched
        }

    return results


def main():
    random.seed(42)
    dataset = generate_test_dataset()
    
    algorithms = {
        "Linear Search": LinearSearchLookup(),
        "Binary Trie": BinaryTrie(),
        "Multibit Trie": MultibitTrie(),
        "Path Compressed Trie": PathCompressedTrie()  # Add the new trie type
    }

    results = {}

    for name, algo in algorithms.items():
        for prefix in dataset['prefixes']:
            if hasattr(algo, 'add_prefix'):
                algo.add_prefix(prefix, f"NH_{prefix}")
            elif hasattr(algo, 'insert'):
                algo.insert(prefix, f"NH_{prefix}")

        start_time = time.time()
        unmatched = sum(1 for ip in dataset['lookups'] if algo.lookup(ip) is None)
        end_time = time.time()

        results[name] = {
            "total_time": end_time - start_time,
            "avg_lookup_time": (end_time - start_time) / len(dataset['lookups']),
            "unmatched": unmatched
        }

    with open('ip_lookup_benchmark.csv', 'w', newline='') as csvfile:
        fieldnames = ['Algorithm', 'Total Time (s)', 'Average Lookup Time (s)', 'Unmatched Lookups']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, metrics in results.items():
            writer.writerow({
                'Algorithm': name,
                'Total Time (s)': metrics['total_time'],
                'Average Lookup Time (s)': metrics['avg_lookup_time'],
                'Unmatched Lookups': metrics['unmatched']
            })

    print("Benchmark Results:")
    for name, metrics in results.items():
        print(f"{name}:")
        print(f"  Total Time: {metrics['total_time']:.4f} seconds")
        print(f"  Average Lookup Time: {metrics['avg_lookup_time']:.6f} seconds")
        print(f"  Unmatched Lookups: {metrics['unmatched']}")

    # Visualization of tries
    binary_trie = BinaryTrie()
    multibit_trie = MultibitTrie()
    path_compressed_trie = PathCompressedTrie()

    for prefix in dataset['prefixes']:
        binary_trie.insert(prefix, f"NH_{prefix}")
        multibit_trie.insert(prefix, f"NH_{prefix}")
        path_compressed_trie.insert(prefix, f"NH_{prefix}")

    # Save the trie visualizations to files
    binary_trie.print_trie('binary_trie_visualization.txt')
    multibit_trie.print_trie('multibit_trie_visualization.txt')
    path_compressed_trie.print_trie('path_compressed_trie_visualization.txt')
if __name__ == "__main__":
    main()