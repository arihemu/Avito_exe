"""Main application window."""

from __future__ import annotations

import os
import threading

import PySimpleGUI as sg
from dotenv import load_dotenv

from ..core.avito_client import AvitoClient
from ..services.description_service import DescriptionService
from ..scheduler import create_scheduler


def main() -> None:
    load_dotenv()
    layout = [
        [
            sg.Text("Client ID"),
            sg.Input(key="CLIENT_ID", default_text=os.getenv("AVITO_CLIENT_ID", "")),
        ],
        [
            sg.Text("Client Secret"),
            sg.Input(
                key="CLIENT_SECRET", default_text=os.getenv("AVITO_CLIENT_SECRET", "")
            ),
        ],
        [
            sg.Text("Refresh Token"),
            sg.Input(
                key="REFRESH_TOKEN", default_text=os.getenv("AVITO_REFRESH_TOKEN", "")
            ),
        ],
        [
            sg.Text("Account ID"),
            sg.Input(key="ACCOUNT_ID", default_text=os.getenv("ACCOUNT_ID", "")),
        ],
        [sg.Text("Description")],
        [sg.Multiline(size=(60, 10), key="DESC")],
        [sg.Button("Save Keys"), sg.Button("Update Description"), sg.Button("Exit")],
    ]

    window = sg.Window("Avito Helper Lite", layout)

    scheduler = create_scheduler()
    scheduler.start()

    client: AvitoClient | None = None
    desc_service: DescriptionService | None = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Save Keys":
            os.environ.update(
                {
                    "AVITO_CLIENT_ID": values["CLIENT_ID"],
                    "AVITO_CLIENT_SECRET": values["CLIENT_SECRET"],
                    "AVITO_REFRESH_TOKEN": values["REFRESH_TOKEN"],
                    "ACCOUNT_ID": values["ACCOUNT_ID"],
                }
            )
            client = AvitoClient(
                values["CLIENT_ID"], values["CLIENT_SECRET"], values["REFRESH_TOKEN"]
            )
            desc_service = DescriptionService(client, values["ACCOUNT_ID"])
            sg.popup("Saved")
        if event == "Update Description" and desc_service:
            text = values["DESC"]
            threading.Thread(target=desc_service.update_all_items, args=(text,)).start()

    scheduler.shutdown()
    window.close()


if __name__ == "__main__":
    main()
