import boundaryData from "./data/sidi-salem-boundary.json";

type Ring = number[][];
type PolygonCoordinates = Ring[];

const polygons = boundaryData.coordinates as PolygonCoordinates[];

function isOnSegment(longitude: number, latitude: number, start: number[], end: number[]): boolean {
  const cross = (longitude - start[0]) * (end[1] - start[1])
    - (latitude - start[1]) * (end[0] - start[0]);
  if (Math.abs(cross) > 1e-9) return false;
  return longitude >= Math.min(start[0], end[0]) - 1e-9
    && longitude <= Math.max(start[0], end[0]) + 1e-9
    && latitude >= Math.min(start[1], end[1]) - 1e-9
    && latitude <= Math.max(start[1], end[1]) + 1e-9;
}

function containsRing(longitude: number, latitude: number, ring: Ring): boolean {
  let contains = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i];
    const [xj, yj] = ring[j];
    if (isOnSegment(longitude, latitude, ring[j], ring[i])) return true;
    const crossesLatitude = (yi > latitude) !== (yj > latitude);
    if (crossesLatitude && longitude < ((xj - xi) * (latitude - yi)) / (yj - yi) + xi) {
      contains = !contains;
    }
  }
  return contains;
}

export function isInsideSidiSalem(latitude: number, longitude: number): boolean {
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)
    || latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
    return false;
  }

  return polygons.some(polygon => containsRing(longitude, latitude, polygon[0])
    && !polygon.slice(1).some(hole => containsRing(longitude, latitude, hole)));
}
