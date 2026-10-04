# FINAL AUDIT - Wasalny Tuktuk

تاريخ المراجعة: 2026-10-02

> ملاحظة تحديث: الأقسام التاريخية أدناه تصف حالة ما قبل تنظيف workflows. الحالة الحالية يحكمها `.github/workflows/build.yml` ودليل [إعداد بناء الإصدار](README_GITHUB_APK_BUILD.md)؛ تشغيلات Actions القديمة ليست تحققًا من workflow الحالي.

## النطاق والحدود

راجعت ملفات Android/Kotlin وCompose وNavigation، تسجيل الدخول والأدوار، تسجيل السائق، الخريطة والرحلات، مستودع Firebase، خدمات الموقع والإشعارات، Cloud Functions، Firestore/Storage Rules والفهارس، إعدادات Gradle وManifest وFirebase، GitHub Actions، والوثائق ذات الصلة. راجعت التدفقات ساكنًا من الواجهة حتى طبقة Firebase، وبُني APK على GitHub Actions؛ لم أختبر الرحلات على جهاز أو Firebase حي.

## الملفات المعدلة في هذه الجولة

1. `app/src/main/java/com/wasalny/sidisalem/MainActivity.kt`
2. `app/src/main/java/com/wasalny/sidisalem/AuthScreens.kt`
3. `app/src/main/java/com/wasalny/sidisalem/FirebaseRidesRepository.kt`
# FINAL AUDIT - تدقيق ربط Firebase وGitHub

تاريخ التدقيق: 2026-10-02

## النتيجة المختصرة

المستودع مضبوط حاليًا على مشروع Firebase `wasalny-app-f5dbb` في `.firebaserc`، ومعرّف المشروع نفسه موجود في إعداد Android. لا يلزم إنشاء مشروع Firebase جديد لمجرد استخدام حساب GitHub جديد؛ استخدم المشروع الحالي إذا كان الحساب/الفريق الجديد يملك صلاحية Firebase عليه. تعذّر إثبات ذلك من هذه البيئة لأن Firebase CLI غير مسجل الدخول.

## الملفات وفحصها

| الملف | الحالة | الملاحظة |
|---|---|---|
| `.github/workflows/build.yml` | الحالي | يبني APK وAAB موقّعين ويرفعهما كـ artifact. يتطلب أسرار التوقيع الأربعة؛ `GOOGLE_SERVICES_JSON` اختياري بصيغة Base64 مع fallback إلى ملف العميل المتتبع. |
| `.gitignore` | موجود | يستبعد keystore و`.pem` و`.p12`، لكنه لا يستبعد `.env` أو `serviceAccountKey.json` أو `app/google-services.json`. |
| `firebase.json` | موجود | يحدد Firestore rules/indexes وStorage rules وFunctions runtime `nodejs22`. |
| `.firebaserc` | موجود | المشروع الافتراضي `wasalny-app-f5dbb`. |
| `app/google-services.json` | موجود ومتتبع في Git | إعداد Android Client؛ projectId مطابق، ويتضمن الحزمة الحالية `com.wasalny.sidisalem` وتسجيلًا إضافيًا قديمًا `com.wasalny.app`. |
| `functions/.env` | غير موجود | البحث في Functions لم يجد استخدامًا لـ`process.env` أو Firebase runtime secrets حاليًا. |
| ملفات `serviceAccountKey.json` أو `.env` | غير موجودة | لم تظهر أسماؤها في ملفات المستودع أو أسماء الملفات بتاريخ Git الذي فُحص. |

لم تُطبع قيمة API key الموجودة ضمن إعداد Firebase العميل. هذا الملف لا يحتوي حقول Service Account أو مفتاح Admin SDK؛ مع ذلك فهو متتبع في مستودع عام، لذا قيّد Firebase/Google API key حسب التطبيق وواجهات API، ولا تعتبره مفتاح خادم.

## GitHub Actions Secrets

**المطلوب لبناء إصدار موقّع حاليًا:** أضف `ANDROID_KEYSTORE_BASE64` و`ANDROID_KEYSTORE_PASSWORD` و`ANDROID_KEY_ALIAS` و`ANDROID_KEY_PASSWORD` إلى Actions Secrets. يتوقف الـworkflow برسالة خطأ واضحة عند غياب أي منها. تفاصيل تجهيز keystore موجودة في [دليل بناء الإصدار](README_GITHUB_APK_BUILD.md).

- `GOOGLE_SERVICES_JSON` اختياري، ويجب أن يحتوي ملف Firebase Android كاملًا بصيغة Base64. يتحقق الـworkflow من JSON ومعرّف المشروع والحزمة، ويستخدم `app/google-services.json` المتتبع إذا لم يوجد السر.

