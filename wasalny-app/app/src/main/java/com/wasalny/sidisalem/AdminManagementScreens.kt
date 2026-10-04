package com.wasalny.sidisalem

import android.graphics.BitmapFactory
import android.util.Base64
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
fun AdminPassengersTab() {
    val repository = remember { FirebaseRidesRepository() }
    val scope = rememberCoroutineScope()
    var passengers by remember { mutableStateOf<List<PassengerRecord>>(emptyList()) }
    var selectedAction by remember { mutableStateOf<Pair<PassengerRecord, Int?>?>(null) }
    var busy by remember { mutableStateOf(false) }
    var loading by remember { mutableStateOf(true) }
    var error by remember { mutableStateOf<String?>(null) }

    suspend fun refresh() {
        loading = true
        try {
            passengers = repository.listPassengers()
            error = null
        } catch (e: Exception) {
            error = e.toUserMessage("تعذر تحميل قائمة الركاب")
        } finally {
            loading = false
        }
    }
    LaunchedEffect(Unit) { refresh() }

    Column(Modifier.fillMaxSize().padding(12.dp)) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("الركاب • أحدث 100 حساب", fontWeight = FontWeight.Bold)
            TextButton(enabled = !loading && !busy, onClick = { scope.launch { refresh() } }) { Text("تحديث") }
        }
        error?.let { Text(it, color = Color(0xFFB3261E)) }
        if (loading) CircularProgressIndicator(Modifier.align(Alignment.CenterHorizontally))
        else if (passengers.isEmpty()) Text("لا توجد حسابات ركاب بعد.", color = Color.Gray)
        else LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(passengers, key = { it.uid }) { passenger ->
                Card(Modifier.fillMaxWidth()) {
                    Row(
                        Modifier.fillMaxWidth().padding(12.dp),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        PassengerProfilePhoto(passenger.profileImageBase64)
                        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            Text(passenger.name.ifBlank { "بدون اسم" }, fontWeight = FontWeight.Bold)
                            Text(passenger.phone, color = Color.Gray)
                            Text(if (passenger.isBanned) "موقوف مؤقتاً" else "الحساب نشط", color = if (passenger.isBanned) Color(0xFFB3261E) else Color(0xFF287D47))
                            Text("UID: ${passenger.uid}", color = Color.Gray, fontSize = 10.sp)
                        }
                        if (passenger.isBanned) {
                            OutlinedButton(enabled = !busy, onClick = { selectedAction = passenger to null }) { Text("رفع الإيقاف") }
                        } else {
                            Column(horizontalAlignment = Alignment.End) {
                                TextButton(enabled = !busy, onClick = { selectedAction = passenger to 24 }) { Text("إيقاف 24 ساعة") }
                                TextButton(enabled = !busy, onClick = { selectedAction = passenger to 168 }) { Text("إيقاف 7 أيام") }
                            }
                        }
                    }
                }
            }
        }
    }

    selectedAction?.let { (passenger, duration) ->
        AlertDialog(
            onDismissRequest = { if (!busy) selectedAction = null },
            title = { Text(if (duration == null) "رفع إيقاف الراكب" else "إيقاف الراكب") },
            text = {
                Text(
                    if (duration == null) "سيتمكن ${passenger.name.ifBlank { "هذا الراكب" }} من طلب الرحلات مرة أخرى."
                    else "سيُمنع ${passenger.name.ifBlank { "هذا الراكب" }} من طلب الرحلات لمدة ${if (duration == 24) "24 ساعة" else "7 أيام"}."
                )
            },
            confirmButton = {
                Button(enabled = !busy, onClick = {
                    busy = true
                    scope.launch {
                        try {
                            repository.setPassengerBan(passenger.uid, duration)
                            selectedAction = null
                            refresh()
                        } catch (e: Exception) {
                            error = e.toUserMessage("تعذر تحديث حالة الراكب")
                        } finally {
                            busy = false
                        }
                    }
                }) { Text(if (duration == null) "رفع الإيقاف" else "تأكيد") }
            },
            dismissButton = { TextButton(enabled = !busy, onClick = { selectedAction = null }) { Text("إلغاء") } }
        )
    }
}

@Composable
private fun PassengerProfilePhoto(base64: String) {
    var bitmap by remember(base64) { mutableStateOf<ImageBitmap?>(null) }
    LaunchedEffect(base64) {
        bitmap = if (base64.isBlank()) null else withContext(Dispatchers.IO) {
            runCatching {
                val bytes = Base64.decode(base64, Base64.DEFAULT)
                BitmapFactory.decodeByteArray(bytes, 0, bytes.size)?.asImageBitmap()
            }.getOrNull()
        }
    }
    if (bitmap != null) {
        Image(bitmap!!, contentDescription = "صورة الراكب", modifier = Modifier.size(56.dp).clip(CircleShape))
    } else {
        Text("👤", fontSize = 32.sp, modifier = Modifier.padding(8.dp))
    }
}

