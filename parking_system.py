"""Campus Parking Permit Manager.

Issues permits for vehicles in zones A to C, revokes them, checks for
expired permits and flags vehicles that should not be parked in a zone.
"""
import json
import secrets
from datetime import datetime, timedelta

ZONES = ("A", "B", "C")
DATE_FORMAT = "%Y-%m-%d"
VALIDITY_DAYS = 180


def normalize_plate(vehicle_plate):
    """Return the plate stripped and upper-cased, or raise ValueError."""
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        raise ValueError("Vehicle plate must be a non-empty string")
    return vehicle_plate.strip().upper()


def generate_permit_number(permits):
    """Return a permit number that has not been issued yet."""
    issued = {record.get("permit") for record in permits.values()}
    while True:
        number = "P" + str(10000 + secrets.randbelow(90000))
        if number not in issued:
            return number


def register_permit(permits, vehicle_plate, zone_id, zone_records=None):
    """Issue a permit and return its number.

    Raises ValueError if the plate or the zone is invalid.
    """
    plate = normalize_plate(vehicle_plate)
    if zone_id not in ZONES:
        raise ValueError(f"Invalid zone: {zone_id!r}")
    if zone_records is None:
        zone_records = []
    permit_no = generate_permit_number(permits)
    expiry = datetime.now() + timedelta(days=VALIDITY_DAYS)
    permits[plate] = {
        "zone": zone_id,
        "permit": permit_no,
        "expiry": expiry.strftime(DATE_FORMAT),
    }
    zone_records.append((plate, zone_id))
    return permit_no


def revoke_permit(permits, vehicle_plate):
    """Remove a permit. Return True if one existed, otherwise False."""
    if not isinstance(vehicle_plate, str):
        return False
    return permits.pop(vehicle_plate.strip().upper(), None) is not None


def is_expired(permits, vehicle_plate):
    """Return True if the plate's permit is expired or unreadable."""
    permit = permits.get(vehicle_plate)
    if permit is None:
        return False
    try:
        expiry = datetime.strptime(permit["expiry"], DATE_FORMAT)
    except (KeyError, ValueError):
        return True
    return expiry < datetime.now()


def scan_zone(permits, zone_id, plates_seen):
    """Return the plates that should not be parked in the given zone."""
    flagged = []
    for plate in plates_seen:
        key = plate.strip().upper()
        permit = permits.get(key)
        if (permit is None or permit["zone"] != zone_id
                or is_expired(permits, key)):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permits from a JSON file; return {} if missing or invalid."""
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Warning: {file} is not valid JSON; starting empty.")
        return {}
    return data if isinstance(data, dict) else {}


def save_permit_database(permits, file="permits.json"):
    """Write the permits to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(permits, handle, indent=2)


def set_expiry(permits, vehicle_plate, date_text):
    """Set a permit's expiry date (YYYY-MM-DD). Raises on bad input."""
    plate = normalize_plate(vehicle_plate)
    if plate not in permits:
        raise KeyError(f"No permit for {plate}")
    datetime.strptime(date_text, DATE_FORMAT)
    permits[plate]["expiry"] = date_text


def main():
    """Run the demo."""
    permits = load_permit_database()
    register_permit(permits, "KA01AB1234", "A")
    for plate, zone in (("KA05XY9999", "Z"), ("", "B"), (None, "C")):
        try:
            register_permit(permits, plate, zone)
        except ValueError as error:
            print("Rejected:", error)
    set_expiry(permits, "KA01AB1234", "2020-01-01")
    revoke_permit(permits, "MH12ZZ0000")
    print("Flagged in zone A:",
          scan_zone(permits, "A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]))
    plate = input("Plate to revoke (Enter to skip): ").strip()
    if plate:
        if revoke_permit(permits, plate):
            print("Revoked:", plate.upper())
        else:
            print("No permit found for:", plate.upper())
    save_permit_database(permits)
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
