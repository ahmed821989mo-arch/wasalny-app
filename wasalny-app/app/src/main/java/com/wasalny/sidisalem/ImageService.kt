package com.wasalny.sidisalem

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.ByteArrayOutputStream
import kotlin.math.max
import kotlin.math.min

object ImageService {
    // Keep four driver documents plus their metadata safely below Firestore's 1 MiB limit.
    private const val MAX_COMPRESSED_BYTES = 140 * 1024

    suspend fun compressAndConvertToBase64(context: Context, uri: Uri): String = withContext(Dispatchers.IO) {
        val resolver = context.contentResolver
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        resolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, bounds) }
            ?: error("تعذر قراءة الصورة")
        require(bounds.outWidth > 0 && bounds.outHeight > 0) { "ملف الصورة غير صالح" }

        for (maxDimension in listOf(1200, 1000, 800, 700, 600)) {
            var sampleSize = 1
            while (max(bounds.outWidth, bounds.outHeight) / (sampleSize * 2) >= maxDimension) {
                sampleSize *= 2
            }
            val options = BitmapFactory.Options().apply { inSampleSize = sampleSize }
            val decoded = resolver.openInputStream(uri)?.use {
                BitmapFactory.decodeStream(it, null, options)
            } ?: error("تعذر قراءة الصورة")
            val targetWidth = max(1, min(decoded.width, maxDimension * decoded.width / max(decoded.width, decoded.height)))
            val targetHeight = max(1, min(decoded.height, maxDimension * decoded.height / max(decoded.width, decoded.height)))
            val bitmap = if (decoded.width != targetWidth || decoded.height != targetHeight) {
                Bitmap.createScaledBitmap(decoded, targetWidth, targetHeight, true).also { decoded.recycle() }
            } else {
                decoded
            }

            try {
                for (quality in listOf(40, 35, 30, 25, 20)) {
                    val output = ByteArrayOutputStream()
                    check(bitmap.compress(Bitmap.CompressFormat.JPEG, quality, output)) { "تعذر ضغط الصورة" }
                    val bytes = output.toByteArray()
                    if (bytes.size <= MAX_COMPRESSED_BYTES) {
                        return@withContext Base64.encodeToString(bytes, Base64.NO_WRAP)
                    }
                }
            } finally {
                bitmap.recycle()
            }
        }
        error("تعذر ضغط الصورة إلى الحجم المسموح. اختر صورة أوضح وأصغر.")
    }
}
