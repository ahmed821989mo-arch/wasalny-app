# بناء إصدار وصلني من GitHub

راجع [دليل بناء APK وAAB](README_GITHUB_APK_BUILD.md) لإعداد Actions Secrets وتشغيل Workflow وتنزيل artifacts.

قبل الإطلاق، فعّل Phone Authentication وFirestore وStorage وCloud Functions، وانشر القواعد والفهارس، ثم اختبر الرحلات والإشعارات على أجهزة فعلية حسب [دليل إعداد Firebase](FIRESTORE_SETUP_AR.md) و[قائمة الإصدار](PRODUCTION_RELEASE_CHECKLIST_AR.md).

`app/google-services.json` إعداد عميل Firebase وليس مفتاح Admin SDK. يمكن إبقاؤه متتبعًا كما هو أو استبداله بسر اختياري Base64 باسم `GOOGLE_SERVICES_JSON`. قيّد API key من Google Cloud، ولا تخزن مفاتيح خدمة أو keystore في المستودع.
