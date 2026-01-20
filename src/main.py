import psutil
import os
import sys
import time
import ctypes
import json
from colorama import init, Fore, Style

init(autoreset=True)

# ================== ADMIN CHECK ==================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1
    )
    sys.exit(0)

if not is_admin():
    print("🔐 Demande des permissions administrateur...")
    relaunch_as_admin()

# ================== JSON BLACKLIST ==================

if getattr(sys, 'frozen', False):
    DATA_PATH = os.path.join(os.path.dirname(sys.executable), "process_blacklist.json")
else:
    DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process_blacklist.json")

DEFAULT_BLACKLIST = [
    "system", "system idle process", "wininit.exe", "csrss.exe", "services.exe",
    "lsass.exe", "smss.exe", "svchost.exe", "explorer.exe", "winlogon.exe",
    "dwm.exe", "fontdrvhost.exe", "registry", "wudfhost.exe", "runtimebroker.exe",
    "memcompression", "audiodg.exe", "spoolsv.exe", "wmiprvse.exe",
    "migrationservice.exe", "armsvc.exe", "conhost.exe", "mbamservice.exe",
    "mpdefendercoreservice.exe"
]

if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        BLACKLIST_NAMES = set(json.load(f))
else:
    BLACKLIST_NAMES = set(DEFAULT_BLACKLIST)
    with open(DATA_PATH, "w") as f:
        json.dump(list(BLACKLIST_NAMES), f, indent=4)

def save_blacklist():
    with open(DATA_PATH, "w") as f:
        json.dump(list(BLACKLIST_NAMES), f, indent=4)

# ================== SCRIPT ==================

SELF_PID = os.getpid()

def is_user_process(proc):
    try:
        name = proc.name().lower()
        if proc.pid == SELF_PID:
            return False
        if name in BLACKLIST_NAMES:
            return False
        if proc.username() is None:
            return False
        if "system" in proc.username().lower():
            return False
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def confirm_close(name, pid):
    # PID système < 1000 affiché en rouge et non fermable
    if pid < 1000:
        print(Fore.RED + f"Système détecté : {name} (PID {pid})")
        return False
    while True:
        choice = input(f"Fermer {name} (PID {pid}) ? [o/n/b=blacklist] : ").lower()
        if choice == "o":
            return True
        elif choice == "n":
            return False
        elif choice == "b":
            BLACKLIST_NAMES.add(name.lower())
            save_blacklist()
            print(Fore.YELLOW + f"{name} ajouté à la blacklist ✅")
            return False

def close_process(proc):
    try:
        proc.terminate()
        proc.wait(timeout=3)
        print(f"✔ Fermé proprement : {proc.name()} (PID {proc.pid})")
        return True
    except psutil.TimeoutExpired:
        print(f"⚠ Ne répond pas, kill forcé : {proc.name()} (PID {proc.pid})")
        try:
            proc.kill()
            return True
        except psutil.AccessDenied:
            print("⛔ Accès refusé")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return False

def close_remaining_by_name(name):
    closed = 0
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.name().lower() == name.lower():
                proc.kill()
                closed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return closed

def main():
    print("\n=== Fermeture des applications (ADMIN) ===\n")

    closed_processes = []

    for proc in psutil.process_iter(["pid", "name", "username"]):
        if not is_user_process(proc):
            continue

        name = proc.name()
        pid = proc.pid

        if confirm_close(name, pid):
            if close_process(proc):
                closed_processes.append(name)

    print("\n=== Vérification des processus en arrière-plan ===\n")
    time.sleep(1)

    for name in set(closed_processes):
        count = close_remaining_by_name(name)
        if count > 0:
            print(f"🔁 {count} processus restant(s) de {name} fermés")

    print("\n=== Terminé ===")

if __name__ == "__main__":
    main()
