# Issues Found: parking_system.py

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Expired permit not flagged | Logic bug (High) | 25-30, 51-52 | setExpiry saves whatever text it is given. The demo sets 01/01/2020, but the code reads %Y-%m-%d, so parsing fails, the bare except returns False, and the permit counts as not expired. | Check the date with strptime when it is set, catch only KeyError/ValueError, and treat an unreadable date as expired. |
| Bad permits accepted | Logic bug (High) | 9-17 | An empty plate, None and zone "Z" all get registered, and ZONES is never used. None is saved as the string "null", so junk builds up in permits.json every run. | Validate the plate and the zone, and raise ValueError for bad input. |
| Bare except hides errors | Error handling (Medium) | 16, 22, 29, 43 | Pylint W0702 and Flake8 E722. Every error is swallowed, including real bugs. | Catch specific exceptions: KeyError, ValueError, FileNotFoundError, json.JSONDecodeError. |
| "Enter to skip" revokes a permit | Logic bug (Medium) | 63-64 | Pressing Enter passes "" to revoke_permit, which deletes the empty-plate permit instead of skipping. | Strip the input and only call revoke_permit when it is not empty. |
| Mutable default argument | Bug (Medium, Pylint W0102) | 9 | zone_records=[] is shared between all calls. | Default to None and create the list inside the function. |
| Files opened without with or encoding | Resource handling (Medium, R1732/W1514) | 42, 47 | The file may not get closed, and the encoding depends on the platform. | Use with open(file, encoding="utf-8") as handle. |
| try/except/pass in revoke | Error handling (Low, Bandit B110) | 22-23 | A failed revoke gives no feedback at all. | Use dict.pop(key, None) and return True or False. |
| Weak random for permit numbers | Security (Low, Bandit B311) | 11 | random.randint is not meant for security use and can give duplicate numbers. | Use secrets.randbelow and retry until the number is unused. |
| Global state | Design (Low, W0603) | 40 | global permits makes the functions depend on hidden state. | Pass permits in as a parameter and return the loaded dict. |
| Bad function name | Style (Low, C0103) | 51 | setExpiry is not snake_case. | Rename it to set_expiry. |
| Missing docstrings | Style (Low, C0114/C0116) | 1, 9, 19, 25, 32, 39, 46, 51, 54 | The module and functions have no documentation. | Add a docstring to the module and every function. |
| main() runs on import | Style (Low, Flake8 E305) | 68 | Importing the file runs the whole program. | Wrap the call in if __name__ == "__main__". |
| Formatting | Style (Low, E302/E501) | 9, 13, 19, 25, 27, 32, 39, 46, 51, 54, 62 | Missing blank lines and lines over 79 characters (line 13 is 110). | Two blank lines between functions, and wrap long lines. |

Pylint score: 6.32/10 before, 10.00/10 after. Line numbers are from the original starter file.
