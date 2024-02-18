import socket
import time
import threading
import webbrowser
class Twitch:
    sock: socket = None
    # You may hardcode the OAuthToken however, it is recommended you don't... As the application will redirect you to the auth, and fetch the Token itself.
    OAuthToken: str = None 
    # Connect to the IRC server utilizing socket connection. 
    clientToken: str = 'bm5jz15swcewiz2igffjr24h7ijkdl'
    def twitch_connect(self, channel: str) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print("Connecting to Twitch...")
        # Specified twitch socket info.
        self.sock.connect(('irc.chat.twitch.tv', 6667))
        # Verify User Utilizing OAUTH or connect anonymously
        if self.OAuthToken == None:
            print("Awaiting Server Authentication...")
            # Spin up a listener for Token here! TODO
            
            # Open up the web browser. 
            webbrowser.open(f'https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={self.clientToken}&redirect_uri=http://localhost:3000/&scope=chat%3Aread+user%3Awrite%3Achat+user%3Abot&state=c3ab8aa609ea11e793ae92361f002671')


## TEST CODE BELOW.
twi = Twitch()
twi.twitch_connect('byte1223')