private val permissionLabels = listOf(
    "drivers" to "إدارة السائقين",
    "subscriptions" to "مراجعة الاشتراكات",
    "rides" to "سجل الرحلات",
    "ratings" to "التقييمات",
    "passengers" to "إدارة الركاب",
    "pricing" to "المناطق والأسعار"
)

@Composable
fun AdminSupervisorsTab() {
    val repository = remember { FirebaseRidesRepository() }
    val scope = rememberCoroutineScope()
    var supervisors by remember { mutableStateOf<List<SupervisorRecord>>(emptyList()) }
    var invitations by remember { mutableStateOf<List<SupervisorInvitation>>(emptyList()) }
    var phone by remember { mutableStateOf("") }
    var selectedPermissions by remember { mutableStateOf(setOf("drivers")) }
    var editing by remember { mutableStateOf<SupervisorRecord?>(null) }
    var loading by remember { mutableStateOf(true) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    val actorUid = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid

    suspend fun refresh() {
        loading = true
        try {
            supervisors = repository.listSupervisors()
            invitations = repository.listSupervisorInvitations()
            error = null
        } catch (e: Exception) {
            error = e.toUserMessage("تعذر تحميل المشرفين")
        } finally {
            loading = false
        }
    }
    LaunchedEffect(Unit) { refresh() }

    Column(
        Modifier.fillMaxSize().padding(12.dp).verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("صلاحيات فرعية للمشرفين", fontWeight = FontWeight.Bold)
        Text("أدخل رقم الهاتف الذي سيستخدمه المشرف في تسجيل الدخول. لا تُمنح الصلاحيات إلا بعد التحقق من الرقم.", color = Color.Gray)
        OutlinedTextField(
            value = phone,
            onValueChange = { phone = it.take(24) },
            label = { Text(if (editing == null) "رقم موبايل المشرف" else "رقم المشرف") },
            enabled = !busy && editing == null,
            singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
            modifier = Modifier.fillMaxWidth()
        )
        if (editing != null) Text("تعديل صلاحيات ${editing!!.phone}", color = Color.Gray)
        permissionLabels.forEach { (permission, label) ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(
                    checked = permission in selectedPermissions,
                    onCheckedChange = { checked ->
                        selectedPermissions = if (checked) selectedPermissions + permission else selectedPermissions - permission
                    },
                    enabled = !busy
                )
                Text(label)
            }
        }
        if (selectedPermissions.isEmpty()) Text("اختر صلاحية واحدة على الأقل.", color = Color(0xFFB3261E))
        error?.let { Text(it, color = Color(0xFFB3261E)) }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(
                enabled = !busy && selectedPermissions.isNotEmpty() &&
                    (editing != null || isValidEgyptPhone(phone)),
                onClick = {
                    busy = true
                    scope.launch {
                        try {
                            if (editing != null) {
                                repository.updateSupervisorAccess(editing!!.uid, editing!!.active, selectedPermissions)
                            } else {
                                val uid = actorUid ?: error("انتهت جلسة المشرف")
                                val normalized = normalizeEgyptPhoneStrict(phone) ?: error("رقم الهاتف المصري غير صالح")
                                if (supervisors.any { it.phone == normalized }) {
                                    error("هذا الرقم مرتبط بمشرف بالفعل. استخدم تعديل الصلاحيات.")
                                }
                                repository.saveSupervisorInvitation(normalized, selectedPermissions, uid)
                            }
                            phone = ""
                            editing = null
                            selectedPermissions = setOf("drivers")
                            refresh()
                        } catch (e: Exception) {
                            error = e.toUserMessage("تعذر حفظ الصلاحيات")
                        } finally {
                            busy = false
                        }
                    }
                }
            ) { Text(if (editing == null) "إرسال دعوة" else "حفظ الصلاحيات") }
            if (editing != null) {
                TextButton(enabled = !busy, onClick = {
                    phone = ""
                    editing = null
                    selectedPermissions = setOf("drivers")
                }) { Text("إلغاء التعديل") }
            } else {
                TextButton(enabled = !busy && !loading, onClick = { scope.launch { refresh() } }) { Text("تحديث القائمة") }
            }
        }

        Spacer(Modifier.height(8.dp))
        Text("المشرفون المسجلون", fontWeight = FontWeight.Bold)
        supervisors.forEach { supervisor ->
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(supervisor.phone, fontWeight = FontWeight.Medium)
                    Text(permissionLabels.filter { it.first in supervisor.permissions }.joinToString(" • ") { it.second }.ifBlank { "لا توجد صلاحيات" }, color = Color.Gray)
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        TextButton(enabled = !busy, onClick = {
                            editing = supervisor
                            phone = supervisor.phone
                            selectedPermissions = supervisor.permissions
                        }) { Text("تعديل") }
                        TextButton(enabled = !busy, onClick = {
                            busy = true
                            scope.launch {
                                try {
                                    repository.updateSupervisorAccess(
                                        supervisor.uid,
                                        !supervisor.active,
                                        supervisor.permissions.ifEmpty { setOf("drivers") }
                                    )
                                    refresh()
                                } catch (e: Exception) {
                                    error = e.toUserMessage("تعذر تغيير حالة المشرف")
                                } finally {
                                    busy = false
                                }
                            }
                        }) { Text(if (supervisor.active) "إيقاف" else "تفعيل") }
                    }
                    Text(if (supervisor.active) "نشط" else "موقوف", color = if (supervisor.active) Color(0xFF287D47) else Color(0xFFB3261E))
                }
            }
        }

        Text("دعوات تنتظر أول دخول", fontWeight = FontWeight.Bold)
        invitations.forEach { invitation ->
            Card(Modifier.fillMaxWidth()) {
                Row(
                    Modifier.fillMaxWidth().padding(10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(Modifier.weight(1f)) {
                        Text(invitation.phone, fontWeight = FontWeight.Medium)
                        Text(permissionLabels.filter { it.first in invitation.permissions }.joinToString(" • ") { it.second }, color = Color.Gray)
                    }
                    TextButton(enabled = !busy, onClick = {
                        busy = true
                        scope.launch {
                            try {
                                repository.deleteSupervisorInvitation(invitation.phone)
                                refresh()
                            } catch (e: Exception) {
                                error = e.toUserMessage("تعذر إلغاء الدعوة")
                            } finally {
                                busy = false
                            }
                        }
                    }) { Text("إلغاء") }
                }
            }
        }
        if (loading) CircularProgressIndicator(Modifier.align(Alignment.CenterHorizontally))
    }
}

