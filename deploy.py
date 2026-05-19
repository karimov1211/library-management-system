import subprocess
import sys

def run_cmd(args):
    print(f"Bajarilmoqda: {' '.join(args)}")
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Xato yuz berdi:\n{res.stderr}")
        return False
    if res.stdout:
        print(res.stdout)
    return True

print("=== Logistika Loyihasini GitHub'ga Yuklash ===")

# 1. Git add
if not run_cmd(["git", "add", "."]):
    print("Fayllarni Gitga qo'shib bo'lmadi.")
    sys.exit(1)

# 2. Git commit
commit_msg = "feat: transform library system to logistics system with React & FastAPI"
# Commit may fail if there are no changes, so we handle it gracefully
run_cmd(["git", "commit", "-m", commit_msg])

# 3. Git push
print("Kodni GitHub-ga yuklash (push) boshlanmoqda...")
if not run_cmd(["git", "push", "origin", "main"]):
    print("\n[!] Push bajarilmadi. Iltimos, GitHub remote manzilingiz to'g'ri sozlanganini tekshiring.")
    print("Maslahat: Agar remote ulanmagan bo'lsa, quyidagi buyruqni terminalda ishga tushiring:")
    print("git remote add origin https://github.com/karimov1211/library_system.git")
    sys.exit(1)

print("\n[+] Kodlar muvaffaqiyatli GitHub-ga yuklandi! Azure deploy boshlandi.")
