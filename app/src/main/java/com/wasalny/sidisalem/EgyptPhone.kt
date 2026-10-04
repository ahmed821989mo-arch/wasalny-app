package com.wasalny.sidisalem

fun normalizeEgyptPhoneStrict(value: String): String? {
    val digits = value.filter(Char::isDigit)
    val normalized = when {
        digits.startsWith("00") -> digits.drop(2)
        digits.startsWith("+") -> digits
        else -> digits
    }
    val candidate = when {
        normalized.startsWith("0") -> "2$normalized"
        normalized.startsWith("2") -> normalized
        normalized.length == 10 && normalized.startsWith("1") -> "2$normalized"
        else -> normalized
    }
    return if (Regex("^2(?:0|1|2|5)[0-9]{10}$").matches(candidate)) "+$candidate" else null
}

fun isValidEgyptPhone(value: String): Boolean = normalizeEgyptPhoneStrict(value) != null
