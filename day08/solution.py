import time
from dataclasses import dataclass, replace

from util.read_file import read_file


@dataclass
class Entry:
    signal_patterns: list[str]
    output_signals: list[str]


lines = read_file("input.txt")[:-1]

entries = []
for line in lines:
    signal_patterns, output_signals = line.split(" | ")
    signal_patterns, output_signals = signal_patterns.split(), output_signals.split()
    entries.append(Entry(signal_patterns, output_signals))

part_1 = sum(1 for entry in entries for output_signal in entry.output_signals if len(output_signal) in [2, 4, 3, 7])
print(f"Part 1: {part_1}")

part_2 = 0
for entry in entries:

    decoded = [None] * 10
    easy_numbers = {
        1: 2,
        4: 4,
        7: 3,
        8: 7
    }

    for easy_number, n_segments in easy_numbers.items():
        decoded[easy_number] = [signal for signal in entry.signal_patterns if len(signal) == n_segments][0]

    len_6 = [signal for signal in entry.signal_patterns if len(signal) == 6]
    decoded[6] = [signal for signal in len_6 if set(decoded[1]) - set(signal)][0]
    decoded[9] = [signal for signal in len_6 if not set(decoded[4]) - set(signal)][0]
    decoded[0] = [signal for signal in len_6 if signal not in [decoded[6], decoded[9]]][0]

    len_5 = [signal for signal in entry.signal_patterns if len(signal) == 5]
    decoded[3] = [signal for signal in len_5 if not set(decoded[7]) - set(signal)][0]
    decoded[5] = [signal for signal in len_5 if len(set(decoded[9]) - set(signal)) == 1 and not signal == decoded[3]][0]
    decoded[2] = [signal for signal in len_5 if signal not in [decoded[3], decoded[5]]][0]

    result_entry = ""
    for output_signal in entry.output_signals:
        for i, decoded_entry in enumerate(decoded):
            if set(decoded_entry) == set(output_signal):
                result_entry += str(i)
                break
    result_entry = int(result_entry)
    part_2 += result_entry

print(f"Part 2: {part_2}")
