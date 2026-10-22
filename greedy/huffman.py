"""Huffman Coding for Compressing Delivery Manifests.

This module implements greedy variable-length prefix coding to compress logistics
manifests and shipment telematics data, achieving lossless data compression.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple, Any
import heapq


@dataclass
class HuffmanNode:
    """Node in the Huffman binary tree."""
    char: Optional[str]
    freq: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    # Priority queue comparator (min-heap by frequency)
    def __lt__(self, other: "HuffmanNode") -> bool:
        if self.freq != other.freq:
            return self.freq < other.freq
        # Tie-breaker for deterministic tree building
        char_self = self.char if self.char is not None else ""
        char_other = other.char if other.char is not None else ""
        return char_self < char_other


class HuffmanCoding:
    """Huffman Encoder and Decoder.

    Greedy Strategy:
    At each step, greedily select and combine the two nodes with the lowest frequencies
    into a parent node whose frequency is the sum of their frequencies.
    """

    def __init__(self):
        self.root: Optional[HuffmanNode] = None
        self.char_to_code: Dict[str, str] = {}
        self.code_to_char: Dict[str, str] = {}
        self.frequencies: Dict[str, int] = {}

    def build_tree_from_text(self, text: str) -> Optional[HuffmanNode]:
        """Calculates character frequencies and builds Huffman prefix tree."""
        if not text:
            self.root = None
            self.char_to_code = {}
            self.code_to_char = {}
            self.frequencies = {}
            return None

        # Step 1: Count character frequencies
        self.frequencies = {}
        for char in text:
            self.frequencies[char] = self.frequencies.get(char, 0) + 1

        # Edge case: single unique character
        if len(self.frequencies) == 1:
            only_char = next(iter(self.frequencies))
            self.root = HuffmanNode(char=None, freq=self.frequencies[only_char])
            self.root.left = HuffmanNode(char=only_char, freq=self.frequencies[only_char])
            self.char_to_code = {only_char: "0"}
            self.code_to_char = {"0": only_char}
            return self.root

        # Step 2: Min-heap of leaf nodes
        heap = [HuffmanNode(char=ch, freq=fq) for ch, fq in self.frequencies.items()]
        heapq.heapify(heap)

        # Step 3: Greedily merge two lowest frequency nodes
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            merged = HuffmanNode(
                char=None,
                freq=node1.freq + node2.freq,
                left=node1,
                right=node2
            )
            heapq.heappush(heap, merged)

        self.root = heap[0]

        # Step 4: Generate prefix codes
        self.char_to_code = {}
        self.code_to_char = {}
        self._generate_codes(self.root, "")
        return self.root

    def _generate_codes(self, node: Optional[HuffmanNode], current_code: str):
        if node is None:
            return
        if node.char is not None:
            self.char_to_code[node.char] = current_code
            self.code_to_char[current_code] = node.char
            return
        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    def encode(self, text: str) -> str:
        """Encodes plain text into a binary bitstring."""
        if not text:
            return ""
        if not self.char_to_code:
            self.build_tree_from_text(text)
        return "".join(self.char_to_code[ch] for ch in text)

    def decode(self, bitstring: str) -> str:
        """Decodes binary bitstring back into the original plain text."""
        if not bitstring or self.root is None:
            return ""

        # Edge case: single unique character
        if len(self.char_to_code) == 1:
            char = next(iter(self.char_to_code))
            return char * len(bitstring)

        decoded_chars = []
        curr = self.root
        for bit in bitstring:
            curr = curr.left if bit == "0" else curr.right
            if curr is not None and curr.char is not None:
                decoded_chars.append(curr.char)
                curr = self.root

        return "".join(decoded_chars)

    def compress_manifest(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Performs end-to-end compression, verifies losslessness, and returns compression statistics."""
        self.build_tree_from_text(text)
        encoded_bits = self.encode(text)
        decoded_text = self.decode(encoded_bits)

        # Lossless verification
        assert decoded_text == text, "Decoded text does not match original text (lossy failure)!"

        original_chars = len(text)
        original_bits = original_chars * 8  # Standard ASCII 8 bits per character
        compressed_bits = len(encoded_bits)
        compressed_bytes = (compressed_bits + 7) // 8

        ratio = (compressed_bits / original_bits) if original_bits > 0 else 1.0
        saving_pct = (1.0 - ratio) * 100.0 if original_bits > 0 else 0.0

        stats = {
            "original_character_count": original_chars,
            "original_size_bits": original_bits,
            "original_size_bytes": original_chars,
            "compressed_size_bits": compressed_bits,
            "compressed_size_bytes": compressed_bytes,
            "compression_ratio": round(ratio, 4),
            "space_saving_percentage": round(saving_pct, 2),
            "unique_characters": len(self.frequencies),
            "is_lossless": True,
            "codebook_sample": dict(sorted(self.char_to_code.items(), key=lambda x: len(x[1]))[:10])
        }

        return encoded_bits, stats
