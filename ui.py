# UI helper functions for terminal styling and formatting
# Includes banners, tables, colors, and progress bars

import os
import sys
import time


# Check if terminal supports color output
USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"


class Colors:
    """ANSI color codes for terminal text formatting."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Colors
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"


def color(text, code):
    """Wraps text with ANSI color code if colors are enabled."""
    if USE_COLOR:
        return f"{code}{text}{Colors.RESET}"
    return text


def clear_screen():
    """Clears the console screen across Windows and Unix systems."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Pauses execution until user presses Enter."""
    input("\n  Press Enter to continue...")


def banner(title, subtitle=""):
    """Displays a stylized box banner for menus and screens."""
    width = 66
    border_top = "╔" + "═" * width + "╗"
    title_line = "║" + title.center(width) + "║"
    border_bottom = "╚" + "═" * width + "╝"

    print(color(border_top, Colors.CYAN))
    print(color(title_line, Colors.CYAN + Colors.BOLD))
    if subtitle:
        subtitle_line = "║" + subtitle.center(width) + "║"
        print(color(subtitle_line, Colors.CYAN))
    print(color(border_bottom, Colors.CYAN))


def section(title):
    """Prints a section heading with a divider line."""
    divider_len = max(2, 58 - len(title))
    print("\n" + color(f"── {title.upper()} ", Colors.BLUE) + color("─" * divider_len, Colors.BLUE))


def success(message):
    """Prints a green success message."""
    print(color(f"  ✓ {message}", Colors.GREEN))


def warning(message):
    """Prints a yellow warning message."""
    print(color(f"  ! {message}", Colors.YELLOW))


def error(message):
    """Prints a red error message."""
    print(color(f"  ✗ {message}", Colors.RED))


def loading(message, steps=3, delay=0.1):
    """Displays a brief loading animation."""
    print(f"  {message}", end="", flush=True)
    for _ in range(steps):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()


def progress_bar(value, width=24):
    """Renders a simple ASCII progress bar (0 to 100%)."""
    val = max(0.0, min(100.0, float(value)))
    filled = round(width * (val / 100.0))
    empty = width - filled
    return "█" * filled + "░" * empty


def table(headers, rows):
    """Prints tabular data neatly formatted with borders."""
    if not rows:
        print("  No records found.")
        return

    # Calculate max width required for each column
    num_cols = len(headers)
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for idx in range(num_cols):
            if idx < len(row):
                col_widths[idx] = max(col_widths[idx], len(str(row[idx])))

    # Helper to construct horizontal table border lines
    def build_border(left_char, cross_char, right_char, fill_char):
        segments = [fill_char * (w + 2) for w in col_widths]
        return left_char + cross_char.join(segments) + right_char

    # Top border
    print(build_border("┌", "┬", "┐", "─"))

    # Header row
    header_cells = [f" {headers[i]:<{col_widths[i]}} " for i in range(num_cols)]
    print("│" + "│".join(header_cells) + "│")

    # Header separator
    print(build_border("├", "┼", "┤", "─"))

    # Data rows
    for row in rows:
        cells = []
        for i in range(num_cols):
            cell_val = str(row[i]) if i < len(row) else ""
            cells.append(f" {cell_val:<{col_widths[i]}} ")
        print("│" + "│".join(cells) + "│")

    # Bottom border
    print(build_border("└", "┴", "┘", "─"))
