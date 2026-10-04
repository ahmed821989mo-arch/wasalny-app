package com.wasalny.sidisalem

import android.app.Activity
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.google.firebase.FirebaseException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.PhoneAuthCredential
import com.google.firebase.auth.PhoneAuthOptions
import com.google.firebase.auth.PhoneAuthProvider
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import java.util.concurrent.TimeUnit

private val BrandGreen = Color(0xFF0D7C3E)
private val BrandGreenDark = Color(0xFF0A5A2C)
private val SurfaceMist = Color(0xFFF6FAF7)

@Composable
fun PhoneAuthScreen(onAuthenticated: () -> Unit) {
    val context = LocalContext.current
    val activity = context as? Activity
    val auth = remember { FirebaseAuth.getInstance() }
    val scope = rememberCoroutineScope()
    var phone by remember { mutableStateOf("") }
    var code by remember { mutableStateOf("") }
    var verificationId by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    fun finish(credential: PhoneAuthCredential) {
        busy = true
        scope.launch {
            try {
                auth.signInWithCredential(credential).await()
                onAuthenticated()
            } catch (e: Exception) {
                error = e.toUserMessage("تعذر تأكيد رقم الهاتف")
            } finally { busy = false }
        }
    }

    Column(Modifier.fillMaxSize().background(SurfaceMist)) {
        Box(
            Modifier.fillMaxWidth().height(190.dp).background(Brush.verticalGradient(listOf(BrandGreen, BrandGreenDark))),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("🛺", fontSize = 44.sp)
                Spacer(Modifier.height(6.dp))
                Text("وصلني توكتوك", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 26.sp)
                Text("رحلتك تبدأ من هنا", color = Color.White.copy(alpha = 0.85f), fontSize = 14.sp)
            }
        }
        Card(
            Modifier.fillMaxWidth().padding(20.dp),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(2.dp)
        ) {
            Column(Modifier.padding(20.dp)) {
                Text("تسجيل الدخول", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(4.dp))
                Text("أكد رقم الموبايل لحماية الركاب والسائقين.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 13.sp)
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(
                    value = phone,
                    onValueChange = { phone = it.filter { c -> c.isDigit() || c == '+' }.take(16) },
                    label = { Text("رقم الموبايل المصري") },
                    placeholder = { Text("01xxxxxxxxx") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                    singleLine = true,
                    enabled = verificationId == null && !busy,
                    modifier = Modifier.fillMaxWidth()
                )
                if (verificationId != null) {
                    Spacer(Modifier.height(10.dp))
                    OutlinedTextField(
                        value = code,
                        onValueChange = { code = it.filter(Char::isDigit).take(6) },
                        label = { Text("كود SMS") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        enabled = !busy,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
                if (error != null) {
                    Spacer(Modifier.height(8.dp))
                    Text(error!!, color = MaterialTheme.colorScheme.error, fontSize = 13.sp)
                }
                Spacer(Modifier.height(16.dp))
                Button(
                    enabled = !busy && if (verificationId == null) isValidEgyptPhone(phone) else code.length == 6,
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    shape = RoundedCornerShape(14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = BrandGreen),
                    onClick = {
                        error = null
                        if (verificationId == null) {
                            val normalizedPhone = normalizeEgyptPhoneStrict(phone)
                            if (normalizedPhone == null) {
                                error = "أدخل رقم موبايل مصري صحيح يبدأ بـ 010 أو 011 أو 012 أو 015"
                                return@Button
                            }
                            val act = activity
                            if (act == null) { error = "تعذر فتح تحقق الهاتف"; return@Button }
                            busy = true
                            val callbacks = object : PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                                override fun onVerificationCompleted(credential: PhoneAuthCredential) = finish(credential)
                                override fun onVerificationFailed(e: FirebaseException) {
                                    busy = false; error = e.toUserMessage("فشل إرسال كود SMS")
                                }
                                override fun onCodeSent(id: String, token: PhoneAuthProvider.ForceResendingToken) {
                                    verificationId = id; busy = false
                                }
                            }
                            PhoneAuthProvider.verifyPhoneNumber(
                                PhoneAuthOptions.newBuilder(auth)
                                    .setPhoneNumber(normalizedPhone)
                                    .setTimeout(60L, TimeUnit.SECONDS)
                                    .setActivity(act)
                                    .setCallbacks(callbacks)
                                    .build()
                            )
                        } else {
                            finish(PhoneAuthProvider.getCredential(verificationId!!, code))
                        }
                    }
                ) {
                    if (busy) CircularProgressIndicator(Modifier.size(20.dp), strokeWidth = 2.dp, color = Color.White)
                    else Text(if (verificationId == null) "إرسال كود SMS" else "تأكيد الرقم", fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}

@Composable
fun CustomerProfileScreen(onComplete: (String) -> Unit, onBack: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val repo = remember { FirebaseRidesRepository() }
    val uid = FirebaseAuth.getInstance().currentUser?.uid
    var name by remember { mutableStateOf("") }
    var error by remember { mutableStateOf<String?>(null) }
    var saving by remember { mutableStateOf(false) }
    val phone = FirebaseAuth.getInstance().currentUser?.phoneNumber.orEmpty()

    Column(Modifier.fillMaxSize().background(SurfaceMist).padding(24.dp), verticalArrangement = Arrangement.Center) {
        Card(
            Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(2.dp)
        ) {
            Column(Modifier.padding(20.dp)) {
                Text("بيانات الراكب", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(4.dp))
                Text("رقم الهاتف: ${phone.ifBlank { "غير معروف" }}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 13.sp)
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(name, { name = it }, label = { Text("الاسم") }, singleLine = true, modifier = Modifier.fillMaxWidth())
                if (error != null) { Spacer(Modifier.height(8.dp)); Text(error!!, color = MaterialTheme.colorScheme.error, fontSize = 13.sp) }
                Spacer(Modifier.height(16.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(onClick = onBack, enabled = !saving, modifier = Modifier.weight(1f).height(50.dp), shape = RoundedCornerShape(14.dp)) { Text("رجوع") }
                    Button(onClick = {
                        val id = uid
                        if (id == null) { error = "انتهت جلسة الحساب"; return@Button }
                        if (name.trim().length < 2) { error = "اكتب الاسم بالكامل"; return@Button }
                        if (!isValidEgyptPhone(phone)) { error = "رقم الهاتف الموثق ليس رقم موبايل مصريًا صحيحًا"; return@Button }
                        saving = true
                        scope.launch {
                            try {
                                repo.saveUserProfile(id, "customer", name.trim(), phone)
                                context.dataStore.edit {
                                    it[androidx.datastore.preferences.core.stringPreferencesKey("role_$id")] = "customer"
                                    it[androidx.datastore.preferences.core.stringPreferencesKey("user_name_$id")] = name.trim()
                                    it[androidx.datastore.preferences.core.stringPreferencesKey("user_phone_$id")] = phone
                                }
                                onComplete("customer")
                            } catch (e: Exception) { error = e.toUserMessage("تعذر حفظ البيانات") }
                            finally { saving = false }
                        }
                    }, enabled = !saving, modifier = Modifier.weight(1f).height(50.dp), shape = RoundedCornerShape(14.dp), colors = ButtonDefaults.buttonColors(containerColor = BrandGreen)) { Text("متابعة", fontWeight = FontWeight.SemiBold) }
                }
            }
        }
    }
}
