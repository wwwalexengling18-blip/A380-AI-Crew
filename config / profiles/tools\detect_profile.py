import os
import re
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
PROFILES_DIR = CONFIG_DIR / "profiles"
CONFIG_DIR.mkdir(exist_ok=True)
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

RUNTIME_JSON = CONFIG_DIR / "runtime_detected.json"
ACTIVE_PROFILE_YAML = CONFIG_DIR / "active_profile.yaml"

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def find_usercfg_candidates():
    cands = []
    appdata = os.environ.get("APPDATA", "")
    localapp = os.environ.get("LOCALAPPDATA", "")

    # Häufige Orte (MS Store / Steam / 2020/2024 Varianten). Wir scannen breit.
    possible = [
        Path(appdata) / "Microsoft Flight Simulator" / "UserCfg.opt",
        Path(localapp) / "Packages" / "Microsoft.FlightSimulator_8wekyb3d8bbwe" / "LocalCache" / "UserCfg.opt",
        Path(localapp) / "Packages" / "Microsoft.FlightSimulator2024_8wekyb3d8bbwe" / "LocalCache" / "UserCfg.opt",
        Path(localapp) / "Packages" / "Microsoft.FlightSimulator2024" / "LocalCache" / "UserCfg.opt",
        Path(localapp) / "Packages" / "Microsoft.FlightSimulator" / "LocalCache" / "UserCfg.opt",
    ]

    for p in possible:
        if p.exists():
            cands.append(p)

    # Zusätzlich: in Packages nach *FlightSimulator* suchen
    pkg_root = Path(localapp) / "Packages"
    if pkg_root.exists():
        for p in pkg_root.glob("*FlightSimulator*"):
            uc = p / "LocalCache" / "UserCfg.opt"
            if uc.exists():
                cands.append(uc)

    # Duplikate raus
    uniq = []
    seen = set()
    for c in cands:
        s = str(c).lower()
        if s not in seen:
            seen.add(s)
            uniq.append(c)
    return uniq

def parse_installedpackagespath(usercfg_path: Path):
    try:
        text = usercfg_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    m = re.search(r'InstalledPackagesPath\s+"([^"]+)"', text)
    if m:
        return m.group(1)
    return None

def pick_best_usercfg(cands):
    if not cands:
        return None
    # Nimm die zuletzt geänderte
    return max(cands, key=lambda p: p.stat().st_mtime)

def detect_sim_version_from_paths(usercfg_path: Path | None):
    # Heuristik: Wenn der Pfad "2024" enthält, dann MSFS2024. Sonst unknown/2020.
    if not usercfg_path:
        return "unknown"
    s = str(usercfg_path).lower()
    if "2024" in s:
        return "msfs2024"
    if "flightsimulator_8wekyb3d8bbwe" in s or "microsoft flight simulator" in s:
        # kann 2020 sein – wir nennen es msfs2020, wenn kein 2024 Hinweis
        return "msfs2020"
    return "unknown"

def detect_community_folder(installedpackagespath: str | None):
    if not installedpackagespath:
        return None
    base = Path(installedpackagespath)
    # Bei MSFS ist Community meist direkt darunter
    comm = base / "Community"
    if comm.exists():
        return str(comm)
    # Fallback: manchmal ist InstalledPackagesPath schon "Packages"
    # dann liegt Community als sibling
    comm2 = base.parent / "Community"
    if comm2.exists():
        return str(comm2)
    return None

def folder_exists_case_insensitive(parent: Path, needle: str):
    if not parent or not parent.exists():
        return False
    needle = needle.lower()
    for p in parent.iterdir():
        if p.is_dir() and p.name.lower() == needle:
            return True
    return False

def find_folder_like(parent: Path, patterns: list[str]):
    if not parent or not parent.exists():
        return []
    hits = []
    for p in parent.iterdir():
        if not p.is_dir():
            continue
        name = p.name.lower()
        for pat in patterns:
            if pat in name:
                hits.append(p.name)
                break
    return sorted(list(set(hits)))