@Composable
fun AdminFareZonesTab() {
    val repository = remember { FirebaseRidesRepository() }
    val scope = rememberCoroutineScope()
    var zones by remember { mutableStateOf<List<FareZone>>(emptyList()) }
    var editing by remember { mutableStateOf<FareZone?>(null) }
    var deleting by remember { mutableStateOf<FareZone?>(null) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        val listener = repository.listenFareZones(
            { zones = it.sortedBy { zone -> zone.name } },
            { error = it.toUserMessage("تعذر تحميل مناطق الأسعار") }
        )
        try {
            kotlinx.coroutines.awaitCancellation()
        } finally {
            listener.remove()
        }
    }

    Column(Modifier.fillMaxSize().padding(12.dp)) {
        Text("مناطق الخدمة والأسعار", fontWeight = FontWeight.Bold)
        Text("السعر المعروض للراكب إرشادي بناءً على المسافة المباشرة؛ عرض السائق هو السعر النهائي.", color = Color.Gray)
        error?.let { Text(it, color = Color(0xFFB3261E)) }
        Button(enabled = !busy, onClick = { editing = FareZone("", "", Config.LAT, Config.LON, 5.0, 0.0, 0.0, 1.0, true) }) {
            Text("إضافة منطقة")
        }
        if (zones.isEmpty()) Text("لا توجد مناطق أسعار معرفة. سيستمر نطاق الخدمة الحالي حتى إضافة منطقة.", color = Color.Gray)
        LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(zones, key = { it.id }) { zone ->
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text(zone.name, fontWeight = FontWeight.Bold)
                            Switch(
                                checked = zone.active,
                                enabled = !busy,
                                onCheckedChange = { active ->
                                    busy = true
                                    scope.launch {
                                        try { repository.saveFareZone(zone.copy(active = active)) }
                                        catch (e: Exception) { error = e.toUserMessage("تعذر تحديث المنطقة") }
                                        finally { busy = false }
                                    }
                                }
                            )
                        }
                        Text("المركز: %.5f, %.5f • النطاق: %.1f كم".format(zone.centerLat, zone.centerLon, zone.radiusKm), color = Color.Gray)
                        Text("الأساسي ${zone.baseFare.toInt()} ج • لكل كم ${zone.perKmFare.toInt()} ج • الحد الأدنى ${zone.minimumFare.toInt()} ج", color = Color.Gray)
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            TextButton(enabled = !busy, onClick = { editing = zone }) { Text("تعديل") }
                            TextButton(enabled = !busy, onClick = { deleting = zone }) { Text("حذف") }
                        }
                    }
                }
            }
        }
    }

    editing?.let { zone ->
        FareZoneEditor(
            initial = zone,
            onDismiss = { if (!busy) editing = null },
            onSave = { changed ->
                busy = true
                scope.launch {
                    try {
                        repository.saveFareZone(changed)
                        editing = null
                    } catch (e: Exception) {
                        error = e.toUserMessage("تعذر حفظ المنطقة")
                    } finally {
                        busy = false
                    }
                }
            }
        )
    }
    deleting?.let { zone ->
        AlertDialog(
            onDismissRequest = { deleting = null },
            title = { Text("حذف منطقة الأسعار") },
            text = { Text("سيُحذف إعداد ${zone.name}. لن يؤثر ذلك في الرحلات المسجلة.") },
            confirmButton = {
                Button(enabled = !busy, onClick = {
                    busy = true
                    scope.launch {
                        try {
                            repository.deleteFareZone(zone.id)
                            deleting = null
                        } catch (e: Exception) {
                            error = e.toUserMessage("تعذر حذف المنطقة")
                        } finally {
                            busy = false
                        }
                    }
                }) { Text("حذف") }
            },
            dismissButton = { TextButton(onClick = { deleting = null }) { Text("إلغاء") } }
        )
    }
}

