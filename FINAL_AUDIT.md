# FINAL AUDIT - Wasalny Tuktuk

تاريخ الفحص: 2026-10-02

## النطاق

تم فك أرشيف المشروع إلى جذر المستودع الحالي، وفحص تطبيق Android/Kotlin وCompose والتنقل وFirebase وCloud Functions والقواعد والفهارس وGradle وManifest وGitHub Actions وملفات الإعداد. الأرشيف لا يحتوي مفاتيح خدمة أو مفاتيح توقيع خاصة؛ إعداد `google-services.json` إعداد عميل عام، وتطابق معرف مشروعه وحزمة Android.

## الملفات التي عُدلت

- `.gitignore`
- `.github/workflows/validate-project.yml`
- `README.md`
- `FIREBASE_SCHEMA.md`
- `firestore.rules`
- `firestore.indexes.json`
- `storage.rules`
- `functions/package.json` و`functions/package-lock.json`
- `functions/src/index.ts`
- `functions/test/firestore.rules.test.cjs`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/java/com/wasalny/sidisalem/MainActivity.kt`
- `app/src/main/java/com/wasalny/sidisalem/FirebaseRidesRepository.kt`
- `app/src/main/java/com/wasalny/sidisalem/RideScreens.kt`
- `app/src/main/java/com/wasalny/sidisalem/AuthScreens.kt`
- `app/src/main/java/com/wasalny/sidisalem/AdminScreens.kt`
- `app/src/main/java/com/wasalny/sidisalem/WasalnyMessagingService.kt`
- `FINAL_AUDIT.md`

ملفات التطبيق والإعداد التي كانت داخل الأرشيف وفُكّت إلى المستودع أُضيفت كما هي، ولم تُنشأ نسخة مشروع ثانية.

## المشاكل والإصلاحات

- مدخل المشرف كان يظهر داخل حساب المستخدم. أزيل من واجهة الراكب، وأصبح الدخول عبر `wasalny://admin` فقط؛ التحقق من UID ووثيقة `admins/{uid}` النشطة ما زال إلزاميًا، وقواعد Firestore تمنع قراءة بيانات المشرف أو تعديل الدور من العميل.
- تسجيل السائق كان يكتب سجلًا قبل انتهاء رفع الصور ويقبل نوع مركبة حرًا. التسجيل الآن أربع خطوات، والمركبة TukTuk فقط. تُرفع الصور أولًا مع فحص النوع والحجم والتقدم وإعادة المحاولة، ثم يتحقق Callable خادمي من UID والهاتف الموثق وبيانات Storage قبل إنشاء سجل `pending`. قواعد Firestore تمنع إنشاء سجل السائق أو تحريره مباشرة من العميل.
- إنشاء الرحلة ورقم التواصل كانا عمليتين منفصلتين. جُمِعا في Batch واحد، مع معرف ثابت لإعادة المحاولة. اختبارات القواعد تتحقق من السماح بالكتابة الذرية.
- قبول عرض السائق لم يحجز وثيقة السائق نفسها. أصبح الاختيار Callable خادميًا يغيّر الرحلة والعرض والدعوة وحالة التوفر داخل Transaction واحدة، ويعيد التحقق من الاشتراك والحالة؛ القواعد ترفض القبول المباشر من العميل.
- مغادرة شاشة الطلبات كانت توقف السائق. أصبحت خدمة الموقع مستقلة عن التنقل بين الشاشات، وتعود عند فتح التطبيق، ويُسمح للسائق بالتحول إلى Offline حتى دون إذن الموقع. أضيفت مهمة خادمية لإيقاف الاشتراكات المنتهية، مع فهرس وتحديثات مجزأة.
- البحث المجدول يعيد الحجز إلى `scheduled` عند فشل مؤقت بدل تركه عالقًا، وقراءة السائقين للحجوزات paginated، والكتابات موزعة على دفعات دون حد Firestore.
- أضيفت إشعارات المشرف لطلبات السائق والاشتراك واستكمال الطلب، ومعرف حدث ثابت لتقليل تكرار إشعارات Android. فشل FCM لا يوقف تدفق الرحلة.
- استُبدلت رسائل Firebase الداخلية في الواجهات برسائل آمنة ومفهومة. أزيل مسار تسجيل الدخول المجهول غير المستخدم.
- أزيل Firebase placeholder من GitHub Actions؛ يستخدم البناء إعداد Firebase الموجود أو Secret اختياريًا. أضيفت فحوص Functions والقواعد إلى workflow.

## الاختبارات والفحوص

- `npm ci`: نجح.
- `npm run build`: نجح.
- `npm run lint`: نجح.
- `npm run test:rules`: نجح، 9 اختبارات من 9 على Firestore وStorage Emulator.
- `npm audit --audit-level=moderate`: صفر ثغرات.
- تحليل JSON وGitHub Actions YAML: نجح.
- `./gradlew help` باستخدام JDK 21: نجح.
- `./gradlew :app:assembleDebug`: لم يكتمل. البيئة لا تحتوي Android SDK، ولا يوجد `ANDROID_HOME` أو `sdk.dir`؛ Gradle أوقف البناء برسالة `SDK location not found` قبل ترجمة Kotlin.
- لم تُشغّل اختبارات واجهة/جهاز Android أو اختبارًا حيًا لـCloud Functions. لم يتم نشر Firebase.

محاكي Storage أصدر تحذير Java `Unsafe` من runtime الخاص بالمحاكي، لكن جميع الاختبارات اكتملت بنجاح.

## خطوات التشغيل والبناء

- Android: ثبّت JDK 21 وAndroid SDK 35، ثم شغّل `./gradlew assembleDebug`.
- Cloud Functions: من `functions/` شغّل `npm ci` ثم `npm run build` و`npm run lint`.
- اختبارات القواعد: من `functions/` شغّل `npm run test:rules`؛ يلزم Java لتشغيل محاكيات Firebase.
- نشر Firebase بعد مراجعة المشروع المستهدف: `firebase deploy --only firestore:rules,firestore:indexes,storage,functions`.

## إعدادات Firebase المطلوبة

- تفعيل Phone Authentication وFirestore وFirebase Storage.
- تفعيل Cloud Functions وCloud Scheduler، وخطة Firebase المناسبة للـScheduler.
- توفير `app/google-services.json` المطابق للحزمة `com.wasalny.sidisalem`، أو Secret باسم `GOOGLE_SERVICES_JSON` بصيغة Base64 في GitHub Actions.
- إنشاء وثيقة لكل مشرف في `admins/{uid}` مع `role: admin` و`active: true` عبر مسار إداري موثوق، لا من التطبيق.
- إعداد bucket الخاص بـStorage ونشر القواعد والفهارس قبل الإطلاق.
