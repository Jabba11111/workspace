"""
Pattern Analyzer - learns generation rules from sample data.

Two modes:
1. Pattern mode: detects numeric/format patterns and generates similar values
2. Rotation mode: cycles through given examples when values are from a fixed set
"""

import random
import re
from typing import Optional


class PatternAnalyzer:
    """Analyzes sample values and derives generation rules."""

    def __init__(self, sample_values: list):
        self.samples = [str(v).strip() for v in sample_values
                        if str(v).strip() and str(v).strip().lower() != "nan"]
        self.pattern = None
        self._generator_fn = None

        if self.samples:
            self._analyze()

    def _analyze(self):
        """Analyze samples and determine the best generation strategy."""
        # Strategy 1: Fixed set (few unique values, or structured "code - label" pairs)
        if self._detect_fixed_set():
            return

        # Strategy 2: Numeric pattern (integers, decimals, prefixed numbers)
        if self._detect_numeric_pattern():
            return

        # Strategy 3: Alphanumeric format pattern (e.g. "AB-123456")
        if self._detect_format_pattern():
            return

        # Fallback: rotation through examples
        self.pattern = {"type": "rotation", "values": list(self.samples)}
        self._generator_fn = self._gen_rotation

    def _detect_fixed_set(self) -> bool:
        """Detect if values come from a small fixed set (e.g. dropdown/enum)."""
        unique = list(dict.fromkeys(self.samples))  # preserve order, deduplicate

        # If there are structured "code - label" pairs
        coded_pattern = all(re.match(r"^\d+\s*-\s*.+$", v) for v in unique)
        if coded_pattern:
            self.pattern = {"type": "fixed_set", "values": unique}
            self._generator_fn = self._gen_rotation
            return True

        # If few unique values relative to total samples, treat as fixed set
        if len(unique) <= max(5, len(self.samples) * 0.3):
            # Check for non-numeric diversity (not just random numbers)
            all_numeric = all(re.match(r"^[\d.,]+$", v) for v in unique)
            if not all_numeric or len(unique) <= 5:
                if len(unique) < len(self.samples) * 0.8:
                    self.pattern = {"type": "fixed_set", "values": unique}
                    self._generator_fn = self._gen_rotation
                    return True

        return False

    def _detect_numeric_pattern(self) -> bool:
        """Detect numeric patterns: pure integers, decimals, prefixed numbers."""
        # Try to parse all as numbers (with possible unit suffix)
        cleaned = []
        suffix = ""
        for v in self.samples:
            # Extract possible unit suffix: "16898 kWh" -> (16898, " kWh")
            m = re.match(r"^([\d.,]+)\s*(.*)$", v)
            if not m:
                return False
            num_str = m.group(1).replace(",", ".")
            if m.group(2):
                if not suffix:
                    suffix = " " + m.group(2)
                elif " " + m.group(2) != suffix:
                    return False  # inconsistent suffixes
            try:
                cleaned.append(float(num_str))
            except ValueError:
                return False

        if not cleaned:
            return False

        # Determine prefix (common leading digits)
        str_values = [re.match(r"^[\d.,]+", v).group().replace(",", ".") for v in self.samples]
        prefix = self._find_common_prefix_digits(str_values)

        # Determine if integer or decimal
        is_decimal = any("." in sv for sv in str_values)

        # Determine digit count (length of numeric part)
        lengths = [len(sv.replace(".", "").replace(",", "")) for sv in str_values]
        if is_decimal:
            # Count decimal places
            dec_places = []
            for sv in str_values:
                if "." in sv:
                    dec_places.append(len(sv.split(".")[-1]))
                else:
                    dec_places.append(0)
            max_dec = max(dec_places) if dec_places else 2

            min_val = min(cleaned)
            max_val = max(cleaned)
            # Add some margin
            margin = (max_val - min_val) * 0.2 if max_val > min_val else max_val * 0.5
            self.pattern = {
                "type": "decimal",
                "min": max(0, min_val - margin),
                "max": max_val + margin,
                "decimals": max_dec,
                "prefix": prefix,
                "suffix": suffix,
            }
            self._generator_fn = self._gen_decimal
            return True
        else:
            # Integer pattern
            int_values = [int(c) for c in cleaned]
            min_val = min(int_values)
            max_val = max(int_values)

            # Check consistent digit count
            digit_counts = set(lengths)
            fixed_length = lengths[0] if len(digit_counts) == 1 else None

            if prefix and fixed_length:
                # Prefixed fixed-length number like "80xxxxxxxx"
                suffix_len = fixed_length - len(prefix)
                self.pattern = {
                    "type": "prefixed_integer",
                    "prefix": prefix,
                    "suffix_length": suffix_len,
                    "suffix_text": suffix,
                }
                self._generator_fn = self._gen_prefixed_integer
            elif fixed_length:
                # Fixed-length number (e.g. 8 digits, 10 digits)
                self.pattern = {
                    "type": "fixed_length_integer",
                    "length": fixed_length,
                    "min": min_val,
                    "max": max_val,
                    "suffix": suffix,
                }
                self._generator_fn = self._gen_fixed_length_integer
            else:
                # Variable-length integer in a range
                margin = int((max_val - min_val) * 0.2) if max_val > min_val else max(1, int(max_val * 0.5))
                self.pattern = {
                    "type": "integer",
                    "min": max(0, min_val - margin),
                    "max": max_val + margin,
                    "suffix": suffix,
                }
                self._generator_fn = self._gen_integer
            return True

    def _detect_format_pattern(self) -> bool:
        """Detect alphanumeric format patterns like 'AB-123456', 'PRJ-2024-001'."""
        if len(self.samples) < 2:
            # With very few samples, just rotate
            return False

        # Try to find a common structure: split into literal and variable parts
        # Build a regex-like template from the samples
        template = self._build_template(self.samples)
        if template:
            self.pattern = {"type": "template", "template": template, "samples": list(self.samples)}
            self._generator_fn = self._gen_from_template
            return True

        return False

    def _find_common_prefix_digits(self, str_values: list) -> str:
        """Find common leading digit prefix across all values."""
        if not str_values:
            return ""
        prefix = str_values[0]
        for v in str_values[1:]:
            while not v.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        # Only keep digit prefix
        digit_prefix = ""
        for ch in prefix:
            if ch.isdigit():
                digit_prefix += ch
            else:
                break
        return digit_prefix

    def _build_template(self, samples: list) -> Optional[list]:
        """Build a generation template from samples.

        Returns a list of segments:
        - {"type": "literal", "value": "-"}
        - {"type": "digits", "length": 4, "min": 1000, "max": 9999}
        - {"type": "alpha", "length": 2, "case": "upper"}
        - {"type": "choice", "values": ["A", "B", "C"]}
        """
        if not samples or len(samples) < 2:
            return None

        # Tokenize each sample into character-type runs
        def tokenize(s):
            tokens = []
            i = 0
            while i < len(s):
                if s[i].isdigit():
                    j = i
                    while j < len(s) and s[j].isdigit():
                        j += 1
                    tokens.append(("D", s[i:j]))
                    i = j
                elif s[i].isalpha():
                    j = i
                    while j < len(s) and s[j].isalpha():
                        j += 1
                    tokens.append(("A", s[i:j]))
                    i = j
                else:
                    j = i
                    while j < len(s) and not s[j].isdigit() and not s[j].isalpha():
                        j += 1
                    tokens.append(("S", s[i:j]))
                    i = j
            return tokens

        tokenized = [tokenize(s) for s in samples]

        # Check all have same number of tokens and same types
        token_types = [tuple(t[0] for t in toks) for toks in tokenized]
        if len(set(token_types)) != 1:
            return None

        template = []
        type_pattern = token_types[0]
        for idx, ttype in enumerate(type_pattern):
            values_at_pos = [toks[idx][1] for toks in tokenized]
            unique_vals = list(set(values_at_pos))

            if ttype == "S":
                # Separator/literal - should be the same across all
                if len(unique_vals) == 1:
                    template.append({"type": "literal", "value": unique_vals[0]})
                else:
                    return None  # Inconsistent separators
            elif ttype == "D":
                lengths = set(len(v) for v in values_at_pos)
                int_vals = [int(v) for v in values_at_pos]
                if len(lengths) == 1:
                    length = lengths.pop()
                    template.append({
                        "type": "digits",
                        "length": length,
                        "min": min(int_vals),
                        "max": max(int_vals),
                    })
                else:
                    template.append({
                        "type": "digits",
                        "length": max(lengths),
                        "min": min(int_vals),
                        "max": max(int_vals),
                    })
            elif ttype == "A":
                if len(unique_vals) <= 5:
                    template.append({"type": "choice", "values": unique_vals})
                else:
                    length = max(len(v) for v in values_at_pos)
                    is_upper = all(v.isupper() for v in values_at_pos)
                    template.append({
                        "type": "alpha",
                        "length": length,
                        "case": "upper" if is_upper else "mixed",
                    })

        return template

    # --- Generator functions ---

    def generate(self) -> str:
        """Generate a new value based on the analyzed pattern."""
        if self._generator_fn:
            return self._generator_fn()
        return random.choice(self.samples) if self.samples else ""

    def _gen_rotation(self) -> str:
        return random.choice(self.pattern["values"])

    def _gen_decimal(self) -> str:
        p = self.pattern
        val = random.uniform(p["min"], p["max"])
        result = f"{val:.{p['decimals']}f}"
        return result + p.get("suffix", "")

    def _gen_integer(self) -> str:
        p = self.pattern
        val = random.randint(int(p["min"]), int(p["max"]))
        return str(val) + p.get("suffix", "")

    def _gen_fixed_length_integer(self) -> str:
        p = self.pattern
        length = p["length"]
        min_val = max(p["min"], 10 ** (length - 1))
        max_val = min(p["max"], 10 ** length - 1)
        if min_val > max_val:
            min_val = 10 ** (length - 1)
            max_val = 10 ** length - 1
        val = random.randint(min_val, max_val)
        return str(val) + p.get("suffix_text", p.get("suffix", ""))

    def _gen_prefixed_integer(self) -> str:
        p = self.pattern
        suffix_len = p["suffix_length"]
        suffix_val = random.randint(0, 10 ** suffix_len - 1)
        return p["prefix"] + str(suffix_val).zfill(suffix_len) + p.get("suffix_text", "")

    def _gen_from_template(self) -> str:
        parts = []
        for segment in self.pattern["template"]:
            if segment["type"] == "literal":
                parts.append(segment["value"])
            elif segment["type"] == "digits":
                length = segment["length"]
                min_v = max(segment["min"], 10 ** (length - 1))
                max_v = min(segment["max"], 10 ** length - 1)
                if min_v > max_v:
                    min_v = 10 ** (length - 1)
                    max_v = 10 ** length - 1
                val = random.randint(min_v, max_v)
                parts.append(str(val).zfill(length))
            elif segment["type"] == "choice":
                parts.append(random.choice(segment["values"]))
            elif segment["type"] == "alpha":
                length = segment["length"]
                if segment["case"] == "upper":
                    parts.append("".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length)))
                else:
                    parts.append("".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length)))
        return "".join(parts)

    def describe(self) -> str:
        """Return a human-readable description of the detected pattern."""
        if not self.pattern:
            return "Geen patroon gedetecteerd"

        t = self.pattern["type"]
        if t == "fixed_set":
            return f"Vaste waarden ({len(self.pattern['values'])} opties)"
        elif t == "rotation":
            return f"Roulatie door {len(self.pattern['values'])} voorbeelden"
        elif t == "decimal":
            p = self.pattern
            return f"Decimaal {p['min']:.0f}-{p['max']:.0f} ({p['decimals']} decimalen){p.get('suffix', '')}"
        elif t == "integer":
            p = self.pattern
            return f"Geheel getal {p['min']}-{p['max']}"
        elif t == "fixed_length_integer":
            return f"Getal van {self.pattern['length']} cijfers"
        elif t == "prefixed_integer":
            p = self.pattern
            return f"Getal met prefix '{p['prefix']}' ({p['suffix_length']} + {len(p['prefix'])} cijfers)"
        elif t == "template":
            return f"Formaat-patroon (bijv. {self.samples[0]})"
        return "Onbekend patroon"
