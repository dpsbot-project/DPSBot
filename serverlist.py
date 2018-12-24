from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import DPSBot
    from server import Serverlist
    global Serverlist
    serverlist = Serverlist(DPSBot())