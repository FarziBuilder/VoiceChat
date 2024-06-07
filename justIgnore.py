from gi.repository import GLib
from bluetooth_agent import BluetoothAgent, register_agent

class AutoTrustAgent(BluetoothAgent):
    def authorize_service(self, device, uuid):
        return True

    def request_pincode(self, device):
        return "0000"

    def request_confirmation(self, device, passkey):
        self.set_trusted(device)
        return True

agent = AutoTrustAgent()
register_agent(agent, "/agent")
loop = GLib.MainLoop()
loop.run()
