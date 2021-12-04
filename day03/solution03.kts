import java.io.File
import java.lang.RuntimeException

val lines = File("input.txt")
    .readLines()
    .filter { it.isNotBlank() }

fun part1(): Int {
    val mostCommonBits = (lines[0].indices)
        .map { i ->
            lines
                .map { it[i] }
                .groupBy { it }
                .maxByOrNull { it.value.size }!!
                .key
        }.joinToString(separator = "")

    val leastCommonBits = mostCommonBits.map {
        when (it) {
            '1' -> '0'
            '0' -> '1'
            else -> throw RuntimeException()
        }
    }.joinToString(separator = "")

    val gamma = mostCommonBits.toInt(2)
    val radix = leastCommonBits.toInt(2)

    return gamma * radix
}

fun part2(): Int {

    fun computeOxygenGeneratorRating(): Int {
        val remaining = lines.toMutableSet()
        var i = 0
        while (remaining.size > 1) {
            val occurrences = remaining
                .map { it[i] }
                .groupBy { it }
                .mapValues { it.value.size }
                .toMap()

            val toKeep = when {
                occurrences.getOrDefault('1', 0) == occurrences.getOrDefault('0', 0) -> '1'
                else -> occurrences.maxByOrNull { it.value }!!.key
            }
            remaining.removeIf { it[i] != toKeep }
            i += 1
        }
        return remaining
            .toList()
            .first()
            .toInt(2)
    }

    fun computeScrubberRating(): Int {
        val remaining = lines.toMutableSet()
        var i = 0
        while (remaining.size > 1) {
            val occurrences = remaining
                .map { it[i] }
                .groupBy { it }
                .mapValues { it.value.size }
                .toMap()

            val toKeep = when {
                occurrences.getOrDefault('0', 0) == occurrences.getOrDefault('1', 0) -> '0'
                else -> occurrences.minByOrNull { it.value }!!.key
            }
            remaining.removeIf { it[i] != toKeep }
            i += 1
        }
        return remaining
            .toList()
            .first()
            .toInt(2)
    }

    return computeOxygenGeneratorRating() * computeScrubberRating()
}
part1()
println("Part 1: ${part1()}")
println("Part 1: ${part2()}")