@Composable
private fun FareZoneEditor(
    initial: FareZone,
    onDismiss: () -> Unit,
    onSave: (FareZone) -> Unit
) {
    var name by remember(initial.id) { mutableStateOf(initial.name) }
    var lat by remember(initial.id) { mutableStateOf(initial.centerLat.toString()) }
    var lon by remember(initial.id) { mutableStateOf(initial.centerLon.toString()) }
    var radius by remember(initial.id) { mutableStateOf(initial.radiusKm.toString()) }
    var base by remember(initial.id) { mutableStateOf(initial.baseFare.toString()) }
    var perKm by remember(initial.id) { mutableStateOf(initial.perKmFare.toString()) }
    var minimum by remember(initial.id) { mutableStateOf(initial.minimumFare.toString()) }
    var validationError by remember(initial.id) { mutableStateOf<String?>(null) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (initial.id.isBlank()) "منطقة أسعار جديدة" else "تعديل المنطقة") },
        text = {
            Column(
                Modifier.fillMaxWidth().heightIn(max = 460.dp).verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text("المركز الافتراضي هو مركز الخدمة الحالي. أدخل الأسعار التي تريد عرضها كتقدير.", color = Color.Gray)
                OutlinedTextField(name, { name = it }, label = { Text("اسم المنطقة") }, singleLine = true)
                OutlinedTextField(lat, { lat = it }, label = { Text("خط العرض للمركز") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                OutlinedTextField(lon, { lon = it }, label = { Text("خط الطول للمركز") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                OutlinedTextField(radius, { radius = it }, label = { Text("نطاق الخدمة بالكيلومتر") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                OutlinedTextField(base, { base = it }, label = { Text("السعر الأساسي بالجنيه") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                OutlinedTextField(perKm, { perKm = it }, label = { Text("السعر لكل كيلومتر بالجنيه") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                OutlinedTextField(minimum, { minimum = it }, label = { Text("الحد الأدنى بالجنيه") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal), singleLine = true)
                validationError?.let { Text(it, color = Color(0xFFB3261E)) }
            }
        },
        confirmButton = {
            Button(onClick = {
                val changed = FareZone(
                    id = initial.id,
                    name = name.trim(),
                    centerLat = lat.toDoubleOrNull() ?: Double.NaN,
                    centerLon = lon.toDoubleOrNull() ?: Double.NaN,
                    radiusKm = radius.toDoubleOrNull() ?: Double.NaN,
                    baseFare = base.toDoubleOrNull() ?: Double.NaN,
                    perKmFare = perKm.toDoubleOrNull() ?: Double.NaN,
                    minimumFare = minimum.toDoubleOrNull() ?: Double.NaN,
                    active = initial.active
                )
                if (changed.name.length !in 2..60 || !changed.centerLat.isFinite() || !changed.centerLon.isFinite() ||
                    !changed.radiusKm.isFinite() || !changed.baseFare.isFinite() || !changed.perKmFare.isFinite() ||
                    !changed.minimumFare.isFinite()
                ) {
                    validationError = "أكمل الحقول بأرقام صالحة."
                } else {
                    validationError = null
                    onSave(changed)
                }
            }) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } }
    )
}