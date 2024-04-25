#!/usr/bin/env python3

import os
import struct
import json
import socket
import sys
import time

def encode_data(data, opcode):
    length = len(data)
    payload = struct.pack('<L', length)
    return payload + struct.pack('<L', opcode) + data.encode('utf-8')

if len(sys.argv) < 3:
    print("Pass client Id and Payload please!!")
    sys.exit(1)

presence_client_id = sys.argv[1]

# Path to Discord IPC socket file for macOS
discord_ipc = os.path.expanduser("~/Library/Application Support/discord/Local Storage/leveldb/discord-ipc-0")

try:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(discord_ipc)
        
        # Handshake
        handshake_data = json.dumps({'v': 1, 'client_id': presence_client_id})
        s.sendall(encode_data(handshake_data, 0))

        # Wait (max 4 seconds) to receive the output
        time.sleep(4)

        # Set activity
        payload_data = sys.argv[2]
        s.sendall(encode_data(payload_data, 1))
except FileNotFoundError:
    print("Discord IPC not found. Make sure Discord is running.")
except Exception as e:
    print("An error occurred:", e)
