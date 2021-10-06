import lzw
import re
import sys
import requests
import log

IP = "192.168.1.1"

response = requests.get(IP + "downloadFile?file=/var/config/psi")
assert response.status_code == 200

compressed_data = response.text
try:
    # the file has multiple "pages" so we need to use the "PagingDecoder" here
    decoder = lzw.PagingDecoder(initial_code_size=258)
    log.info("LZW Decompressing data...")
    r = b"".join([b"".join(pg) for pg in decoder.decodepages(compressed_data)])
    log.info("OK.")
    print(r)
except Exception as e:
    log.info(e)
    log.critical("Data decompression failed! Possible file corruption.")
    sys.exit(1)
