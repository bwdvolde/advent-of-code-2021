import java.io.File

enum class Action {
    FORWARD,
    DOWN,
    UP
}

val regex = Regex("(forward|down|up) ([0-9]+)")

fun String.parse(): Pair<Action, Int> {
    return regex
        .matchEntire(this)!!
        .groupValues
        .let { Action.valueOf(it[1].toUpperCase()) to it[2].toInt() }
}

val actions = File("input.txt")
    .readLines()
    .filter { it.isNotBlank() }
    .map { it.parse() }

fun part1(actions: Collection<Pair<Action, Int>>): Int {
    data class Acc(val horizontal: Int, val depth: Int)

    return actions.fold(Acc(0, 0), { acc, (action, amount) ->
        when (action) {
            Action.FORWARD -> acc.copy(
                horizontal = acc.horizontal + amount
            )
            Action.DOWN -> acc.copy(
                depth = acc.depth + amount
            )
            Action.UP -> acc.copy(
                depth = acc.depth - amount
            )
        }
    })
        .let { it.depth * it.horizontal }
}

fun part2(actions: Collection<Pair<Action, Int>>): Int {
    data class Acc(val horizontal: Int, val depth: Int, val aim: Int)

    return actions.fold(Acc(0, 0, 0), { acc, (action, amount) ->
        when (action) {
            Action.FORWARD -> acc.copy(
                horizontal = acc.horizontal + amount,
                depth = acc.depth + acc.aim * amount
            )
            Action.DOWN -> acc.copy(
                aim = acc.aim + amount
            )
            Action.UP -> acc.copy(
                aim = acc.aim - amount
            )
        }
    })
        .let { it.depth * it.horizontal }
}

println("Part 1: ${part1(actions)}")
println("Part 2: ${part2(actions)}")

