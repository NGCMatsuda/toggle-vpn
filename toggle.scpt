set vpnConnectionInProgress to false
set MyVPNName to "NVPN-SE" -- set your VPN name

tell application "System Events"
	tell current location of network preferences
		set vpnConnectionInProgress to false
		
		-- determine current VPN connection status 	
		set isConnected to the service MyVPNName

		-- if connected, then disconnect	
		if isConnected is not null then
			if current configuration of isConnected is not connected then
				connect isConnected
				set vpnConnectionInProgress to true
			else
				disconnect isConnected
				set vpnConnectionInProgress to false
			end if
		end if
	end tell
end tell


if vpnConnectionInProgress is true then
	display notification "" with title "VPN Connection Staeted!" subtitle "You may now browse the internet privately and securely"
else
	display notification "" with title "VPN Connection Terminated!" subtitle "You may now browse the internet as public"
end if
