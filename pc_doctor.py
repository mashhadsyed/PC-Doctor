import customtkinter as ctk
import platform
import shutil
import socket
import ctypes
import threading
import subprocess
import os
import re
from datetime import datetime

# PC Doctor - Simple PC Health & Troubleshooting Assistant

APP_NAME = "PC Doctor"
APP_VERSION = "0.3.0"

TOOLKIT_DIR = r"C:\PC-Health-Check-Toolkit"
ANALYZER_PATH = os.path.join(TOOLKIT_DIR, "ErrorLogAnalyzer.ps1")
HTML_REPORT = os.path.join(TOOLKIT_DIR, "ErrorAnalysisReport.html")
TEXT_REPORT = os.path.join(TOOLKIT_DIR, "ErrorAnalysisReport.txt")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F4F7FB"
NAVY = "#172B4D"
BLUE = "#2563EB"
GREEN = "#15803D"
ORANGE = "#B45309"
RED = "#B91C1C"
MUTED = "#64748B"


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def get_memory():
    try:
        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(status)

        if ctypes.windll.kernel32.GlobalMemoryStatusEx(
            ctypes.byref(status)
        ):
            total = status.ullTotalPhys / (1024 ** 3)
            available = status.ullAvailPhys / (1024 ** 3)
            used_percent = status.dwMemoryLoad
            return total, available, used_percent
    except Exception:
        pass

    return None, None, None


