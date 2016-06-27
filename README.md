# pyperv2012
Python module for controlling a Windows 2012 HyperV server using WinRM
This class uses pywinrm to access remote winRM enabled hosts and control HyperV 2012 and 2008. 
All commands should be available at some point to allow you to completely control HyperV from Linux!
Commands are returned in JSON output for easy(-ish) parsing. Currently this is pretty dirty and does not even come close to actually exploring all commands. Maybe one day it will but for now, I'm just sharing this if anyone wants to use or build on it.

You must enable Winrm on your server. For the most basic use (not as secure) run the following in an administrator Powershell prompt to allow basic user/password access:
c:\> winrm set winrm/config/service/auth '@{Basic="true"}'
c:\> winrm set winrm/config/service '@{AllowUnencrypted="true"}'


## Requirements
*pywinrm
*json
