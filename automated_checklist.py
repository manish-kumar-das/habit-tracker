"""
Automated Pre-Build Checklist for Growthly
Verifies project is ready for executable build
"""
import os
import sys
import ast
import re
from pathlib import Path


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ChecklistVerifier:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def check(self, condition, message, severity='error'):
        """Record check result"""
        if condition:
            print(f"{Colors.GREEN}✅{Colors.END} {message}")
            self.passed += 1
            self.results.append(('PASS', message))
        else:
            if severity == 'warning':
                print(f"{Colors.YELLOW}⚠️ {Colors.END} {message}")
                self.warnings += 1
                self.results.append(('WARN', message))
            else:
                print(f"{Colors.RED}❌{Colors.END} {message}")
                self.failed += 1
                self.results.append(('FAIL', message))
    
    def section(self, title):
        """Print section header"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.END}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")


def check_project_structure(verifier):
    """Check file and folder structure"""
    verifier.section("📁 PROJECT STRUCTURE")
    
    # Required directories
    required_dirs = [
        'app',
        'app/views',
        'app/services',
        'app/themes',
        'app/models',
        'app/widgets',
        'app/db',
        'app/utils',
        'data',
        'data/profiles',
    ]
    
    for dir_path in required_dirs:
        verifier.check(
            os.path.isdir(dir_path),
            f"Directory exists: {dir_path}"
        )
    
    # Required files
    required_files = [
        'main.py',
        'app/__init__.py',
        'app/main.py',
        'app/themes/__init__.py',
        'app/views/__init__.py',
        'app/services/__init__.py',
        'app/models/__init__.py',
        'app/widgets/__init__.py',
        'app/db/__init__.py',
        'app/utils/__init__.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
    ]
    
    for file_path in required_files:
        verifier.check(
            os.path.isfile(file_path),
            f"File exists: {file_path}"
        )


def check_version_info(verifier):
    """Check version information"""
    verifier.section("📌 VERSION INFORMATION")
    
    # Check app/__init__.py
    try:
        with open('app/__init__.py', 'r') as f:
            content = f.read()
            has_version = '__version__' in content
            verifier.check(has_version, "Version in app/__init__.py")
            
            if has_version:
                match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
                if match:
                    version = match.group(1)
                    print(f"    Version: {version}")
    except FileNotFoundError:
        verifier.check(False, "app/__init__.py exists")
    
    # Check app/main.py
    try:
        with open('app/main.py', 'r') as f:
            content = f.read()
            has_version = '__version__' in content or 'VERSION' in content
            verifier.check(
                has_version,
                "Version in app/main.py",
                severity='warning'
            )
    except FileNotFoundError:
        verifier.check(False, "app/main.py exists")


def check_imports(verifier):
    """Check for import issues"""
    verifier.section("📦 IMPORT VERIFICATION")
    
    # Test critical imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
    
    imports_to_test = {
        'Theme system': 'app.themes',
        'Theme manager': 'app.themes.manager',
        'Views': 'app.views',
        'Services': 'app.services',
        'Models': 'app.models',
        'Widgets': 'app.widgets',
        'Database': 'app.db',
        'Utils': 'app.utils',
    }
    
    for name, module_path in imports_to_test.items():
        try:
            __import__(module_path)
            verifier.check(True, f"Import {name}: {module_path}")
        except Exception as e:
            verifier.check(False, f"Import {name}: {module_path} - {str(e)}")


def check_syntax_errors(verifier):
    """Check Python files for syntax errors"""
    verifier.section("🔍 SYNTAX VERIFICATION")
    
    python_files = []
    for root, dirs, files in os.walk('app'):
        # Skip __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = 0
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                ast.parse(code)
        except SyntaxError as e:
            verifier.check(False, f"Syntax error in {file_path}: {e}")
            syntax_errors += 1
    
    verifier.check(
        syntax_errors == 0,
        f"All {len(python_files)} Python files have valid syntax"
    )


def check_debug_code(verifier):
    """Check for leftover debug code"""
    verifier.section("🐛 DEBUG CODE CHECK")
    
    debug_patterns = [
        (r'\bprint\s*\(', 'print statements'),
        (r'\bpdb\.set_trace\(\)', 'pdb debugger'),
        (r'\bbreakpoint\(\)', 'breakpoint calls'),
        (r'#\s*TODO', 'TODO comments'),
        (r'#\s*FIXME', 'FIXME comments'),
        (r'#\s*HACK', 'HACK comments'),
    ]
    
    python_files = []
    for root, dirs, files in os.walk('app'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    issues_found = {}
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern, name in debug_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        if name not in issues_found:
                            issues_found[name] = []
                        issues_found[name].append(file_path)
        except Exception:
            pass
    
    if not issues_found:
        verifier.check(True, "No debug code found")
    else:
        for issue_type, files in issues_found.items():
            verifier.check(
                False,
                f"Found {issue_type} in {len(files)} file(s)",
                severity='warning'
            )
            for file in files[:3]:  # Show first 3
                print(f"    - {file}")


def check_documentation(verifier):
    """Check documentation files"""
    verifier.section("📚 DOCUMENTATION")
    
    # Check README.md content
    if os.path.exists('README.md'):
        with open('README.md', 'r') as f:
            content = f.read()
            required_sections = [
                ('# ', 'Has title'),
                ('## ', 'Has sections'),
                ('Installation', 'Has installation instructions'),
                ('Usage', 'Has usage instructions'),
            ]
            
            for pattern, description in required_sections:
                verifier.check(
                    pattern in content,
                    f"README.md: {description}",
                    severity='warning'
                )
    
    # Check other docs
    docs = {
        'LICENSE': 'License file',
        '.gitignore': 'Git ignore file',
        'CONTRIBUTING.md': 'Contribution guidelines',
        'CHANGELOG.md': 'Changelog',
    }
    
    for file, description in docs.items():
        severity = 'warning' if file in ['CONTRIBUTING.md', 'CHANGELOG.md'] else 'error'
        verifier.check(
            os.path.exists(file),
            f"{description} exists: {file}",
            severity=severity
        )


def check_requirements(verifier):
    """Check requirements.txt"""
    verifier.section("📦 DEPENDENCIES")
    
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            
            # Check for essential packages
            essential = ['PySide6', 'pyside6']
            has_essential = any(pkg.lower() in requirements.lower() for pkg in essential)
            
            verifier.check(
                has_essential,
                "requirements.txt includes PySide6"
            )
            
            verifier.check(
                len(requirements.strip()) > 0,
                "requirements.txt is not empty"
            )
            
            # Check for version pinning
            lines = [l.strip() for l in requirements.split('\n') if l.strip() and not l.startswith('#')]
            versioned = sum(1 for l in lines if '>=' in l or '==' in l or '~=' in l)
            
            verifier.check(
                versioned > 0,
                f"Some dependencies have versions ({versioned}/{len(lines)})",
                severity='warning'
            )
    else:
        verifier.check(False, "requirements.txt exists")


def check_hardcoded_paths(verifier):
    """Check for hardcoded absolute paths"""
    verifier.section("🛣️  PATH VERIFICATION")
    
    python_files = []
    for root, dirs, files in os.walk('app'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Patterns that might indicate absolute paths
    path_patterns = [
        (r'["\']C:\\', 'Windows absolute path'),
        (r'["\']D:\\', 'Windows absolute path'),
        (r'[\'"]/home/', 'Linux absolute path'),
        (r'[\'"]/Users/', 'macOS absolute path'),
    ]
    
    issues = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern, description in path_patterns:
                    if re.search(pattern, content):
                        issues.append(f"{file_path}: {description}")
        except Exception:
            pass
    
    if not issues:
        verifier.check(True, "No hardcoded absolute paths found")
    else:
        for issue in issues[:5]:  # Show first 5
            verifier.check(False, issue, severity='warning')


def check_build_files(verifier):
    """Check build script files"""
    verifier.section("🔨 BUILD SCRIPTS")
    
    build_files = {
        'build_all.py': 'Main build script',
        'test_before_build.py': 'Pre-build test script',
    }
    
    for file, description in build_files.items():
        verifier.check(
            os.path.exists(file),
            f"{description} exists: {file}",
            severity='warning'
        )


def generate_report(verifier):
    """Generate final report"""
    verifier.section("📊 SUMMARY REPORT")
    
    total = verifier.passed + verifier.failed + verifier.warnings
    
    print(f"Total checks: {total}")
    print(f"{Colors.GREEN}Passed: {verifier.passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {verifier.failed}{Colors.END}")
    print(f"{Colors.YELLOW}Warnings: {verifier.warnings}{Colors.END}")
    print()
    
    # Calculate percentage
    if total > 0:
        pass_rate = (verifier.passed / total) * 100
        print(f"Pass rate: {pass_rate:.1f}%")
        print()
    
    # Decision
    if verifier.failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL CRITICAL CHECKS PASSED{Colors.END}")
        print(f"{Colors.GREEN}✅ Project is ready to build!{Colors.END}")
        
        if verifier.warnings > 0:
            print(f"\n{Colors.YELLOW}Note: {verifier.warnings} warnings found.{Colors.END}")
            print(f"{Colors.YELLOW}These won't prevent building but should be addressed.{Colors.END}")
        
        print(f"\n{Colors.BOLD}Next step:{Colors.END}")
        print("  python build_all.py")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ CRITICAL ISSUES FOUND{Colors.END}")
        print(f"{Colors.RED}Please fix {verifier.failed} failed check(s) before building.{Colors.END}")
        return 1


def main():
    """Run all checks"""
    print(f"{Colors.BOLD}")
    print("=" * 60)
    print("  GROWTHLY - AUTOMATED PRE-BUILD CHECKLIST")
    print("=" * 60)
    print(f"{Colors.END}")
    
    verifier = ChecklistVerifier()
    
    # Run all verification sections
    check_project_structure(verifier)
    check_version_info(verifier)
    check_imports(verifier)
    check_syntax_errors(verifier)
    check_debug_code(verifier)
    check_documentation(verifier)
    check_requirements(verifier)
    check_hardcoded_paths(verifier)
    check_build_files(verifier)
    
    # Generate report
    return generate_report(verifier)


if __name__ == '__main__':
    sys.exit(main())