**غير مستخدم حاليًا، فلا تنشئه لمجرد إعادة الربط:**

- `FIREBASE_TOKEN`: لا توجد إحالة إليه في workflows؛ لا حاجة إليه.
- `FIREBASE_SERVICE_ACCOUNT`: لا توجد إحالة إليه؛ لا يوجد Workflow لنشر Firebase تلقائيًا.
- `serviceAccountKey.json`: غير مطلوب ولا ينبغي رفعه إلى المستودع.
- لا توجد متغيرات Functions سرية حالية تستلزم `functions/.env`.

لا يمكن التحقق من وجود Actions Secrets في إعدادات GitHub من المستودع وحده. يجب إضافة أسرار التوقيع يدويًا قبل أول تشغيل ناجح؛ وجود ملف Firebase وحده لا يكفي لإصدار Release موقّع.

إذا كان شرطكم أن **أي إعداد عميل لا يبقى في Git**، فالـworkflow الحالي لا يحقق ذلك بالكامل: يلزم إضافة `GOOGLE_SERVICES_JSON` إلى GitHub Actions، وجعل كل من workflow البناء والتحقق يكتبان الملف من السر، ثم استبعاد الملف وإزالته من Git. لم أغيّر ذلك هنا لأن المطلوب تقرير فقط ولم تُقدّم قيمة سرية. لا تضع Base64 في YAML أو في الكود؛ أضفه من GitHub → Settings → Secrets and variables → Actions.

## المشروع القديم أم مشروع جديد؟

- الإعدادات الحالية تشير إلى `wasalny-app-f5dbb`، وهو مشروع Firebase المقصود في هذا المستودع.
- التوصية: أعد استخدامه إذا كان مملوكًا للفريق ويمكن منح الحساب الجديد صلاحيات Firebase المناسبة. انتقال GitHub account/repository لا يتطلب Firebase project جديدًا.
- لا تنشئ مشروعًا جديدًا إلا إذا فُقدت صلاحية المشروع الحالي أو تقرر ترحيل البيانات عمدًا. عندها يجب تحديث `.firebaserc` وGoogle Services config/Secret، وتفعيل Auth وFirestore وStorage وFCM وFunctions وScheduler، ثم نشر القواعد والفهارس والوظائف.
- Firebase CLI موجود لكنه غير مسجل الدخول، لذلك لم أستطع التحقق من وصول الحساب الحالي إلى المشروع. سجّل الدخول بالحساب المخول ثم تحقق باستخدام `firebase projects:list` وFirebase Console قبل أي نشر.

## عند إضافة نشر آلي مستقبلًا

لا يلزم إنشاء service account لهذا المشروع كي تعمل workflows الحالية. إذا أُضيف Workflow لنشر Cloud Functions والقواعد لاحقًا، فالخيار المفضل هو GitHub OIDC/Workload Identity Federation. إن استُخدم مفتاح Service Account اضطرارًا، خزّن JSON في GitHub Secret باسم متفق عليه مثل `FIREBASE_SERVICE_ACCOUNT`، وامنحه أقل صلاحيات لازمة، ولا تنشئ `serviceAccountKey.json` داخل المستودع.

أمر إنشاء حساب خدمة جديد عبر Google Cloud CLI، بعد اختيار المشروع ومنح الدور الأقل اللازم للنشر:

```bash
gcloud iam service-accounts create wasalny-ci-deploy \
	--project=wasalny-app-f5dbb \
	--display-name="Wasalny GitHub deploy"
```

لا تنشئ مفتاح JSON إلا عند الضرورة وبعد مراجعة سياسة المؤسسة. إن لزم ذلك، أضف المفتاح الناتج مباشرة إلى GitHub Secret عبر واجهة GitHub دون طباعته أو حفظه في Git أو في سجل الطرفية.

## Build وActions

التشغيلات التالية تاريخية وتخص SHA وملفات workflow السابقة؛ لا تثبت نجاح `Build Wasalny Release` الحالي. يلزم تشغيله بعد إضافة أسرار التوقيع والتحقق من APK وAAB الناتجين.

- [Build Wasalny APK](https://github.com/ahmed821989mo-arch/wasalny-app/actions/runs/36996529943)
- [Validate Wasalny project](https://github.com/ahmed821989mo-arch/wasalny-app/actions/runs/36996529887)

هذه التشغيلات تثبت بناء Android ونجاح Functions/TypeScript واختبارات القواعد في GitHub Actions؛ لا تثبت أن Firebase CLI للحساب الجديد مخول أو أن التطبيق متصل بمشروع Firebase حي.
