# وصلني — بناء APK من GitHub

## 1) إنشاء Repository
- افتح GitHub وأنشئ Repository جديد، ويفضل Private.
- ارفع **محتويات هذا المجلد** إلى جذر الـ Repository.
- تأكد أن الملف `.github/workflows/build-apk.yml` موجود.

## 2) إعداد Firebase
- فعّل Phone Authentication وأنشئ Firestore، ثم انشر القواعد والفهارس وCloud Functions حسب [FIRESTORE_SETUP_AR.md](FIRESTORE_SETUP_AR.md).
- ملف `app/google-services.json` الحالي إعداد عميل Firebase عام وموجود في المستودع ليعمل البناء من checkout نظيف؛ لا يحتوي بيانات اعتماد Admin SDK أو مفتاح خدمة. قيّد مفتاح API من Google Cloud حسب التطبيقات وواجهات API المستخدمة.
- يستخدم workflow بناء APK الملف المتتبع مباشرة. يستطيع workflow التحقق استبداله بسر GitHub اختياري باسم `GOOGLE_SERVICES_JSON` يحتوي JSON بصيغة Base64؛ على Linux يمكن توليده باستخدام `base64 -w0 app/google-services.json`.
- يستخدم عرض الخرائط OpenStreetMap ولا يحتاج مفتاح Google Maps؛ يلزم إنترنت لتحميل البلاطات.

## 3) تشغيل البناء
من GitHub:
Actions → Build Wasalny APK → Run workflow

أو اعمل Push على فرع `main`.

## 4) تنزيل APK
بعد نجاح الـ workflow:
Actions → افتح آخر تشغيل ناجح → Artifacts → `Wasalny-APK`

نزّل الملف المضغوط واستخرج APK ثم ثبته على الموبايل.

## ملاحظات
- هذه نسخة Debug للتجربة.
- `minSdk 24`، أي Android 7 أو أحدث.
- الـ workflow يستخدم JDK 21 وGradle Wrapper 8.7 وAndroid SDK.
