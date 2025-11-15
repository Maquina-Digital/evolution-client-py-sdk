import sys
from tomlkit import parse, dumps

if len(sys.argv) != 2:
    print("Usage: python update_pyproject_version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1]

with open("pyproject.toml", "r") as f:
    data = parse(f.read())

if "project" in data and "version" in data["project"]:
    data["project"]["version"] = new_version
else:
    print("Error: version field not found in pyproject.toml")
    sys.exit(1)

with open("pyproject.toml", "w") as f:
    f.write(dumps(data))

print(f"Updated pyproject.toml to version {new_version}")
