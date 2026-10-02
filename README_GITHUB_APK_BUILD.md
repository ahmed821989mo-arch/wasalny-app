# بناء إصدار وصلني من GitHub Actions

## متطلبات GitHub

من إعدادات المستودع، أضف Actions Secrets التالية قبل تشغيل Workflow:

- `ANDROID_KEYSTORE_BASE64`: ملف التوقيع بصيغة Base64؛ أنشئه محليًا باستخدام `base64 -w0 release-keystore.jks`.
- `ANDROID_KEYSTORE_PASSWORD`: كلمة مرور مخزن المفاتيح.
- `ANDROID_KEY_ALIAS`: الاسم المستعار للمفتاح.
- `ANDROID_KEY_PASSWORD`: كلمة مرور المفتاح.
- `GOOGLE_SERVICES_JSON` (اختياري): محتوى `app/google-services.json` بعد تحويله إلى Base64. عند غيابه يستخدم Workflow الملف المتتبع، ويتحقق من المشروع والحزمة قبل البناء.

لا ترفع ملف keystore أو `keystore.properties` إلى GitHub، ولا تطبع الأسرار في السجلات. احتفظ بنسخة احتياطية آمنة من keystore؛ فقدان مفتاح التطبيق يمنع تحديث التطبيق المنشور بالمفتاح نفسه.

## البناء والتنزيل

يبدأ **Build Wasalny Release** عند push إلى `main` أو يدويًا من Actions. يبني APK موقّعًا للتوزيع وAAB للنشر في Google Play، ثم يرفعهما ضمن artifact باسم `Wasalny-Release` لمدة 14 يومًا. يفشل البناء بوضوح إذا غابت أسرار التوقيع أو كان إعداد Firebase غير صالح.

يتطلب المشروع JDK 17 وGradle Wrapper 8.7، ويدعم Android 7 (API 24) فأحدث. بناء CI لا يعني أن التطبيق نُشر إلى Google Play أو أن خدمات Firebase فُعّلت؛ راجع [قائمة الإصدار](PRODUCTION_RELEASE_CHECKLIST_AR.md) واختبر التدفقات على أجهزة فعلية قبل الإطلاق.
