const assert = require("node:assert/strict");
const { test } = require("node:test");
const { isInsideSidiSalem } = require("../lib/sidi-salem-boundary.js");

test("the city center and a remote northern part of Sidi Salem are in the service area", () => {
  assert.equal(isInsideSidiSalem(31.27133, 30.786165), true);
  assert.equal(isInsideSidiSalem(31.5, 30.7), true);
});

test("neighboring districts outside Sidi Salem are excluded", () => {
  assert.equal(isInsideSidiSalem(31.13, 30.646), false);
  assert.equal(isInsideSidiSalem(31.2, 30.8), false);
});

test("invalid coordinates and the invalid side of a border are rejected", () => {
  assert.equal(isInsideSidiSalem(Number.NaN, 30.786165), false);
  assert.equal(isInsideSidiSalem(31.27133, 181), false);
  assert.equal(isInsideSidiSalem(31.538, 30.8), false);
});
