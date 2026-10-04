package com.wasalny.sidisalem

fun normalizeEgyptPhoneStrict(value: String): String? {
    val digits = buildString {
        value.forEach { character ->
            val digit = Character.digit(character, 10)
            if (digit >= 0) append(digit)
        }
    }

    val localNumber = when {
        digits.startsWith("00") -> digits.drop(2).removePrefix("20")
        digits.startsWith("20") -> digits.drop(2)
        digits.startsWith("0") -> digits.drop(1)
        else -> digits
    }
    if (localNumber.length != 10 || localNumber.take(2) !in setOf("10", "11", "12", "15")) {
        return null
    }
    return "+20$localNumber"
}

fun isValidEgyptPhone(value: String): Boolean = normalizeEgyptPhoneStrict(value) != null

fun isValidTukTukPlate(value: String): Boolean {
    val plate = value.trim()
    return plate.length in 2..20 && plate.any(Char::isLetterOrDigit) &&
        plate.all { it.isLetterOrDigit() || it == ' ' || it == '-' }
}