#!/bin/python
import os, sys, time, json, ast
import requests, subprocess
from datetime import datetime

max_chunk_factor = 1024
stream_url = 'http://stream-relay-geo.ntslive.net/stream' # NTS Radio 1
running = True

# Returns timestamp as string
def get_ts():
    dt = datetime.now()
    return str(datetime.timestamp(dt))

if __name__ == '__main__':
    print("nts-tracklist-pirate")
    r = requests.get(stream_url, stream=True) # Connect to audio stream

    outputf = 'nts-tracklist-pirate.txt'
    fn = '/tmp/nts-stream-' + get_ts() + '.mp3'
    file = open(fn, 'wb')
    i =  0

    last = None
    with open(outputf, "r") as f:
        last = f.readlines()[-1]

    print("Recording...")
    for block in r.iter_content(1024):
        file.write(block)
        i += 1024
        if i  >= (1024 * max_chunk_factor):
            file.close()
            print("Sending chunk for scan...")

            data = ""
            process = subprocess.Popen("songrec audio-file-to-recognized-song " + fn, shell=True, stdout=subprocess.PIPE)
            for line in process.stdout:
                data += line.decode('utf-8')
            process.wait()

            try:
                json = json.loads(data)
                mname = json['track']['title'] + " " + json['track']['subtitle']
                print(mname)
                if last is not None:
                    if last.strip() == mname.strip():
                        print("Match last request! Cancelling...")
                        break
                        
                with open(outputf, "a") as f:
                   f.write(mname+"\n")
            except:
                print('No data found on chunk.')

            break
            
    os.remove(fn)
