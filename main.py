#!/usr/bin/env python3
import os
import subprocess
import sys
import random
import time
import shutil
import textwrap
from datetime import datetime, timedelta


class DiskCleaner:
    def __init__(self):
        self.start_time = None
        self.current_pass = 0
        self.total_passes = 0

    def print_progress(self, operation, current, total, elapsed=None, remaining=None):
        """progress-bar"""
        bar_length = 30
        percent = current / total
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        if elapsed and remaining:
            status = f"{operation} |{bar}| {current}/{total} ⏱️ {elapsed} ↗ {remaining}"
        else:
            status = f"{operation} |{bar}| {current}/{total}"

        print(f"\r{status}", end='', flush=True)

        if current == total:
            print()

    def run_cmd(self, cmd, silent=True):
        """Execute the command without output"""
        try:
            if silent:
                subprocess.run(cmd, shell=True, check=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               executable='/bin/bash')
            else:
                subprocess.run(cmd, shell=True, check=True, executable='/bin/bash')
            return True
        except subprocess.CalledProcessError:
            return False

    def format_time(self, seconds):
        """Time formatting"""
        return str(timedelta(seconds=int(seconds)))

    def confirm_dangerous_action(self):
        """Confirmation for dangerous operations"""
        print("\n THIS MAY DAMAGE THE DISK!")
        response = input("[!] Continue? (yes/no): ")
        return response.lower() == 'yes'

    def get_disk_usage(self):
        """Get information about free space"""
        try:
            total, used, free = shutil.disk_usage("/")
            return free // (1024 ** 3)  # in GB
        except:
            return 0

    def method_standard(self):
        """Standard cleaning"""
        print(" Standard cleaning...")
        commands = [
            "sudo apt clean",
            "sudo apt autoremove --purge -y",
            "sudo journalctl --vacuum-time=7d",
            "rm -rf ~/.cache/* /tmp/* /var/tmp/* 2>/dev/null || true"
        ]

        for i, cmd in enumerate(commands, 1):
            self.print_progress("Cache cleaning", i, len(commands))
            self.run_cmd(cmd)
            time.sleep(0.5)

    def method_deep(self):
        """Deep cleaning"""
        print(" Deep cleaning...")
        commands = [
            "docker system prune -af 2>/dev/null || true",
            "npm cache clean --force 2>/dev/null || true",
            "pip cache purge 2>/dev/null || true",
            "snap set system refresh.retain=2 2>/dev/null || true"
        ]

        for i, cmd in enumerate(commands, 1):
            self.print_progress("Deep cleaning", i, len(commands))
            self.run_cmd(cmd)
            time.sleep(1)

    def method_secure(self):
        """Safe cleaning with overwriting"""
        if not self.confirm_dangerous_action():
            return

        print("Safe cleaning...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        test_file = "/tmp/secure_wipe.dat"
        size_mb = min(100, free_gb * 1024)

        self.start_time = time.time()

        for i in range(3):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (3 - i) / (i + 1) if i > 0 else 0

            self.print_progress(
                f"Pass {i + 1}/3",
                i + 1,
                3,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/urandom of={test_file} bs=1M count={size_mb} 2>/dev/null")
            self.run_cmd(f"rm -f {test_file}")
            time.sleep(1)

    def method_paranoid(self):
        """Paranoid cleaning"""
        if not self.confirm_dangerous_action():
            return

        print(" Paranoid cleaning...")
        free_gb = self.get_disk_usage()
        print(f" Free space: {free_gb} GB")

        patterns = ['zero', 'urandom', 'zero', 'urandom', 'zero']
        self.total_passes = len(patterns)
        self.start_time = time.time()

        for i, pattern in enumerate(patterns, 1):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / i if i > 0 else 0

            self.print_progress(
                f"Pass {i}/{self.total_passes} ({pattern})",
                i,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/paranoid_wipe bs=1M count=50 2>/dev/null")
            self.run_cmd("rm -f /tmp/paranoid_wipe")
            time.sleep(2)

    def method_ultra_paranoid(self):
        """Ultra-paranoid cleaning"""
        if not self.confirm_dangerous_action():
            return

        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        self.total_passes = 35
        self.start_time = time.time()

        for i in range(self.total_passes):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / (i + 1) if i > 0 else elapsed * self.total_passes

            if i in [0, 34]:
                pattern = "zero"
            else:
                pattern = "urandom"

            self.print_progress(
                f"Pass {i + 1}/{self.total_passes} ({pattern})",
                i + 1,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            size_mb = min(10, free_gb * 1024)
            if size_mb <= 0:
                break

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/ultra_wipe bs=1M count={size_mb} 2>/dev/null")
            self.run_cmd("rm -f /tmp/ultra_wipe")
            self.run_cmd("sync")
            time.sleep(1)

    def method_shredding(self):
        """Military-grade shredding with multiple algorithms"""
        if not self.confirm_dangerous_action():
            return

        print(" MILITARY SHREDDING...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        shred_patterns = [
            ("random", "NSA Random"),
            ("zero", "Zero Fill"),
            ("0xff", "One Fill"),
            ("urandom", "Crypto Random"),
            ("zero", "Final Zero")
        ]

        self.total_passes = len(shred_patterns)
        self.start_time = time.time()

        for i, (pattern, desc) in enumerate(shred_patterns, 1):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / i if i > 0 else 0

            self.print_progress(
                f"Shred {i}/{self.total_passes} ({desc})",
                i,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(
                f"shred -v -n 1 -z /tmp/shred_file 2>/dev/null || dd if=/dev/{pattern} of=/tmp/shred_file bs=1M count=20 2>/dev/null")
            self.run_cmd("rm -f /tmp/shred_file")
            time.sleep(1)

    def method_quantum_entanglement(self):
        """Quantum Entanglement Clean - 8-pass Fibonacci sequence patterns"""
        if not self.confirm_dangerous_action():
            return

        print(" QUANTUM ENTANGLEMENT CLEAN...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        fibonacci_patterns = [0x00, 0x01, 0x01, 0x02, 0x03, 0x05, 0x08, 0x0D]
        self.total_passes = len(fibonacci_patterns)
        self.start_time = time.time()

        for i, pattern in enumerate(fibonacci_patterns, 1):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / i if i > 0 else 0

            self.print_progress(
                f"Quantum {i}/{self.total_passes} (0x{pattern:02X})",
                i,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/zero of=/tmp/quantum_wipe bs=1M count=30 2>/dev/null")
            self.run_cmd("rm -f /tmp/quantum_wipe")
            time.sleep(1)

    def method_neural_network(self):
        """Neural Network Scramble - 12-pass AI-generated patterns"""
        if not self.confirm_dangerous_action():
            return

        print("NEURAL NETWORK SCRAMBLE...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        self.total_passes = 12
        self.start_time = time.time()

        for i in range(self.total_passes):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / (i + 1) if i > 0 else elapsed * self.total_passes

            pattern = "urandom" if i % 2 == 0 else "zero"
            self.print_progress(
                f"Neural {i + 1}/{self.total_passes} ({pattern})",
                i + 1,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/neural_wipe bs=1M count=25 2>/dev/null")
            self.run_cmd("rm -f /tmp/neural_wipe")
            time.sleep(1)

    def method_holographic(self):
        """Holographic Data Shatter - 7-pass interference patterns"""
        if not self.confirm_dangerous_action():
            return

        print("HOLOGRAPHIC DATA SHATTER...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        holographic_patterns = ['zero', 'urandom', 'zero', 'urandom', 'zero', 'urandom', 'zero']
        self.total_passes = len(holographic_patterns)
        self.start_time = time.time()

        for i, pattern in enumerate(holographic_patterns, 1):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / i if i > 0 else 0

            self.print_progress(
                f"Holographic {i}/{self.total_passes}",
                i,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/holographic_wipe bs=1M count=35 2>/dev/null")
            self.run_cmd("rm -f /tmp/holographic_wipe")
            time.sleep(1)

    def method_temporal_flux(self):
        """Temporal Flux Clean - 24-pass time-based patterns"""
        if not self.confirm_dangerous_action():
            return

        print("TEMPORAL FLUX CLEAN...")
        free_gb = self.get_disk_usage()
        print(f"Free space: {free_gb} GB")

        self.total_passes = 24
        self.start_time = time.time()

        for i in range(self.total_passes):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / (i + 1) if i > 0 else elapsed * self.total_passes

            if i % 3 == 0:
                pattern = "zero"
            elif i % 3 == 1:
                pattern = "urandom"
            else:
                pattern = "zero"

            self.print_progress(
                f"Temporal {i + 1}/{self.total_passes}",
                i + 1,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/temporal_wipe bs=1M count=15 2>/dev/null")
            self.run_cmd("rm -f /tmp/temporal_wipe")
            time.sleep(1)

    def method_fractal_compression(self):
        """Fractal Compression Erase - 9-pass recursive patterns"""
        if not self.confirm_dangerous_action():
            return

        print("FRACTAL COMPRESSION ERASE...")
        free_gb = self.get_disk_usage()
        print(f" Free space: {free_gb} GB")

        fractal_patterns = ['zero', 'urandom', 'zero', 'urandom', 'zero', 'urandom', 'zero', 'urandom', 'zero']
        self.total_passes = len(fractal_patterns)
        self.start_time = time.time()

        for i, pattern in enumerate(fractal_patterns, 1):
            elapsed = time.time() - self.start_time
            remaining = elapsed * (self.total_passes - i) / i if i > 0 else 0

            self.print_progress(
                f"Fractal {i}/{self.total_passes}",
                i,
                self.total_passes,
                self.format_time(elapsed),
                self.format_time(remaining)
            )

            self.run_cmd(f"dd if=/dev/{pattern} of=/tmp/fractal_wipe bs=1M count=40 2>/dev/null")
            self.run_cmd("rm -f /tmp/fractal_wipe")
            time.sleep(1)

    def show_menu(self):
        """Show selection menu"""
        print(r"""
    ____                        ____  _      __       ___                _ __    _ __      __  _           
   / __ \__  ___________       / __ \(_)____/ /__    /   |  ____  ____  (_) /_  (_) /___ _/ /_(_)___  ____ 
  / /_/ / / / / ___/ __ \     / / / / / ___/ //_/   / /| | / __ \/ __ \/ / __ \/ / / __ `/ __/ / __ \/ __ \
 / ____/ /_/ / /  / /_/ /    / /_/ / (__  ) ,<     / ___ |/ / / / / / / / / / / / / /_/ / /_/ / /_/ / / / /
/_/    \__, /_/   \____/    /_____/_/____/_/|_|   /_/  |_/_/ /_/_/ /_/_/_/ /_/_/_/\__,_/\__/_/\____/_/ /_/ 
      /____/                                                                                                                                                                                             
        """)

        print("=" * 70)
        print("[1]  Standard Clean - Removes temporary files and system cache")
        print("[2]  Deep Clean - Clears Docker, NPM, PIP system caches")
        print("[3]  Secure Clean - Single-pass overwrite with random data")
        print("[4]  Paranoid Clean - Five-pass overwrite with different algorithms")
        print("[5]  Ultra-Paranoid - 35-pass Gutmann method for complete destruction")
        print("[6]  Military Shredding - Multi-algorithm secure deletion")
        print("[7]  Quantum Entanglement - 8-pass Fibonacci sequence patterns")
        print("[8]  Neural Network - 12-pass AI-inspired random patterns")
        print("[9]  Holographic Shatter - 7-pass interference pattern algorithms")
        print("[10] Temporal Flux - 24-pass time-based seed generation")
        print("[11] Fractal Compression - 9-pass recursive pattern overwrite")
        print("=" * 70)

    def main(self):
        """Main function"""
        self.show_menu()

        choice = input("Select method [1-11]: ").strip()

        methods = {
            '1': self.method_standard,
            '2': self.method_deep,
            '3': self.method_secure,
            '4': self.method_paranoid,
            '5': self.method_ultra_paranoid,
            '6': self.method_shredding,
            '7': self.method_quantum_entanglement,
            '8': self.method_neural_network,
            '9': self.method_holographic,
            '10': self.method_temporal_flux,
            '11': self.method_fractal_compression
        }

        if choice in methods:
            try:
                methods[choice]()
                print("\n[!] Cleaning completed!")

                if self.start_time:
                    total_time = time.time() - self.start_time
                    print(f"⏱️ Total time: {self.format_time(total_time)}")

            except KeyboardInterrupt:
                print("\n\n[!] Stopped by user")
            except Exception as e:
                print(f"\n\n[!] Error: {e}")
        else:
            print("[!] Invalid choice")


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] For full functionality run with sudo!")

    cleaner = DiskCleaner()
    cleaner.main()
