import java.io.File

val lines = File("input.txt")
    .readLines()
    .filter { it.isNotBlank() }
    .map { it.toInt() }


fun part1(lines: List<Int>): Int {
    return lines
        .windowed(2)
        .count { it.first() < it.last() }
}

fun part2(lines: List<Int>): Int {
    return lines
        .windowed(4)
        .count { it.first() < it.last() }
}

println("Part 1: ${part1(lines)}")
println("Part 2: ${part2(lines)}")
