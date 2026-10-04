---
name: Android and Firebase toolchains
description: Java version and project-ID requirements for building this Android app and testing its Firebase rules locally.
---

Use Java 17 for Android Gradle builds. Firebase CLI emulator tests require Java 21 or newer. For Storage rules that read Firestore documents, make the rules-test `projectId` match the Firebase Emulator CLI `--project` ID.

**Why:** A newer JDK triggered Android's `jlink` module conversion failure in this environment, while Firebase CLI rejected Java versions below 21. Storage permission checks also failed when the test project ID differed from the emulator project.

**How to apply:** Set `JAVA_HOME` to JDK 17 for APK builds. Install or select JDK 21+ only for Firebase emulator tests, and keep both emulator project IDs identical.