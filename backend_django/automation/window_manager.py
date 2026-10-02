import pygetwindow as gw


def focus_window(program):
    title = program.window_title_pattern
    wins = gw.getWindowsWithTitle(title)

    if not wins:
        raise Exception(f"No window found for: {title}")

    win = wins[0]
    win.activate()
    return True


def maximize_window(program):
    title = program.window_title_pattern
    wins = gw.getWindowsWithTitle(title)

    if not wins:
        raise Exception(f"No window found for: {title}")

    win = wins[0]
    win.maximize()
    return True
