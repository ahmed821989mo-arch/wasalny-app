# بناء إصدار وصلني من GitHub Actions

## متطلبات GitHub

يحتاج Workflow إلى `GOOGLE_SERVICES_JSON` فقط إذا لم يكن الملف `app/google-services.json` موجودًا في المستودع. يمكن أن تكون قيمة السر محتوى الملف مباشرة أو بصيغة Base64.

يتحقق Workflow من أن إعداد Firebase يخص المشروع والحزمة الصحيحين قبل البناء.

## البناء والتنزيل

يبدأ **Build Wasalny Debug APK** عند push إلى `main` أو يدويًا من Actions. يبني APK تصحيح قابلًا للاختبار ويرفعه ضمن artifact باسم `wasalny-debug-apk` لمدة 14 يومًا. لا يحاول Workflow حاليًا إنشاء إصدار Release، لذلك لا يحتاج إلى أسرار توقيع.

يتطلب المشروع JDK 17 وGradle Wrapper 8.7، ويدعم Android 7 (API 24) فأحدث. APK التصحيح مخصص للاختبار وليس للتوزيع على Google Play؛ راجع [قائمة الإصدار](PRODUCTION_RELEASE_CHECKLIST_AR.md) قبل إعداد إصدار إنتاجي.
