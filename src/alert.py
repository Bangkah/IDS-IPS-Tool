
import sys

def print_alert(msg, severity="info"):
    color = {
        "info": "\033[94m",
        "warning": "\033[93m",
        "critical": "\033[91m",
        "end": "\033[0m"
    }
    sev = severity.lower()
    c = color.get(sev, color["info"])
    print(f"{c}{msg}{color['end']}", file=sys.stderr if sev=="critical" else sys.stdout)