class PCDoctor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} | Simple PC Health Assistant")
        self.geometry("1050x720")
        self.minsize(850, 600)
        self.configure(fg_color=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.show_dashboard()

    # SIDEBAR

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=225,
            corner_radius=0,
            fg_color=NAVY
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="✚  PC Doctor",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="white"
        ).pack(padx=20, pady=(30, 5), anchor="w")

        ctk.CTkLabel(
            sidebar,
            text="Your simple PC assistant",
            text_color="#CBD5E1",
            font=ctk.CTkFont(size=12)
        ).pack(padx=22, pady=(0, 25), anchor="w")

        self.nav_button(
            sidebar, "⌂   Home", self.show_dashboard
        )
        self.nav_button(
            sidebar, "✓   Check my PC", self.run_health_check
        )
        self.nav_button(
            sidebar, "⌁   Internet help", self.show_internet_help
        )
        self.nav_button(
            sidebar, "⚠   Scan Windows Errors", self.scan_windows_errors
        )
        self.nav_button(
            sidebar, "✚   Understand & Fix Errors", self.show_error_guide
        )
        self.nav_button(
            sidebar, "▤   Reports", self.show_reports
        )

        ctk.CTkLabel(
            sidebar,
            text="Made by Mashhad",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="bottom", pady=(0, 5))

        ctk.CTkLabel(
            sidebar,
            text=f"Version {APP_VERSION}",
            text_color="#CBD5E1",
            font=ctk.CTkFont(size=11)
        ).pack(side="bottom", pady=(0, 18))

    def nav_button(self, parent, text, command):
        ctk.CTkButton(
            parent,
            text=text,
            command=command,
            anchor="w",
            height=43,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#294366",
            text_color="white",
            font=ctk.CTkFont(size=13)
        ).pack(fill="x", padx=12, pady=4)

    # MAIN AREA

    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )
        self.main.grid(
            row=0, column=1,
            sticky="nsew", padx=28, pady=24
        )
        self.main.grid_columnconfigure(0, weight=1)

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        self.main.grid_rowconfigure(3, weight=0)

    def heading(self, title, subtitle):
        ctk.CTkLabel(
            self.main,
            text=title,
            text_color=NAVY,
            font=ctk.CTkFont(size=29, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self.main,
            text=subtitle,
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            wraplength=730,
            justify="left"
        ).grid(row=1, column=0, sticky="w", pady=(0, 22))

    # HOME DASHBOARD

    def show_dashboard(self):
        self.clear_main()

        self.heading(
            "Hello! Let's check your PC.",
            "Simple checks, clear explanations. No technical "
            "knowledge required."
        )

        welcome = ctk.CTkFrame(
            self.main, fg_color="#E4EDFF", corner_radius=16
        )
        welcome.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        welcome.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            welcome,
            text="Your computer, made easier.",
            text_color=NAVY,
            font=ctk.CTkFont(size=21, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(22, 6))

        ctk.CTkLabel(
            welcome,
            text=(
                "Check storage, memory, internet connectivity, "
                "and common Windows event log errors."
            ),
            text_color=NAVY,
            font=ctk.CTkFont(size=14),
            wraplength=600,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 15))

        ctk.CTkButton(
            welcome,
            text="Check my PC  →",
            command=self.run_health_check,
            height=43,
            width=180,
            fg_color=BLUE,
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, sticky="w", padx=22, pady=(0, 12))

        ctk.CTkButton(
            welcome,
            text="Scan Windows Errors",
            command=self.scan_windows_errors,
            height=40,
            width=180,
            fg_color=NAVY
        ).grid(row=3, column=0, sticky="w", padx=22, pady=(0, 22))

        cards = ctk.CTkFrame(self.main, fg_color="transparent")
        cards.grid(row=3, column=0, sticky="ew")
        cards.grid_columnconfigure((0, 1), weight=1)

        self.info_card(
            cards, 0, 0, "STORAGE",
            "Check available space",
            "Find out if your drive is getting full."
        )
        self.info_card(
            cards, 0, 1, "MEMORY",
            "Check RAM usage",
            "See how much memory is currently in use."
        )
        self.info_card(
            cards, 1, 0, "INTERNET",
            "Test your connection",
            "Check basic connectivity and DNS lookup."
        )
        self.info_card(
            cards, 1, 1, "WINDOWS ERRORS",
            "Review event logs",
            "Scan recent Windows errors and warnings."
        )

        ctk.CTkLabel(
            self.main,
            text="Basic diagnostics only. Review guidance before making changes.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(row=4, column=0, sticky="w", pady=15)

    def info_card(self, parent, row, col, label, title, description):
        card = ctk.CTkFrame(
            parent, fg_color="white", corner_radius=12
        )
        card.grid(
            row=row, column=col,
            sticky="nsew", padx=6, pady=6
        )

        ctk.CTkLabel(
            card,
            text=label,
            text_color=BLUE,
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 5))

        ctk.CTkLabel(
            card,
            text=title,
            text_color=NAVY,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=16, pady=3)

        ctk.CTkLabel(
            card,
            text=description,
            text_color=MUTED,
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=16, pady=(3, 16))

    # PC HEALTH CHECK

    def run_health_check(self):
        self.clear_main()

        self.heading(
            "Your PC health check",
            "We're checking a few basic things. This may take a moment."
        )

        self.status_label = ctk.CTkLabel(
            self.main,
            text="Checking your computer...",
            text_color=BLUE,
            font=ctk.CTkFont(size=16)
        )
        self.status_label.grid(
            row=2, column=0, sticky="w", pady=10
        )

        self.results = ctk.CTkTextbox(
            self.main,
            height=340,
            corner_radius=12,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.results.grid(
            row=3, column=0, sticky="nsew", pady=10
        )
        self.results.insert("1.0", "Please wait while the checks run...")
        self.results.configure(state="disabled")
        self.main.grid_rowconfigure(3, weight=1)

        threading.Thread(
            target=self.collect_health_data,
            daemon=True
        ).start()

    def collect_health_data(self):
        lines = []
        issues = 0

        lines.append("YOUR PC")
        lines.append(
            f"Operating system: {platform.system()} {platform.release()}"
        )
        lines.append(f"Computer name: {platform.node()}")
        lines.append("")

        # Storage
        try:
            disk = shutil.disk_usage("C:\\")
            free_gb = disk.free / (1024 ** 3)
            total_gb = disk.total / (1024 ** 3)
            free_percent = disk.free / disk.total * 100

            lines.append("1. STORAGE")
            lines.append(
                f"Drive C: has {free_gb:.1f} GB free "
                f"out of {total_gb:.1f} GB."
            )

            if free_percent < 10:
                lines.append(
                    "Attention: storage is running low. "
                    "Review large files before deleting anything."
                )
                issues += 1
            else:
                lines.append(
                    "No low-storage warning from this basic check."
                )

            lines.append("")
        except Exception:
            lines.extend([
                "1. STORAGE",
                "We couldn't check the C: drive. "
                "Please review it in Windows Settings.",
                ""
            ])

        # Memory
        total, available, used = get_memory()
        lines.append("2. MEMORY")

        if used is not None:
            lines.append(
                f"Approximately {used}% of your RAM is currently in use."
            )
            lines.append(
                f"Available memory: {available:.1f} GB "
                f"of {total:.1f} GB."
            )

            if used >= 90:
                lines.append(
                    "Attention: memory use is high. Close apps "
                    "you recognise and aren't using."
                )
                issues += 1
            else:
                lines.append(
                    "No high-memory-use warning from this basic check."
                )
        else:
            lines.append("We couldn't read memory usage on this computer.")

        lines.append("")

        # Internet connection
        lines.append("3. INTERNET")

        try:
            with socket.create_connection(("1.1.1.1", 53), timeout=3):
                lines.append("A basic network connection test succeeded.")
        except OSError:
            lines.append(
                "The connection test did not succeed. "
                "Check Wi-Fi, cables and router status."
            )
            issues += 1

        try:
            socket.getaddrinfo("example.com", 443)
            lines.append("DNS lookup succeeded.")
        except OSError:
            lines.append(
                "DNS lookup failed. Check other devices before "
                "trying further troubleshooting."
            )
            issues += 1

        lines.extend([
            "",
            "IMPORTANT",
            "These are basic checks, not a complete diagnosis.",
            "A warning does not automatically mean something is broken.",
            "No files were deleted and no settings were changed.",
            "",
            f"Report generated: {datetime.now():%Y-%m-%d %H:%M:%S}"
        ])

        report = "\n".join(lines)
        self.after(0, lambda: self.display_results(report, issues))

    def display_results(self, report, issues):
        self.status_label.configure(
            text="Check complete. Review the results below.",
            text_color=GREEN if issues == 0 else ORANGE
        )

        self.results.configure(state="normal")
        self.results.delete("1.0", "end")
        self.results.insert("1.0", report)
        self.results.configure(state="disabled")

        ctk.CTkButton(
            self.main,
            text="← Back to home",
            command=self.show_dashboard,
            height=40
        ).grid(row=4, column=0, sticky="w", pady=10)

    # WINDOWS ERROR SCANNER

    def scan_windows_errors(self):
        self.clear_main()

        self.heading(
            "Windows Error Scanner",
            "Review recent Windows event log errors and warnings "
            "using your existing diagnostic script."
        )

        ctk.CTkLabel(
            self.main,
            text=(
                "This scan reads Windows event logs and creates reports. "
                "It does not intentionally change Windows settings."
            ),
            text_color=NAVY,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        ).grid(row=2, column=0, sticky="w", pady=(0, 15))

        self.scan_status = ctk.CTkLabel(
            self.main,
            text="Ready to scan.",
            text_color=BLUE,
            font=ctk.CTkFont(size=15)
        )
        self.scan_status.grid(
            row=3, column=0, sticky="w", pady=10
        )

        self.scan_button = ctk.CTkButton(
            self.main,
            text="Start Windows Error Scan",
            command=self.start_error_scan,
            height=44,
            width=240,
            fg_color=BLUE
        )
        self.scan_button.grid(
            row=4, column=0, sticky="w", pady=10
        )

        ctk.CTkButton(
            self.main,
            text="Open HTML report",
            command=self.open_html_report,
            height=40,
            width=200
        ).grid(row=5, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            self.main,
            text="Open text report",
            command=self.open_text_report,
            height=40,
            width=200
        ).grid(row=6, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            self.main,
            text="← Back to home",
            command=self.show_dashboard,
            height=40
        ).grid(row=7, column=0, sticky="w", pady=(15, 0))

    def start_error_scan(self):
        if not os.path.isfile(ANALYZER_PATH):
            self.scan_status.configure(
                text=f"Analyzer not found:\n{ANALYZER_PATH}",
                text_color=RED
            )
            return

        self.scan_button.configure(
            state="disabled",
            text="Scanning Windows logs..."
        )
        self.scan_status.configure(
            text="Scanning. Please wait...",
            text_color=BLUE
        )

        threading.Thread(
            target=self.run_error_scan,
            daemon=True
        ).start()

    def run_error_scan(self):
        try:
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy", "Bypass",
                    "-File", ANALYZER_PATH
                ],
                cwd=TOOLKIT_DIR,
                capture_output=True,
                text=True,
                timeout=180,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                )
            )

            if result.returncode == 0:
                message = (
                    "Scan finished. Check the HTML or text report below."
                )
                color = GREEN
            else:
                details = (
                    result.stderr.strip()
                    or result.stdout.strip()
                    or f"Exit code: {result.returncode}"
                )
                message = "The scan reported an issue:\n" + details[-1200:]
                color = RED

        except subprocess.TimeoutExpired:
            message = "The scan took too long and was stopped."
            color = RED
        except Exception as exc:
            message = f"Could not run the scanner:\n{exc}"
            color = RED

        self.after(
            0,
            lambda: self.finish_error_scan(message, color)
        )

    def finish_error_scan(self, message, color):
        self.scan_status.configure(
            text=message,
            text_color=color
        )
        self.scan_button.configure(
            state="normal",
            text="Start Windows Error Scan"
        )

    # REPORT OPENING

    def open_html_report(self):
        self.open_report(HTML_REPORT)

    def open_text_report(self):
        self.open_report(TEXT_REPORT)

    def open_report(self, path):
        if not os.path.isfile(path):
            self.show_message(
                "Report not found",
                "The report doesn't exist yet. Run the Windows "
                "Error Scan first."
            )
            return

        try:
            os.startfile(path)
        except Exception as exc:
            self.show_message(
                "Could not open report",
                str(exc)
            )

    def show_message(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("480x200")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=title,
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=NAVY
        ).pack(padx=20, pady=(20, 10))

        ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=420,
            justify="left"
        ).pack(padx=20, pady=5)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=15)

    # INTERNET HELP

    def show_internet_help(self):
        self.clear_main()

        self.heading(
            "Internet help",
            "Try these safe checks if websites aren't loading."
        )

        steps = [
            "1. Make sure Wi-Fi is turned on or the network cable is connected.",
            "2. Check whether the same problem occurs on another device.",
            "3. Restart your router if other devices also have problems.",
            "4. If only this PC has the issue, run the PC health check.",
            "5. If the problem continues, contact your internet provider or IT support."
        ]

        panel = ctk.CTkFrame(
            self.main, fg_color="white", corner_radius=12
        )
        panel.grid(row=2, column=0, sticky="ew")

        for step in steps:
            ctk.CTkLabel(
                panel,
                text=step,
                text_color=NAVY,
                font=ctk.CTkFont(size=14),
                wraplength=680,
                justify="left"
            ).pack(anchor="w", padx=20, pady=12)

        ctk.CTkButton(
            self.main,
            text="Test my connection",
            command=self.run_health_check,
            height=42
        ).grid(row=3, column=0, sticky="w", pady=20)

    # UNDERSTAND & FIX WINDOWS ERRORS

    def show_error_guide(self):
        self.clear_main()

        self.heading(
            "Understand & Fix My Errors",
            "Plain-English explanations and cautious next steps based on your latest Windows event report."
        )

        panel = ctk.CTkFrame(self.main, fg_color="white", corner_radius=12)
        panel.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        panel.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        text_box = ctk.CTkTextbox(
            panel,
            wrap="word",
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        text_box.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        panel.grid_rowconfigure(0, weight=1)

        report_exists = os.path.isfile(TEXT_REPORT)
        report_text = ""
        if report_exists:
            try:
                with open(TEXT_REPORT, "r", encoding="utf-8", errors="replace") as report_file:
                    report_text = report_file.read()
            except OSError as exc:
                report_text = ""
                text_box.insert(
                    "1.0",
                    "PC Doctor couldn't read the text report.\n\n"
                    f"Details: {exc}\n\n"
                    "Run Windows Error Scan again, then reopen this page."
                )
                text_box.configure(state="disabled")
                ctk.CTkButton(
                    self.main,
                    text="← Back to home",
                    command=self.show_dashboard,
                    height=40
                ).grid(row=3, column=0, sticky="w", pady=8)
                return

        if not report_text:
            text_box.insert(
                "1.0",
                "No readable Windows error report was found yet.\n\n"
                "1. Choose “Scan Windows Errors” from the left menu.\n"
                "2. Wait for the scan to finish.\n"
                "3. Return here to see explanations for detected events.\n\n"
                "This page provides guidance only. It does not automatically change Windows settings."
            )
            text_box.configure(state="disabled")
            ctk.CTkButton(
                self.main,
                text="Scan Windows Errors",
                command=self.scan_windows_errors,
                height=40
            ).grid(row=3, column=0, sticky="w", pady=8)
            ctk.CTkButton(
                self.main,
                text="← Back to home",
                command=self.show_dashboard,
                height=40
            ).grid(row=4, column=0, sticky="w", pady=8)
            return

        # Detect event IDs and provider names present in the latest text report.
        events = set()
        for match in re.finditer(
            r"Event ID:\s*(\d+)\s*\nSource:\s*([^\r\n]+)",
            report_text,
            flags=re.IGNORECASE
        ):
            events.add((match.group(1).strip(), match.group(2).strip()))

        # Also account for report summaries where the ID and source appear on separate lines.
        if not events:
            for match in re.finditer(
                r"Event ID:\s*(\d+).*?Source:\s*([^\r\n]+)",
                report_text,
                flags=re.IGNORECASE | re.DOTALL
            ):
                events.add((match.group(1).strip(), match.group(2).strip()))

        guidance = []
        guidance.append("HOW TO USE THIS PAGE")
        guidance.append("These are explanations and safe investigation steps, not a guaranteed diagnosis.")
        guidance.append("A Windows event does not automatically mean your PC is damaged.")
        guidance.append("")

        def add_if_found(event_id, provider_part, title, severity, meaning, steps):
            found = any(
                eid == str(event_id) and provider_part.lower() in provider.lower()
                for eid, provider in events
            )
            if found:
                guidance.append(f"{title} — {severity}")
                guidance.append(meaning)
                guidance.append("Safe next steps:")
                for number, step in enumerate(steps, 1):
                    guidance.append(f"  {number}. {step}")
                guidance.append("")

        add_if_found(
            10016, "DistributedCOM",
            "DistributedCOM event 10016", "Usually low priority",
            "This permission warning is commonly expected on Windows and often does not indicate a problem.",
            [
                "If Windows and your apps work normally, you can usually leave it alone.",
                "Do not change DCOM permissions or registry settings just to remove this warning."
            ]
        )
        add_if_found(
            10010, "DistributedCOM",
            "DistributedCOM event 10010", "Investigate if there are symptoms",
            "A DCOM component did not register within the expected time. The event details are needed to identify the component.",
            [
                "Note the event time and whether an app failed to open or respond around then.",
                "Open the event in Event Viewer and inspect its General and Details tabs.",
                "Avoid applying a generic registry or permissions fix without identifying the component."
            ]
        )
        add_if_found(
            11714, "MsiInstaller",
            "Windows Installer event 11714", "App installation issue",
            "This event can indicate that an older app version could not be removed. Check the full event message for the app name and error code.",
            [
                "Open Settings → Apps → Installed apps and check whether the named app is installed.",
                "If an update is failing, use the app publisher's official installer or repair/uninstall instructions.",
                "Do not manually delete Windows Installer cache files. If the installer asks for an old source file, use the official app support route."
            ]
        )
        add_if_found(
            134, "Microsoft-Windows-Time-Service",
            "Windows Time event 134", "Usually connectivity-related",
            "Windows Time could not resolve its configured time server using DNS.",
            [
                "Check that websites load and that other devices can access the internet.",
                "If internet works, open Settings → Time & language → Date & time and use Sync now.",
                "If the issue repeats, investigate DNS or network configuration rather than changing the clock registry."
            ]
        )
        add_if_found(
            34, "BTHUSB",
            "Bluetooth event 34", "Feature/compatibility warning",
            "The adapter reports that a particular Bluetooth Low Energy peripheral-mode feature is unavailable. This alone does not prove ordinary Bluetooth connections are broken.",
            [
                "If Bluetooth devices work, you may not need to do anything.",
                "If a device fails to connect, check the PC manufacturer's support page for the exact model's Bluetooth driver."
            ]
        )
        add_if_found(
            17, "BTHUSB",
            "Bluetooth event 17", "Investigate if Bluetooth stopped working",
            "Windows reports that the Bluetooth adapter failed and its driver was unloaded.",
            [
                "Check Settings → Bluetooth & devices to see whether Bluetooth is available.",
                "In Device Manager, inspect the Bluetooth adapter for a warning symbol and note its exact name.",
                "If needed, install the correct Bluetooth driver from the PC or adapter manufacturer's official support page. Avoid random driver-download websites."
            ]
        )
        add_if_found(
            20, "WindowsUpdateClient",
            "Windows Update event 20", "Update failed",
            "The report shows a Microsoft Defender security-intelligence update failed with error 0x80240016. This can be temporary or related to another update operation.",
            [
                "Open Settings → Windows Update and select Check for updates.",
                "Open Windows Security → Virus & threat protection → Protection updates and check for updates.",
                "Keep real-time antivirus protection enabled. If the failure repeats, record the latest error and troubleshoot Windows Update."
            ]
        )
        add_if_found(
            1, "CoworkVMService",
            "CoworkVMService event 1", "Insufficient details",
            "The report summary identifies a warning from this service, but the summary does not establish its cause.",
            [
                "If you recognise the related application, check whether it is working normally and update it through its official source.",
                "Inspect the event's full General message before attempting any repair."
            ]
        )

        if len(guidance) <= 4:
            guidance.extend([
                "No supported event patterns were recognised in the current report.",
                "Open the text report for full details, or run the Windows Error Scan to refresh it.",
                ""
            ])

        guidance.extend([
            "IMPORTANT SAFETY NOTES",
            "• PC Doctor does not automatically repair event-log issues.",
            "• Do not edit the registry, disable security software, or change DCOM permissions just to clear event logs.",
            "• If a problem is not affecting how you use the PC, an event may not need action.",
            "",
            f"Report file: {TEXT_REPORT}"
        ])

        text_box.insert("1.0", "\n".join(guidance))
        text_box.configure(state="disabled")

        button_row = ctk.CTkFrame(self.main, fg_color="transparent")
        button_row.grid(row=3, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            button_row,
            text="Open text report",
            command=self.open_text_report,
            height=40
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            button_row,
            text="Run a new scan",
            command=self.scan_windows_errors,
            height=40
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            button_row,
            text="← Back to home",
            command=self.show_dashboard,
            height=40
        ).pack(side="left")

    # REPORTS PAGE

    def show_reports(self):
        self.clear_main()

        self.heading(
            "Reports",
            "Open the diagnostic reports generated by PC Doctor."
        )

        ctk.CTkLabel(
            self.main,
            text=(
                "Run a Windows Error Scan first to generate updated "
                "Windows error reports. PC health check results are "
                "currently displayed directly in the app."
            ),
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        ).grid(row=2, column=0, sticky="w", pady=10)

        ctk.CTkButton(
            self.main,
            text="Scan Windows Errors",
            command=self.scan_windows_errors,
            height=42,
            width=220
        ).grid(row=3, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            self.main,
            text="Open HTML error report",
            command=self.open_html_report,
            height=42,
            width=220
        ).grid(row=4, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            self.main,
            text="Open text error report",
            command=self.open_text_report,
            height=42,
            width=220
        ).grid(row=5, column=0, sticky="w", pady=8)

        ctk.CTkButton(
            self.main,
            text="Open PC health report",
            command=lambda: self.open_report(
                os.path.join(TOOLKIT_DIR, "HealthReport.txt")
            ),
            height=42,
            width=220
        ).grid(row=6, column=0, sticky="w", pady=8)


if __name__ == "__main__":
    app = PCDoctor()
    app.mainloop()