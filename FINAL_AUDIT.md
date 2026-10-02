# FINAL AUDIT - Wasalny Tuktuk

تاريخ المراجعة: 2026-10-02

## النطاق والحدود

راجعت ملفات Android/Kotlin وCompose وNavigation، تسجيل الدخول والأدوار، تسجيل السائق، الخريطة والرحلات، مستودع Firebase، خدمات الموقع والإشعارات، Cloud Functions، Firestore/Storage Rules والفهارس، إعدادات Gradle وManifest وFirebase، GitHub Actions، والوثائق ذات الصلة. راجعت التدفقات ساكنًا من الواجهة حتى طبقة Firebase؛ لم تتوفر بيئة Android أو مشروع Firebase حي لاختبار الرحلات من جهاز إلى جهاز، لذلك لا أصف كل التدفقات بأنها مجرّبة إنتاجيًا.

## الملفات المعدلة في هذه الجولة

1. `app/src/main/java/com/wasalny/sidisalem/MainActivity.kt`
2. `app/src/main/java/com/wasalny/sidisalem/AuthScreens.kt`
3. `app/src/main/java/com/wasalny/sidisalem/FirebaseRidesRepository.kt`
4. `functions/src/index.ts`
5. `firestore.rules`
6. `functions/test/firestore.rules.test.cjs`
7. `BUILD_APK_ON_GITHUB_AR.md`
8. `FIRESTORE_SETUP_AR.md`
9. `FINAL_AUDIT.md`

لم تُنشأ نسخة مشروع أو Repository جديد، ولم تتغير هوية Firebase أو applicationId.

## المشاكل والإصلاحات

- كانت تفضيلات الدور والاسم والهاتف مفاتيح DataStore عامة مشتركة؛ قد يرث حساب Firebase آخر وضع السائق أو بيانات الحساب السابق. أصبحت المفاتيح مرتبطة بالـUID، وتُستعاد بيانات الحساب القديم من وثيقة `users/{uid}` الخاصة به. تعرض الواجهة حالة تحميل حتى يكتمل تحميل دور الحساب الحالي.
- كانت قواعد Firestore تسمح للسائق المعتمد بكتابة `available=true` بنفسه دون فحص رحلة نشطة. أصبح تغيير التوفر Callable خادميًا بمعاملة تتحقق من اعتماد السائق والاشتراك الساري وعدم وجود رحلة نشطة؛ كتابة العميل المباشرة لا تسمح إلا بالإيقاف.
- عند نجاح رفع مستند وفشل الرفع التالي، كانت المحاولة تعيد رفع المستند الناجح وتترك تقدم الرفع الفاشل ظاهرًا. تُحفظ حالة المستند الناجح منفردة ويُمسح تقدم المستند عند فشله، لتُعاد محاولة الملف المتعثر فقط.
- حالة إذن الموقع على الخريطة لم تكن تتزامن عند العودة من إعدادات Android. أضيف فحص عند استئناف الشاشة؛ ويظل الاختيار اليدوي متاحًا دون الإذن.
- تعليمات قديمة كانت تضع دخول المشرف في Account وتفترض إعداد Firebase مؤقتًا في CI. حُدّثت لتطابق `wasalny://admin` وإعداد Firebase العام المتتبع في المشروع.

## الأدوار والأمان

- لا يظهر Admin Login أو لوحة الإدارة في واجهة الراكب أو شاشة الحساب. فتح `wasalny://admin` لا يمنح الصلاحية بذاته؛ الدخول يتطلب Firebase Phone Auth وUID موجودًا في `admins/{uid}` بدور `admin` وحالة `active=true`. Cloud Functions والقواعد تعيدان فرض الصلاحيات خادميًا.
- لم أضف كودًا سريًا ثابتًا للمشرف داخل التطبيق؛ يمكن استخراج أي سر مضمن في APK. اعتماد UID الموثق عبر SMS وقائمة السماح الخادمية أقوى من رمز مشترك. إنشاء المشرف يتم من Firebase Console أو Admin SDK موثوق.
- قواعد Firestore تمنع العميل من ترقية دوره، إنشاء سجل سائق أو اعتماده، قبول العرض مباشرة، وقراءة بيانات الرحلات غير المرتبطة به. قواعد Storage تقيد مسارات المستندات ونوعها وحجمها.
- راجعت معاملات اختيار العرض والإلغاء وتقديم العرض، حالات الرحلة، حدود الدفعات، البحث الفوري التدريجي والحجز المجدول المنفصل، والتحقق الخادمي من الاشتراك. لم أجر اختبار تزامن حيًا على Firebase.

## الاختبارات والفحوص المنفذة

