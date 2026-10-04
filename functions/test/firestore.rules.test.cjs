const fs = require("node:fs");
const path = require("node:path");
const { after, before, beforeEach, test } = require("node:test");
const {
  assertFails,
  assertSucceeds,
  initializeTestEnvironment
} = require("@firebase/rules-unit-testing");
const {
  collection,
  doc,
  getDoc,
  getDocs,
  serverTimestamp,
  setDoc,
  updateDoc
} = require("firebase/firestore");
const { ref, uploadBytes } = require("firebase/storage");

const projectId = "demo-wasalny-rules";
let testEnvironment;

before(async () => {
  testEnvironment = await initializeTestEnvironment({
    projectId,
    firestore: {
      rules: fs.readFileSync(path.resolve(__dirname, "../../firestore.rules"), "utf8")
    },
    storage: {
      rules: fs.readFileSync(path.resolve(__dirname, "../../storage.rules"), "utf8")
    }
  });
});

after(async () => {
  await testEnvironment?.cleanup();
});

beforeEach(async () => {
  await testEnvironment.clearFirestore();
  await testEnvironment.withSecurityRulesDisabled(async context => {
    const db = context.firestore();
    await setDoc(doc(db, "admins/admin-1"), { role: "admin", active: true });
    await setDoc(doc(db, "users/passenger-1"), {
      uid: "passenger-1",
      role: "customer",
      name: "راكب",
      phone: "+201000000000",
      updatedAt: serverTimestamp()
    });
    await setDoc(doc(db, "drivers/driver-1"), {
      uid: "driver-1",
      displayName: "سائق",
      phone: "+201000000001",
      licenseType: "مرخص",
      vehicleType: "توك توك",
      approved: false,
      available: false,
      lat: 31.27133,
      lon: 30.786165,
      geohash: "swy",
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp()
    });
    await setDoc(doc(db, "rides/ride-1"), rideData("passenger-1"));
  });
});

function rideData(customerId, status = "searching") {
  return {
    customerId,
    customerName: "راكب",
    fromAddress: "نقطة البداية",
    toAddress: "الوجهة",
    fromLat: 31.27133,
    fromLon: 30.786165,
    toLat: 31.27233,
    toLon: 30.787165,
    distanceKm: 1,
    femaleMode: false,
    withLuggage: false,
    bookingType: "now",
    status,
    searchRadiusMeters: 500,
    searchStage: 0,
    invitedDriverIds: [],
    scheduledAt: null,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  };
}

function driverApplication(uid, vehicleType = "توك توك") {
  return {
    uid,
    displayName: "سائق جديد",
    phone: "+201000000002",
    licenseType: "مرخص",
    vehicleType,
    idCardImageUrl: "",
    vehicleImageUrl: "",
    profileImageUrl: "",
    idCardImagePath: `driverApplications/${uid}/id-card`,
    vehicleImagePath: `driverApplications/${uid}/vehicle`,
    profileImagePath: "",
    status: "pending",
    approved: false,
    available: false,
    lat: 31.27133,
    lon: 30.786165,
    geohash: "swy",
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  };
}

test("ordinary users cannot read or list admin records", async () => {
  const db = testEnvironment.authenticatedContext("passenger-1").firestore();
  await assertFails(getDoc(doc(db, "admins/admin-1")));
  await assertFails(getDocs(collection(db, "admins")));
});

test("users cannot promote themselves to admin", async () => {
  const db = testEnvironment.authenticatedContext("passenger-1").firestore();
  await assertFails(updateDoc(doc(db, "users/passenger-1"), {
    role: "admin",
    updatedAt: serverTimestamp()
  }));
});

test("passengers cannot approve drivers or read unrelated rides", async () => {
  const passengerDb = testEnvironment.authenticatedContext("passenger-1").firestore();
  const driverDb = testEnvironment.authenticatedContext("driver-1").firestore();
  const otherDriverDb = testEnvironment.authenticatedContext("driver-2").firestore();
  await assertFails(updateDoc(doc(passengerDb, "drivers/driver-1"), { approved: true }));
  await assertFails(updateDoc(doc(driverDb, "drivers/driver-1"), { approved: true }));
  await assertFails(getDoc(doc(otherDriverDb, "rides/ride-1")));
});

test("drivers cannot set themselves available with direct writes", async () => {
  await testEnvironment.withSecurityRulesDisabled(async context => {
    await updateDoc(doc(context.firestore(), "drivers/driver-1"), {
      approved: true,
      subscriptionExpiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000)
    });
  });
  const db = testEnvironment.authenticatedContext("driver-1").firestore();
  await assertFails(updateDoc(doc(db, "drivers/driver-1"), {
    available: true,
    updatedAt: serverTimestamp()
  }));
});

test("clients cannot accept offers by writing ride state directly", async () => {
  const db = testEnvironment.authenticatedContext("passenger-1").firestore();
  await assertFails(updateDoc(doc(db, "rides/ride-1"), {
    status: "accepted",
    selectedDriverId: "driver-1",
    selectedOfferId: "driver-1",
    selectedPrice: 50,
    updatedAt: serverTimestamp()
  }));
});

test("passengers cannot bypass server-side boundary checks when creating rides", async () => {
  const db = testEnvironment.authenticatedContext("passenger-1").firestore();
  await assertFails(setDoc(doc(db, "rides/ride-atomic"), rideData("passenger-1")));
});

test("clients cannot create driver application records directly", async () => {
  const db = testEnvironment.authenticatedContext("driver-new").firestore();
  const validApplication = driverApplication("driver-new");
  await assertFails(setDoc(doc(db, "drivers/driver-new"), {
    ...validApplication,
    idCardImagePath: ""
  }));
  await assertFails(setDoc(doc(db, "drivers/driver-new"), validApplication));
  const carDb = testEnvironment.authenticatedContext("driver-car").firestore();
  await assertFails(setDoc(doc(carDb, "drivers/driver-car"), driverApplication("driver-car", "Car")));
});

test("driver images can only upload to the signed-in UID path", async () => {
  const driverStorage = testEnvironment.authenticatedContext("driver-new").storage();
  const otherStorage = testEnvironment.authenticatedContext("driver-other").storage();
  const image = new Uint8Array([1, 2, 3]);
  await assertSucceeds(uploadBytes(ref(driverStorage, "driverApplications/driver-new/id-card"), image, {
    contentType: "image/png"
  }));
  await assertFails(uploadBytes(ref(otherStorage, "driverApplications/driver-new/id-card"), image, {
    contentType: "image/png"
  }));
});

test("driver image uploads enforce MIME type and size limits", async () => {
  const storage = testEnvironment.authenticatedContext("driver-new").storage();
  await assertFails(uploadBytes(ref(storage, "driverApplications/driver-new/profile"), new Uint8Array([1, 2, 3]), {
    contentType: "image/gif"
  }));
  await assertFails(uploadBytes(
    ref(storage, "driverApplications/driver-new/vehicle"),
    new Uint8Array(5 * 1024 * 1024 + 1),
    { contentType: "image/png" }
  ));
});

test("passengers cannot create rides with invalid coordinates or booking type", async () => {
  const db = testEnvironment.authenticatedContext("passenger-1").firestore();
  await assertFails(setDoc(doc(db, "rides/invalid-location"), {
    ...rideData("passenger-1"),
    fromLat: 120
  }));
  await assertFails(setDoc(doc(db, "rides/invalid-type"), {
    ...rideData("passenger-1"),
    bookingType: "car"
  }));
});
