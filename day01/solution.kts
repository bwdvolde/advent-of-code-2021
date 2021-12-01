import java.io.File

val lines = File("input.txt")
    .readLines()
    .filter { it.isNotBlank() }
    .map { it.toInt() }


fun part1(lines: List<Int>): Int {
    return lines
        .zipWithNext()
        .filter { it.second > it.first }
        .count()
}

fun part2(lines: List<Int>): Int {
    return (0 until lines.size - 3)
        .filter { i -> lines[i] < lines[i + 3] }
        .count()
}

println("Part 1: ${part1(lines)}")
println("Part 2: ${part2(lines)}")
