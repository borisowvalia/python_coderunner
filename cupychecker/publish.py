#!/usr/bin/env python3
"""
Скрипт для быстрой публикации пакета cupychecker через twine
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import re
from datetime import datetime


class PackagePublisher:
    def __init__(self):
        self.package_dir = Path(__file__).parent
        self.dist_dir = self.package_dir / "dist"
        self.setup_cfg = self.package_dir / "setup.cfg"
        self.readme = self.package_dir / "README.md"
        
    def run_command(self, cmd, check=True, capture_output=False):
        """Выполнить команду с обработкой ошибок"""
        print(f"🔄 Выполняю: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd, 
                check=check, 
                capture_output=capture_output, 
                text=True,
                cwd=self.package_dir
            )
            if capture_output:
                return result.stdout.strip()
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка выполнения команды: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            sys.exit(1)
    
    def get_current_version(self):
        """Получить текущую версию из setup.cfg"""
        if not self.setup_cfg.exists():
            print("❌ Файл setup.cfg не найден")
            sys.exit(1)
            
        with open(self.setup_cfg, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r'version\s*=\s*([^\s\n]+)', content)
        if not match:
            print("❌ Не удалось найти версию в setup.cfg")
            sys.exit(1)
            
        return match.group(1)
    
    def update_version(self, new_version):
        """Обновить версию в setup.cfg"""
        print(f"📝 Обновляю версию до {new_version}")
        
        with open(self.setup_cfg, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Обновляем версию
        new_content = re.sub(
            r'version\s*=\s*[^\s\n]+',
            f'version = {new_version}',
            content
        )
        
        with open(self.setup_cfg, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ Версия обновлена до {new_version}")
    
    def increment_version(self, version_type='patch'):
        """Увеличить версию (patch, minor, major)"""
        current_version = self.get_current_version()
        print(f"📦 Текущая версия: {current_version}")
        
        try:
            major, minor, patch = map(int, current_version.split('.'))
        except ValueError:
            print("❌ Неверный формат версии. Ожидается X.Y.Z")
            sys.exit(1)
        
        if version_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif version_type == 'minor':
            minor += 1
            patch = 0
        elif version_type == 'patch':
            patch += 1
        else:
            print("❌ Неверный тип версии. Используйте: major, minor, patch")
            sys.exit(1)
        
        new_version = f"{major}.{minor}.{patch}"
        return new_version
    
    def clean_build(self):
        """Очистить предыдущие сборки"""
        print("🧹 Очищаю предыдущие сборки...")
        
        # Удаляем dist директорию
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            print("✅ Удалена директория dist/")
        
        # Удаляем egg-info
        egg_info_dirs = list(self.package_dir.glob("*.egg-info"))
        for egg_info in egg_info_dirs:
            shutil.rmtree(egg_info)
            print(f"✅ Удалена {egg_info.name}/")
        
        # Удаляем __pycache__
        for pycache in self.package_dir.rglob("__pycache__"):
            shutil.rmtree(pycache)
            print(f"✅ Удален {pycache}")
    
    def run_tests(self):
        """Запустить тесты перед публикацией"""
        print("🧪 Запускаю тесты...")
        
        tests_dir = self.package_dir.parent / "tests"
        if not tests_dir.exists():
            print("⚠️  Директория tests не найдена, пропускаю тесты")
            return
        
        # Запускаем тесты
        result = self.run_command(
            ["python3", "../tests/run_tests.py"],
            check=False,
            capture_output=True
        )
        
        if "✅ Все тесты прошли успешно!" in result:
            print("✅ Все тесты прошли успешно!")
        else:
            print("❌ Тесты не прошли!")
            print(result)
            sys.exit(1)
    
    def build_package(self):
        """Собрать пакет"""
        print("🔨 Собираю пакет...")
        
        # Устанавливаем build зависимости
        self.run_command([
            "pip3", "install", "--upgrade", 
            "setuptools", "wheel", "build"
        ])
        
        # Собираем пакет
        self.run_command(["python3", "-m", "build"])
        
        # Проверяем что файлы созданы
        if not self.dist_dir.exists():
            print("❌ Директория dist/ не создана")
            sys.exit(1)
        
        files = list(self.dist_dir.glob("*"))
        if not files:
            print("❌ Файлы пакета не созданы")
            sys.exit(1)
        
        print("✅ Пакет собран успешно!")
        for file in files:
            print(f"   📦 {file.name}")
    
    def check_package(self):
        """Проверить пакет с помощью twine"""
        print("🔍 Проверяю пакет...")
        
        # Устанавливаем twine если нужно
        self.run_command([
            "pip3", "install", "--upgrade", "twine"
        ])
        
        # Проверяем пакет
        self.run_command([
            "python3", "-m", "twine", "check", "dist/*"
        ])
        
        print("✅ Пакет прошел проверку!")
    
    def upload_to_testpypi(self):
        """Загрузить на TestPyPI"""
        print("🚀 Загружаю на TestPyPI...")
        
        self.run_command([
            "python3", "-m", "twine", "upload", 
            "--repository", "testpypi",
            "dist/*"
        ])
        
        print("✅ Пакет загружен на TestPyPI!")
        print("🔗 https://test.pypi.org/project/cupychecker/")
    
    def upload_to_pypi(self):
        """Загрузить на PyPI"""
        print("🚀 Загружаю на PyPI...")
        
        self.run_command([
            "python3", "-m", "twine", "upload", 
            "dist/*"
        ])
        
        print("✅ Пакет загружен на PyPI!")
        print("🔗 https://pypi.org/project/cupychecker/")
    
    def create_git_tag(self, version):
        """Создать git тег для версии"""
        print(f"🏷️  Создаю git тег v{version}...")
        
        try:
            # Проверяем что мы в git репозитории
            self.run_command(["git", "status"], capture_output=True)
            
            # Добавляем изменения
            self.run_command(["git", "add", "."])
            
            # Коммитим изменения
            self.run_command([
                "git", "commit", 
                "-m", f"Release version {version}"
            ])
            
            # Создаем тег
            self.run_command([
                "git", "tag", 
                "-a", f"v{version}", 
                "-m", f"Release version {version}"
            ])
            
            print(f"✅ Git тег v{version} создан!")
            
        except subprocess.CalledProcessError:
            print("⚠️  Не удалось создать git тег (возможно, не git репозиторий)")
    
    def publish(self, version_type='patch', test_only=False, skip_tests=False, 
                skip_git=False, version=None):
        """Основная функция публикации"""
        
        print("🚀 Начинаю публикацию пакета cupychecker")
        print("=" * 50)
        
        # Определяем версию
        if version:
            new_version = version
        else:
            new_version = self.increment_version(version_type)
        
        print(f"📦 Новая версия: {new_version}")
        
        # Обновляем версию
        self.update_version(new_version)
        
        # Запускаем тесты
        if not skip_tests:
            self.run_tests()
        else:
            print("⚠️  Пропускаю тесты (--skip-tests)")
        
        # Очищаем предыдущие сборки
        self.clean_build()
        
        # Собираем пакет
        self.build_package()
        
        # Проверяем пакет
        self.check_package()
        
        # Создаем git тег
        if not skip_git:
            self.create_git_tag(new_version)
        else:
            print("⚠️  Пропускаю создание git тега (--skip-git)")
        
        # Загружаем пакет
        if test_only:
            self.upload_to_testpypi()
        else:
            self.upload_to_pypi()
        
        print("\n🎉 Публикация завершена успешно!")
        print(f"📦 Версия: {new_version}")
        if test_only:
            print("🔗 TestPyPI: https://test.pypi.org/project/cupychecker/")
        else:
            print("🔗 PyPI: https://pypi.org/project/cupychecker/")


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для публикации пакета cupychecker"
    )
    
    parser.add_argument(
        '--version-type', 
        choices=['major', 'minor', 'patch'], 
        default='patch',
        help='Тип увеличения версии (по умолчанию: patch)'
    )
    
    parser.add_argument(
        '--version',
        help='Конкретная версия (например: 1.2.3)'
    )
    
    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Загрузить только на TestPyPI'
    )
    
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Пропустить тесты'
    )
    
    parser.add_argument(
        '--skip-git',
        action='store_true',
        help='Пропустить создание git тега'
    )
    
    parser.add_argument(
        '--clean-only',
        action='store_true',
        help='Только очистить предыдущие сборки'
    )
    
    parser.add_argument(
        '--build-only',
        action='store_true',
        help='Только собрать пакет'
    )
    
    args = parser.parse_args()
    
    publisher = PackagePublisher()
    
    if args.clean_only:
        publisher.clean_build()
        print("✅ Очистка завершена!")
        return
    
    if args.build_only:
        publisher.clean_build()
        publisher.build_package()
        publisher.check_package()
        print("✅ Сборка завершена!")
        return
    
    publisher.publish(
        version_type=args.version_type,
        test_only=args.test_only,
        skip_tests=args.skip_tests,
        skip_git=args.skip_git,
        version=args.version
    )


if __name__ == "__main__":
    main()
