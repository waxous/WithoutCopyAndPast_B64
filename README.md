# WithoutCopyAndPast_B64

Require python-xlib

The purpose of this script is to simulate keystrokes to send base64 encoded file when no other vector is allowed (like on RDP without copy paste).

Under recent windows, certutil.exe allows base64 conversion so it's possible to retrieve original file.

`certutil -decode InFile OutFile

Be careful, it really simulates keystrokes so when you run it, you can't stop it anymore.

Verify keyboard translation between your host and the remote host on which you want to send your file.
