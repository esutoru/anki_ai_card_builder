import anki
from aqt import mw, gui_hooks

from .gui.builder.component import CardBuilderWindow


def handle_js_message(handled, message, *args, **kwargs):
    if message != "bottom:open_card_builder":
        return handled

    window = CardBuilderWindow(mw)
    window.show()

    return True, None


def add_generate_button() -> None:
    mw.deckBrowser.drawLinks.append(["", "bottom:open_card_builder", "Card Builder"])
    gui_hooks.webview_did_receive_js_message.append(handle_js_message)


def setup_addon() -> None:
    anki.hooks.addHook("profileLoaded", add_generate_button)
