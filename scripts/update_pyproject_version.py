import sys
import toml

if len(sys.argv) != 2:
    print("Usage: python update_pyproject_version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1]

data = toml.load("pyproject.toml")

if "tool" in data and "poetry" in data["tool"]:
    data["tool"]["poetry"]["version"] = new_version
else:
    print("Error: version field not found in pyproject.toml")
    sys.exit(1)

with open("pyproject.toml", "w") as f:
    toml.dump(data, f)

print(f"Updated pyproject.toml to version {new_version}")
