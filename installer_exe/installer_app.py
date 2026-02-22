import os
import sys
import shutil
import time
from pathlib import Path

from colorama import init, Fore, Style

init(autoreset=True)

APP_NAME = "A380 AI Installer (MSFS2024 + FBW A380X)"
LOG_DIR_NAME = "logs"

def exe_dir() -> Path:
    # PyInstaller: sys._MEIPASS für bundled data, aber working dir ist exe-ort
    return Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent)).resolve()

def run_dir() -> Path:
    # Ort der EXE (wo user sie startet)
    return Path(sys.argv[0]).resolve().parent

def log_path() -> Path:
    d = run_dir() / LOG_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    return d / f"installer_{ts}.log"

def log(msg: str, lp: Path):
    lp.write_text(lp.read_text(encoding="utf-8") + msg + "\n" if lp.exists() else msg + "\n", encoding="utf-8")

def banner():
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + APP_NAME)
    print(Fore.CYAN + "=" * 70 + Style.RESET_ALL)

def find_usercfg() -> Path | None:
    # Steam/Standard in deinem Fall:
    p = Path(os.environ.get("APPDATA", "")) / "Microsoft Flight Simulator 2024" / "UserCfg.opt"
    if p.exists():
        return p
    return None

def parse_installed_packages_path(usercfg: Path) -> Path | None:
    txt = usercfg.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in txt:
        line = line.strip()
        if line.lower().startswith("installedpackagespath"):
            # InstalledPackagesPath "C:\...\Packages"
            parts = line.split('"')
            if len(parts) >= 2:
                return Path(parts[1])
    return None

def ensure_community_path(packages_path: Path) -> Path:
    return packages_path / "Community"

def copy_tree(src: Path, dst: Path):
    if dst.exists():
        # vorsichtig: existing behalten, aber überschreiben
        for root, dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            (dst / rel).mkdir(parents=True, exist_ok=True)
            for f in files:
                s = Path(root) / f
                d = dst / rel / f
                shutil.copy2(s, d)
    else:
        shutil.copytree(src, dst)

def verify_wasim_module(module_dir: Path) -> tuple[bool, str]:
    manifest = module_dir / "manifest.json"
    layout = module_dir / "layout.json"
    if not module_dir.exists():
        return False, "Ordner fehlt"
    if not manifest.exists():
        return False, "manifest.json fehlt"
    if not layout.exists():
        return False, "layout.json fehlt"
    return True, "OK"

def main():
    banner()
    lp = log_path()
    log(f"{APP_NAME} gestartet", lp)

    print(Fore.YELLOW + f"Log: {lp}")

    usercfg = find_usercfg()
    if not usercfg:
        msg = "UserCfg.opt nicht gefunden. Erwartet: %APPDATA%\\Microsoft Flight Simulator 2024\\UserCfg.opt"
        print(Fore.RED + msg)
        log(msg, lp)
        input("ENTER zum Beenden...")
        return

    log(f"UserCfg.opt: {usercfg}", lp)
    packages_path = parse_installed_packages_path(usercfg)
    if not packages_path:
        msg = "InstalledPackagesPath konnte nicht gelesen werden (UserCfg.opt)."
        print(Fore.RED + msg)
        log(msg, lp)
        input("ENTER zum Beenden...")
        return

    community = ensure_community_path(packages_path)
    log(f"InstalledPackagesPath: {packages_path}", lp)
    log(f"Community: {community}", lp)
    print(Fore.GREEN + f"Community erkannt: {community}")

    # Payload: wasimcommander-module
    payload_root = exe_dir() / "payload"
    src_mod = payload_root / "wasimcommander-module"
    dst_mod = community / "wasimcommander-module"

    if src_mod.exists():
        print(Fore.CYAN + "Installiere wasimcommander-module in Community ...")
        log("Kopiere wasimcommander-module ...", lp)
        community.mkdir(parents=True, exist_ok=True)
        copy_tree(src_mod, dst_mod)

        ok, reason = verify_wasim_module(dst_mod)
        if ok:
            print(Fore.GREEN + f"✅ wasimcommander-module installiert: {dst_mod}")
            log(f"wasimcommander-module OK: {dst_mod}", lp)
        else:
            print(Fore.RED + f"❌ wasimcommander-module fehlerhaft: {reason}")
            log(f"wasimcommander-module FEHLER: {reason}", lp)
    else:
        msg = f"Payload fehlt: {src_mod} (EXE enthält kein wasimcommander-module). Übersprungen."
        print(Fore.YELLOW + msg)
        log(msg, lp)

    # Check DLLs bundled (optional)
    libdir = exe_dir() / "lib"
    dll1 = libdir / "WASimCommander.WASimClient.dll"
    dll2 = libdir / "Ijwhost.dll"
    print(Fore.CYAN + "Prüfe WASimCommander Client DLLs (für Scripts)...")
    for d in [dll1, dll2]:
        if d.exists():
            print(Fore.GREEN + f"✅ gefunden: {d.name}")
            log(f"DLL OK: {d}", lp)
        else:
            print(Fore.RED + f"❌ fehlt: {d.name}")
            log(f"DLL FEHLT: {d}", lp)

    print()
    print(Fore.GREEN + "Fertig. Nächster Schritt:")
    print(Fore.GREEN + "1) MSFS2024 starten, FBW A380 laden")
    print(Fore.GREEN + "2) 60–120s warten (FBW Init)")
    print(Fore.GREEN + "3) Danach: WASimCommander Client UI → L:Local → List → A380X_ (oder A380)")
    log("Installer beendet.", lp)

    input("ENTER zum Schließen...")

if __name__ == "__main__":
    main()