- `npm --prefix functions run build`: نجح.
- `npm --prefix functions run lint`: نجح.
- `npm --prefix functions run test:rules`: نجح، 10/10 على Firebase Emulator لـFirestore وStorage، بما فيها منع تفعيل السائق بكتابة مباشرة.
- `npm --prefix functions audit -- --audit-level=moderate`: صفر ثغرات.
- فحص Git history بحثًا عن أنماط مفاتيح خاصة ورموز اعتماد: لم يُعثر على تطابق؛ لم تُطبع قيم أسرار.
- فحص ملفات Kotlin المعدلة عبر تشخيصات المحرر: لا أخطاء معروضة.
- `git diff --check`: نجح قبل تحرير هذا التقرير؛ سيعاد ضمن الفحص النهائي قبل commit.
- `./gradlew :app:processDebugGoogleServices --no-daemon`: تعذر قبل مهمة Firebase لأن Gradle 8.7 لا يعمل مع إصدار Java الموجود `25.0.4.1`. Android SDK غير مضبوط (`ANDROID_HOME` غير موجود)، ولذلك لم يكتمل Kotlin compile أو APK أو Gradle checks.
- لم تُشغّل اختبارات Android على جهاز/محاكي، ولم يُنشر Firebase أو تُختبر Cloud Functions على مشروع حي.

## حالة التدفقات المطلوبة

- Passenger: مسار OTP والشروط والملف الشخصي والطلب والعروض والمتابعة والإلغاء والتقييم موجود ومراجع ساكنًا؛ رحلة فعلية كاملة غير متحققة هنا.
- Driver registration: أربع خطوات، TukTuk فقط، ملفات مطلوبة يتحقق منها الخادم قبل سجل pending، مع تقدم وإعادة محاولة جزئية؛ رفع فعلي بحساب Firebase غير متحقق هنا.
- Admin: منفصل عن واجهة الراكب ومحمي بالـUID والقواعد وFunctions؛ اختبار محاولة deep link من جهاز Android غير متاح.
- Map FROM/TO: اختيار النقطتين مستقل، مع النقر اليدوي وموقعي وإعادة اختيار كل نقطة؛ لا اختبار تفاعلي على جهاز.
- Immediate: Function تستخدم 500م ثم 1كم ثم 2كم ثم 5كم.
- Scheduled/School: ينتظر الموعد ثم يرسل للسائقين المتاحين والمؤهلين على دفعات، دون أنصاف أقطار البحث الفوري.
- العروض والقبول: تقديم العرض والتحقق من اختيار السائق مبنيان على Firestore transaction/Callable؛ لم يُجر اختبار ضغط تنافسي حي.
- Firebase Rules: اختبارات Emulator ناجحة للسيناريوهات الموجودة؛ هذا لا يغطي كل احتمالات التكامل الحي.

## إعداد وتشغيل

- Android: ثبّت JDK 21 وAndroid SDK 35، واضبط `ANDROID_HOME` أو `sdk.dir` في `local.properties`، ثم شغّل `./gradlew assembleDebug` أو `./gradlew check`.
- Cloud Functions: من `functions/` شغّل `npm ci` ثم `npm run build` و`npm run lint`.
- قواعد Firebase: من `functions/` شغّل `npm run test:rules`؛ يتطلب Java لتشغيل المحاكيات.
- إعداد Firebase: فعّل Phone Authentication وFirestore وStorage وFCM وCloud Functions وCloud Scheduler، وأنشئ Storage bucket وانشر الفهارس والقواعد.
- أضف `admins/{UID}` من Firebase Console أو Admin SDK موثوقًا، بالحقول `role: "admin"` و`active: true`.
- النشر بعد مراجعة المشروع المقصود: `firebase deploy --only firestore:rules,firestore:indexes,storage,functions`.
- بناء APK عبر GitHub Actions يستخدم JDK 21 وملف `app/google-services.json` المتتبع؛ يمكن لسر `GOOGLE_SERVICES_JSON` في workflow التحقق استبداله إذا لزم.
- توقيع Release يحتاج keystore وبياناته خارج Git، عبر إعداد محلي مستثنى أو GitHub Secrets.

## الخلاصة

نجح بناء وفحص Functions واختبار قواعد Firebase المحلي. لا يمكن اعتماد APK أو الادعاء بجاهزية إطلاق إنتاجي كاملة قبل إعادة Gradle باستخدام JDK 21 وAndroid SDK 35، واختبار التطبيق على جهازين، ونشر/اختبار Functions والقواعد على مشروع Firebase المقصود. لا يوجد «كود مشرف» ثابت داخل APK؛ صلاحية المشرف مرتبطة بالـUID الموثق والمدرج خادميًا.