def write_yaml(path: Path, data: dict):
    # Minimal-YAML ohne extra libs
    lines = []
    for k, v in data.items():
        if isinstance(v, bool):
            vv = "true" if v else "false"
        elif v is None:
            vv = "null"
        else:
            vv = str(v)
        lines.append(f"{k}: {vv}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def load_profile_yaml(name: str) -> dict:
    prof = PROFILES_DIR / f"{name}.yaml"
    if not prof.exists():
        return {"name": "a380x_unknown"}
    # ultra simpel parser (key: value)
    out = {}
    for line in prof.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v in ("true", "false"):
            out[k] = (v == "true")
        elif v == "null":
            out[k] = None
        else:
            out[k] = v
    return out

def main():
    detected = {
        "timestamp": now(),
        "repo_root": str(ROOT),
        "usercfg_found": False,
        "usercfg_path": None,
        "installedpackagespath": None,
        "community_path": None,
        "sim_version_guess": "unknown",
        "found": {
            "fbw_a380x_folders": [],
            "gsx_folders": [],
            "wasim_folders": [],
            "simbridge_folders": [],
        }
    }

    cands = find_usercfg_candidates()
    best = pick_best_usercfg(cands)
    if best:
        detected["usercfg_found"] = True
        detected["usercfg_path"] = str(best)
        detected["sim_version_guess"] = detect_sim_version_from_paths(best)

        ipp = parse_installedpackagespath(best)
        detected["installedpackagespath"] = ipp
        comm = detect_community_folder(ipp)
        detected["community_path"] = comm

        if comm:
            comm_path = Path(comm)

            # FBW A380X (Foldernamen können variieren)
            detected["found"]["fbw_a380x_folders"] = find_folder_like(
                comm_path,
                ["flybywire", "a380", "aircraft-a380"]
            )

            # GSX Pro
            detected["found"]["gsx_folders"] = find_folder_like(
                comm_path,
                ["fsdreamteam-gsx", "gsx-pro", "gsx"]
            )

            # WASimCommander / WASimWASM / Tools
            detected["found"]["wasim_folders"] = find_folder_like(
                comm_path,
                ["wasim", "wasimcommander"]
            )

            # SimBridge (falls als Community package vorhanden)
            detected["found"]["simbridge_folders"] = find_folder_like(
                comm_path,
                ["simbridge", "bridge"]
            )

    # Profil-Auswahl
    has_a380 = len(detected["found"]["fbw_a380x_folders"]) > 0
    has_gsx = len(detected["found"]["gsx_folders"]) > 0
    sim = detected["sim_version_guess"]

    if sim == "msfs2024" and has_a380 and has_gsx:
        chosen = "a380x_msfs2024_gsx"
    elif sim == "msfs2024" and has_a380:
        chosen = "a380x_msfs2024_nogsx"
    else:
        chosen = "a380x_unknown"

    detected["chosen_profile"] = chosen

    # Runtime JSON schreiben
    RUNTIME_JSON.write_text(json.dumps(detected, indent=2, ensure_ascii=False), encoding="utf-8")

    # Active Profile YAML schreiben (Profil + detected hints)
    prof = load_profile_yaml(chosen)
    prof["detected_sim"] = sim
    prof["detected_has_a380x"] = has_a380
    prof["detected_has_gsx"] = has_gsx
    prof["detected_community_path"] = detected["community_path"]

    write_yaml(ACTIVE_PROFILE_YAML, prof)

    print("=== Detect Profile OK ===")
    print(f"runtime_detected.json: {RUNTIME_JSON}")
    print(f"active_profile.yaml:   {ACTIVE_PROFILE_YAML}")
    print(f"Chosen: {chosen}")
    print("")
    print("Quick Summary:")
    print(f"Sim: {sim}")
    print(f"Community: {detected['community_path']}")
    print(f"FBW A380X folders: {detected['found']['fbw_a380x_folders']}")
    print(f"GSX folders:       {detected['found']['gsx_folders']}")

if __name__ == "__main__":
    main()
