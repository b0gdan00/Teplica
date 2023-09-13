import subprocess

file_path = '/dev/ttyUSB0'
desired_permissions = 0o777

def change_permissions():
    try: subprocess.check_call(['sudo', 'chmod', oct(desired_permissions)[2:], file_path])
    except Exception as e: print(f'[change_permissions] Помилка: {e}')

def reload_service():
    try: subprocess.check_call(['sudo', 'systemctl', 'restart', 'server.service',])
    except Exception as e: print(f'[reload_service] Помилка: {e}')

def git_update():
    try: subprocess.check_call(['git', "-C ~/Teplica", 'pull']); reload_service(); return "✅ Програма успішно оновлена"
    except Exception as e: print(f'[git_update] Помилка: {e}'); return "❌ Помилка оновлення"
    
 