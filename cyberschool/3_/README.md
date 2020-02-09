### python hell

Дан python-hell.pyc файл. Очевидно, это питоновский скрипт, вот только если кинуть его в **uncompyle6** он скажет **ImportError: Unknown magic number 227 in python-hell.pyc**

Все потому, что в файле отсутствует магический заголовок. Для питона 3 нужно добавить **42 0d 0d 0a 00 00 00 00 00 00 00 00 00 00 00 00**, для питона 2 **03 f3 0d 0a 6c e7 a3 5b** в начало файла.

После этого получается читабельный код.

```bash
uncompyle6 python-hell.pyc > stage1.py
```

```python
# stage1.py
# uncompyle6 version 3.6.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
# [GCC 8.3.0]
# Embedded file name: <string>
import base64
c = 'ZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBiYXJyeV9hc19GTFVGTApmcm9tIGluc3BlY3QgaW1wb3J0IGdldG91dGVyZnJhbWVzLCBjdXJyZW50ZnJhbWUKZnJvbSBjcnlwdG9ncmFwaHkuZmVybmV0IGltcG9ydCBGZXJuZXQKaW1wb3J0IGJhc2U2NAppbXBvcnQgdGhpcwppbXBvcnQgc3lzCgoKYyA9IGInZ0FBQUFBQmVMMVhkOWN6SkNpdEVmX3FaNXhKTjRsQlA0Wnkza0M0ZVYtRVZ4R09CUkswV1I5Y1gwZC1fdGswa2hJbTBzWGZVNXBSS2lkYzlhMXNpY0hSZkctdmtsYUNFTXNQSVd6VHVsLXcxMzFyY0F0X0NTSUI1UVNLMWNSbDg5WlpGcnJWOUxUaXJlRDV0MHFBb3V2aU5ObVFGQThaNF9NXzh2UHh5aDRVaWF4NXRnTi1NMGNvZ0I5U05OdEx0MVptNHJTanBlbW5WZmRVWlhLN3FJaDQ0RDV4cUNTSDRZdkNhSWoyT1I5Y0JMT1ZsZGdvQkE4djRUUXFNMm5hQkJkSXRRQ3ItQTRqRy1CUGZ6R2dlVU5uVFJtcHN6Ym50YjlEYnhBa2phU1h0Y0o3S1lkRF9OU0JCM1hQZjNhMUsyZ1hBaDJMcnVjbVNheU9CLXBmTnc1a3RPSlI3ME9Mc0h0RGNCYklSMW1USHpjYWVkTFpjZ0FVUk5MSDNzODlBM3lTVFhHQkhKaEotbTBBTER5SlJrZUFfal91N0FRTndkdjRiRXI0aUt2djZCSXlZYnRuclhVM1llb2hHRUZZOXl6OGlSRmxzb0xLVElkZGVRQUlFTUpiLVpCRTNkWGkxanRmajVhWEZTbzFvaG80ekRjTVIzWXBfdW1ma2VHTk5RUkExLUJqY3NqS0MyOXNCdFh6dE45MDY2T09MYWZEdG9DR0ROZ2w0U3pzR09lcDgteUVmSmhlZXdvZnNUblhRaVUzX2hwbU1GQk5IeGFheXY1dUQ1cDZ4Zk9Ya1VQSzFMa3l5WlhkNi0yTHhVbnZBN2VURzFyRkRuU1BsNWVmTEkxdDM5Zm5FSXJvSmFCRUZCUjhhcE9oRGd6cmdTMjRqQmoxaFRGUEM3T2hRcHlwdFgxWlVNWXpYSVEyVzFWT0NHQ0ttYUZoOXc1bG5kSjNvX1BEaWFwaGp0a084VG1ZVFlGdWhrMmQxMXcteXJBbGM0ZEpteXNnZGFtZE83NVJ1djFFdzhrSXVxRjdoT0pMaHBSbUNmMVdpQUU0b2lrR3BVcXNHZmxLX1l4TFBEZUc4LUl3MXN5Zk9wM0RPaHBaOXRDaUM0SGRIQ05FOGY1WFJ2MjAtZjgzWF9mWWtMNnZzWjhScGhiNE1KU0dhZVBzSHBuZ001bGpzd013UUdiTkJwSUx3UGpyMFFwS29UNHNRY29CQjhpN3FGdHZKMzNheWQtcnJ2c1E1UmJoNXpOTDY3UEYtcjNJd2dQb0VBY2o5OWtSeDFHUzRTMWljbFYxNUtmeXBhaTZ4LXpsVEZyYW1ZdUFqd1pfVUJGSHkzTjQ5WHlWaXhCNTlLSENfOFlBVnRrUjctMHAxZGdtZ2lBdzFGSUY4RkpTVG5WQ2N2bU4zaTF0RXZTQ1RHb0h4bUJMaURxak5vd01sSzdDcmlyNXktSms3cVRGdm55WnRrQnZqc0VWWnhSYy1qWngyUmxVU1piUTJYV0xQVjk0RDN0VEVXMXdLbzEwMHRWSHJzTS1lcXhES2pxNUlMV3B3VkpoYlN5TE43bDRNNFZybmt4NXhNdVRreFdHcnllRzg5OG9aeWdsWTRwczhzeWhhNUlWZGI1WURrcVBJQ1FJaXdTTDdLaDkxanNCbTNCTnVNLWtheWZCVVBUd29TSkkwWUt2MFo4SjFqQlFZZnhJY3duTEFzSzVqdDlRMm43WTZPaFRBQmdVdXc4Qk05dk5Nall4a0NQamw2WHJmSGpxSURQSk9xOEtkTkF6YXdkVE8yWDZ3ZncxT1FMeDhJOFlsTTNKTFl3M3NNbUJrTko3Z19scGRuT1QtZTR0M2xWNmJVMl92aVBWSGJ3bHpldkZnNGtIZnF1b2xrS0djN21NZ290cThMUDQyemo5Mzl1V3g2SWhXZkF0YkM2d0RURHYzRnJCS25Rc1hxRkwtQ3p6el9TZmZhX0tMZGlqQUZjR0MtZVY3TjVkZnRXYWpVcGtjT2dGeXRKcFRsakJJZG9teVFpRXdka2dDYV8zQnFVTXcyRHdEUWlEaXVicnVCMmczQXBNeVREel9EcjBYMlNncHdKM2Mwemhvck5SMHlQTFo5cWd6dUVvVEJ3U1Nvd1M5WU9HbGo2dmtWSFdIUXJSNkl5N0NOZndZSzR0V2dYb2RYQkZReFFGNUxxR2oxZFl6Qk9wTG01MVN4azEzMGJza0JrSmxETlFVQTQ5V0NNaGtIN01Hc2s5ejE5QTA1MkZiWVduOUZsNDZEU1ZQMTVUUHhkRllCaW1mNGNldUw1Ym1ZTXhhYmxZMjNpczRkWWhxY0lJS0h3RlZSLUQ0MzhoVzhRSXZ1T0ZsbWVoRU54dlZzSWlrYVJocS1uSXZneGtZVnVjWlR2V0VaQS1taV9pQmcwaU1aREJHSm1HbDZaTDhqOE56YW1CN1lWeHdRSGZxRGNoNWExVDJac1BpX2F0NjcwMWY5OGt6WmlJd05HUExnQXgxc0xURnpNTVhwVTdBeGJlbUM2Q2xjempqd3hmWURYNktSaUduQl8xT04wTXRNbnE2NGFCWS0yYXdEUnVfdzBkU25JRGdSaVlnOXJobEJGSGJGX3hEcXNLVHFBaGtCNWEtRFVqTlhaZkw4M3NCLUxqTWdtS2ZiUjVBZ2VYYTlCcHZwbkI4alJLRzE0aVBMa2s3T3ZKcHBUb2dEWE9zd2F2OE1iWEl5OHZIRmpTUW1ydVRCQVZwQzgyUTgxbkdSSloyekFDNlVlNkxrY0lVVlM4V1RuS2dDMmhQckhfdTdJVWFQcjcySHV6SkVBU3J3YVQ4TDFhLWVRSVFGVlM3VHVlTzBmdl95UVlsdTdfaHVESDZZVXhybDViTXlwZUszNS1vTDI4OFRJdEZqc2VfVUptRkFtS3JkWC14S0liUnYzLWZoNzlkTUNBWFNmaVNzeVMyQ0YzQ2RFTXNlYUZ0NDJzc1RSaVk2czBSRWpnQk1CU0NNQXdZLWhkV2RDdjFqbjVaZEtBdG5iUjFyc0l4RTEwejhMNHhENXBPS0R0SXhIcjZ4NHNHTW5EQVNUUjBfSWhCTnlIS09GakdpMkRyRnVGTmdPTDZxTGtqWDJNVEhkcWRadEdxdnRRdUxHWEVZcWZTbEloNTlRaUpQWGM1Mk90cTBXRWIyVlBjMHB6b09zZ2p0T0FaWFBqSFVyb3ZDeFVjeGJEM3FEOHVQc1pKSGVMaDdBZFMybzBqU3Vob1N4a01TOE9qSnF4aXhFUkF4OHFCOFdmbXVKcWdoVWNTN21YbHpCWFBYa29VdkdwU0dNX1FENjc3VFR2T0dwZzd2M0lUaDNsWDgyS2VkRmh2eVY1WV9TeGk5cExmbHpCWXg1ei15eDBiN2pmOFdvamY3bTRSSzVSRm5wcUwyeG5aby1PSnUwZTFtUW43YV83dHl2Mnc1QWtvMG1xZFJZRnk2TW1nbUN4YTZFcjBtdU5Va2Qtb0JvaklRMGhtMi00ajE2Vm1jczBPOGZlSFI1bDY2bENJZ0E5Y3JwUWRSc19aNDZSak9VVTh6MzRmQmNmYVBfbjB6M2MxUU5WZ3ZOejZJZlUyLWQtbHN1aEc5X1RXQ19PeE1Cdy1ibFk5QlBScDFIVWQzNmdzeXNpdlFhcG9tbkJseVVCaUVEUmt2NGZ2QnVvMUNjMTFmVjM2MlZlRWUwZmRURTZhVlVsN21sRVFHTlJhQkVidnVYU3JTNFFuVEp0VE1RUEZkTEtuWE9oYmJTb1ZJMVhtRVdYSDl1eldwbEx6UEVVb2FuV0VVYmFBSVF3WTFfR3UtWHpKX2xDQUpqV0M4T0dYZlljWGwwYXFIOEF2NHBmQzBpNDNwelE3WjhyaHVZZjM5ZWJfdU5JRTF3WExkSWFQWHBVVU9MNm9odm50S1NFcWhqbU5jb2pIb3E0M0ZPMUhGcWpLSERldkpfdG03d0xERTNzT1Btel9FSlAtMzg3RlY1NEM3V1dCT21xVFVoWGtLQm44ZzlXcFBDUTN5c2FYbnNIajRXSWotUk4yV1VNdWN0aWJDUXU2TVdsamJVR0FlQ1NYNnlpc1VWWklUaWJFM3lfZExOaHNTRHI1TllqWjByTVJOZG9uV0R5eTctWC1XdklqVDFfZjlzTnF2TmVFSUdUcUZ3QlNfbEJLZHdUU19VSDdpalZZQ1pVY2dHZVY1MUMwZlliak0tTFp3ZjBpZE9fOHZRYzZMUXhjOTgtQXVFUnJfbGpIdzM1OUNhQmtqcUphczNwMG4zY0NUZ21UV1gzMlpNckJsTmRIUFY1TkZUVEdtS1NtTXRQcDNoeEhfQWFpM1lsQUlob0JwTGVlVTdBM1V6N05kdDdsc2MzbmxyTWxzckZTSnIydFEtX0trNFVILUh4ME1MYVBXT3o1TlN1M204MHhHeFFGcHpZbm1paVIzR1ljS2RqYXZsMW5ldTg5dzZucExnVlZLYkZzRmJvVmtKVHN2RmRfbnkzVGh0ZU9HeVFpNXMtNlc1NUM1Sm94aDVybGhlYVdhcjV0bU43c1dLQUtaUmJsX2JWMjAzUGk5cFdvdHMzbHlIVmNmUW5rN1E5VjJPUlRZYjdFM2RneVBtVHl1V1BQTW1nWlNaY00zeXRXekJOZzdSUVNGZGNUMUVOaTZYdHBqb3ZHVDgwSEtwOEQ4MTlqVWx6NTlXOVNrUGdTZlVMTTI2clhhc0NSVW9pOEhBUG5jaEZoV2dKdnFtaFhrWUpEQ3d2Sm15YkkwNy11YVFIWVFxSnhFR1A1TV9oWDVCek5hSVdEOEVkU0dQb3hRU3huOEpuZDE1UUl3U0RON1c2dndoN1djOTAtR3kwbzRybVBIdHpIMEdIVXVRaW1UN3R2YVhVRDRPb2Y0ZmIwNFp4c3pCaDZfeEtGRm9lcHpaUGMwaEp0RFJHbjFFUl83ek9TUEZobkJGTHNudjNwS21HVGFRUUlZNGlISUNGRWpyU0dlMjJfNTFBRHRoeWxkeXFTeTlEeHZ0MUltOWdONmdyNVI0MXBhWmV2dFlndzdmb2tTekhNVGlMT1R4alRSSU5HazlKYll2ekV1SnFTekVYQnV5NlJSZGlGVkpPVzBBV25maHlRNVZoQ0ZKX1daeVVEMGxNdXRCSURDdE1RLTR4NlZtM25GWG5hWTJpOVNnTnljSDd6V2ZGT04zcUZsS1phNkFyaUJCMlcxTmRodlRzX0RocXRZd192V2N5VkI4anFKOGpaZnRJSEhoUTMybElXOUV1YkNqQzg1c05rVXZQRzkzNU4xQUpuTW5hNVMxcTRuNjNRWC1aYlNSTXp3MDZkRmVyY2ZDTFlELUVJQnZUalE4RFg2U0VuQ1hjNV9DWkppNXVkWkxoNVJBZnZHUTR0blJFZklkdGlaeEhuTTdDa1gxSlF5VllpREpHLXNIUEVObHJrSTRQMDZpZXFySXJOUGRualJfSXFqOXQyV1ZBSHI3ZWNsdjhXYXh3ZTBVNnJtcGY1REhtSVpGSG9MRmNNSGJQVjZsUzJFa25iVHBHcUxjV0taVWJRLU94X0IydGx1dDZyRjRnNDdaQkVmM2RIMjJtaE9Oc04xSy1NVHdSR2RCN2g5UzZfa2JMd3hEYzlTOUI1ZXkzY0VVNWo2X1dTNHhOdGV6Z1U1YV9QdmRYOVZpQ0VhZi1WUFRiUk04d2VNbVFsQlpvcTBMZDJ3Ukh4RlFydVVLczdqWVJjLXJfM1JkNVZWYjRxTFFjQnFNeHZDSldaUFlmbkNWenZ2cmdPeHVWZVpRR1RMZ2QtTVB6Y3ZFeUVRbC0xTmZib3FKcjBVdjRsY2czN2FjQmxfZ2xuNDRLLUJ3dDB1R0Zlc2lMLWdhUmNSOFVYVXpmVk5mN1FSd1FuYlk4c1RPZENxQnRlSmFmejhSci1MNmtDNlNoaTQyamVNOUlMN2VCQlNSRDZxV1NFckUyVFZyTU5FME5SWFIxWW5pbWNjMmEzcTRsQjQwcnEwZUUzaUh0Mmw5U2pEYVJPRkdrdFU5YndWWklWQ0ZrckZaZFgwRi1xUVF1T3kwanhRTERzOVFfZUc2b0UxbExDRUdRZHk0bnI4TmpLVENVNnowOUdEZThSY0lGS0RqSFRDZUJTTlBQREJLcy0yd1N0RGNBbV84Y1hzWFZtU21qS3d1eVRnOGVNSk9iN01CR3Nacmo4Rm56eGloTFpBY3NZa3JZel9WdGtVWFViRUJOV3lGWDhFNjltZ0E0Y1FQT1A4aUlxcFpzcScKCgpweXRob25fdmVyc2lvbiA9ICIzLjYuOSIKCgpkZWYgcHJpbnRfaGVscCgpOgogICAgaWYgKEZhbHNlID09IEZhbHNlKSBpbiBbRmFsc2VdIG9yIEZhbHNlID09IChGYWxzZSBpbiBbRmFsc2VdKSBvciBGYWxzZSA9PSBGYWxzZSBpbiBbRmFsc2VdOgogICAgICAgIGEsIGIgPSAyNTYsIDI1NgogICAgICAgIGlmIGEgaXMgYiA6CiAgICAgICAgICAgIHgsIHkgPSBbXSwgW10KICAgICAgICAgICAgaWYgbm90IHggaXMgeToKICAgICAgICAgICAgICAgIGEsIGIgPSB0dXBsZSgpLCB0dXBsZSgpCiAgICAgICAgICAgICAgICBpZiBhIGlzIGI6CiAgICAgICAgICAgICAgICAgICAgcHJpbnQoJ1xuJykKICAgICAgICAgICAgICAgICAgICBldmFsKGJhc2U2NC5iNjRkZWNvZGUoYidjSEpwYm5Rb1lpSkpkQ0JwY3lCaVlYTmxOalFnYUdWc2JDRWhJU0lwJykpCgpkZWYgbWF5YmVfcHJpbnRfaGVscCgpOgogICAgaWYgYWxsKFtdKSBhbmQgbm90IGFsbChbW11dKToKICAgICAgICBkZWYgZih4KToKICAgICAgICAgICAgaWYgeCA9PSAzOgogICAgICAgICAgICAgICAgcmV0dXJuIFsiSGVsbG8hIl0KICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHlpZWxkIDIuNzE4MjgxODI4NDU5MDQ1MjM1MzYwMjg3NDcxMzUyNjYyNDk3NzU3MjQ3MDkzNjk5OQogICAgICAgIGlmIGxpc3QoZigzKSkgPT0gW106CiAgICAgICAgICAgIGEgPSBbMSwgMiwgMywgNF0KICAgICAgICAgICAgYiA9IGEKICAgICAgICAgICAgYSArPSBbNSwgNiwgNywgOF0KICAgICAgICAgICAgaWYgYiA9PSBbMSwgMiwgMywgNCwgNSwgNiwgNywgOF06CiAgICAgICAgICAgICAgICBwcmludF9oZWxwKCkKCgpkZWYgcHJpbnRfbmV4dF9sZXZlbCgpOgogICAgc2VjcmV0X2tleSA9IGIiTVNVIEN5YmVyc2Nob29sIgogICAgZm9yX2JydXRlX2ZvcmNlID0gYiczPz8/PycKICAgIHNlY3JldF9rZXkgPSBzZWNyZXRfa2V5ICsgZm9yX2JydXRlX2ZvcmNlCiAgICBzZWNyZXRfa2V5ICs9IGInMTIzNDU2Nzg5MDEyJwogICAgc2VjcmV0X2tleSA9IGJhc2U2NC51cmxzYWZlX2I2NGVuY29kZShzZWNyZXRfa2V5KQogICAgaSA9IGxlbihnZXRvdXRlcmZyYW1lcyhjdXJyZW50ZnJhbWUoKSkpCiAgICBmID0gRmVybmV0KHNlY3JldF9rZXkpCiAgICBwID0gIiIKICAgIHRyeToKICAgICAgICBpZiBpIDwgMzoKICAgICAgICAgICAgcHJpbnQoYmFzZTY0LmI2NGRlY29kZShiIlJHOXVKM1FnYzJ0cGNDQnRZWGxpWlY5dFlYbGlaVjl3Y21sdWRGOW9aV3h3SVNFaCIpKQogICAgICAgICAgICByZXR1cm4KICAgICAgICBwID0gZi5kZWNyeXB0KGMpCiAgICBleGNlcHQ6CiAgICAgICAgcHJpbnQoIk9vb3BzLi4iKQogICAgaWYgcDoKICAgICAgICBwcmludChiYXNlNjQuYjY0ZGVjb2RlKHApKQoKCmRlZiBtYXliZV9tYXliZV9wcmludF9oZWxwKCk6CiAgICBpZiBldmFsKCciUnVieSIgPD4gIlB5dGhvbiInKToKICAgICAgICBsb3ZlID0gdGhpcwogICAgICAgIGlmIHRoaXMgaXMgbG92ZToKICAgICAgICAgICAgaWYgbG92ZSBpcyBub3QgVHJ1ZSBvciBGYWxzZToKICAgICAgICAgICAgICAgIGlmIG5vdCBsb3ZlIGlzIEZhbHNlOgogICAgICAgICAgICAgICAgICAgIGlmIGxvdmUgaXMgbm90IFRydWUgb3IgRmFsc2U6CiAgICAgICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICAgICAgICAgICAgICAgICAgZXhjZXB0OgogICAgICAgICAgICAgICAgICAgICAgICAgICAgcHJpbnQoIkV4Y2VwdGlvbiBvY2N1cnJlZCEhISIpCiAgICAgICAgICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiBoYXNoKGZsb2F0KCctaW5mJykpID09IC0zMTQxNTk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWUgPSAxMQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHXQtSA9IDMyCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgdmFsdWUgPT0gMTE6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1heWJlX3ByaW50X2hlbHAoKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwcmludF9uZXh0X2xldmVsKCkKCgppZiBzeXMudmVyc2lvbi5maW5kKHB5dGhvbl92ZXJzaW9uKSA9PSAtMToKICAgIHByaW50KCkKICAgIHByaW50KCJHbyBhd2F5ISIpCiAgICBwcmludChmIllvdSBoYXZlIHRvIHVzZSB7cHl0aG9uX3ZlcnNpb259ISIpCiAgICBwcmludCgpCiAgICBzeXMuZXhpdCgtMSkKCgp2YWx1ZSA9IDExCnZhbHXQtSA9IDMyCmlmIHZhbHVlID09IDExOgogICAgaWYgRmFsc2UgKiogRmFsc2UgPT0gVHJ1ZToKICAgICAgICBzaXhfbWlsbGlvbiA9IDZfMDAwXzAwMAogICAgICAgIGlmIHNpeF9taWxsaW9uID09IDYwMDAwMDA6CiAgICAgICAgICAgIG1heWJlX21heWJlX3ByaW50X2hlbHAoKQoK'
# okay decompiling python-hell.pyc

```

c - base64 строка, намек дает еще и **import base64**

после расшифровки получаем stage2.py

```bash
# stage2.py
from __future__ import barry_as_FLUFL
from inspect import getouterframes, currentframe
from cryptography.fernet import Fernet
import base64
import this
import sys


c = b'gAAAAABeL1Xd9czJCitEf_qZ5xJN4lBP4Zy3kC4eV-EVxGOBRK0WR9cX0d-_tk0khIm0sXfU5pRKidc9a1sicHRfG-vklaCEMsPIWzTul-w131rcAt_CSIB5QSK1cRl89ZZFrrV9LTireD5t0qAouviNNmQFA8Z4_M_8vPxyh4Uiax5tgN-M0cogB9SNNtLt1Zm4rSjpemnVfdUZXK7qIh44D5xqCSH4YvCaIj2OR9cBLOVldgoBA8v4TQqM2naBBdItQCr-A4jG-BPfzGgeUNnTRmpszbntb9DbxAkjaSXtcJ7KYdD_NSBB3XPf3a1K2gXAh2LrucmSayOB-pfNw5ktOJR70OLsHtDcBbIR1mTHzcaedLZcgAURNLH3s89A3ySTXGBHJhJ-m0ALDyJRkeA_j_u7AQNwdv4bEr4iKvv6BIyYbtnrXU3YeohGEFY9yz8iRFlsoLKTIddeQAIEMJb-ZBE3dXi1jtfj5aXFSo1oho4zDcMR3Yp_umfkeGNNQRA1-BjcsjKC29sBtXztN9066OOLafDtoCGDNgl4SzsGOep8-yEfJheewofsTnXQiU3_hpmMFBNHxaayv5uD5p6xfOXkUPK1LkyyZXd6-2LxUnvA7eTG1rFDnSPl5efLI1t39fnEIroJaBEFBR8apOhDgzrgS24jBj1hTFPC7OhQpyptX1ZUMYzXIQ2W1VOCGCKmaFh9w5lndJ3o_PDiaphjtkO8TmYTYFuhk2d11w-yrAlc4dJmysgdamdO75Ruv1Ew8kIuqF7hOJLhpRmCf1WiAE4oikGpUqsGflK_YxLPDeG8-Iw1syfOp3DOhpZ9tCiC4HdHCNE8f5XRv20-f83X_fYkL6vsZ8Rphb4MJSGaePsHpngM5ljswMwQGbNBpILwPjr0QpKoT4sQcoBB8i7qFtvJ33ayd-rrvsQ5Rbh5zNL67PF-r3IwgPoEAcj99kRx1GS4S1iclV15Kfypai6x-zlTFramYuAjwZ_UBFHy3N49XyVixB59KHC_8YAVtkR7-0p1dgmgiAw1FIF8FJSTnVCcvmN3i1tEvSCTGoHxmBLiDqjNowMlK7Crir5y-Jk7qTFvnyZtkBvjsEVZxRc-jZx2RlUSZbQ2XWLPV94D3tTEW1wKo100tVHrsM-eqxDKjq5ILWpwVJhbSyLN7l4M4Vrnkx5xMuTkxWGryeG898oZyglY4ps8syha5IVdb5YDkqPICQIiwSL7Kh91jsBm3BNuM-kayfBUPTwoSJI0YKv0Z8J1jBQYfxIcwnLAsK5jt9Q2n7Y6OhTABgUuw8BM9vNMjYxkCPjl6XrfHjqIDPJOq8KdNAzawdTO2X6wfw1OQLx8I8YlM3JLYw3sMmBkNJ7g_lpdnOT-e4t3lV6bU2_viPVHbwlzevFg4kHfquolkKGc7mMgotq8LP42zj939uWx6IhWfAtbC6wDTDv3FrBKnQsXqFL-Czzz_Sffa_KLdijAFcGC-eV7N5dftWajUpkcOgFytJpTljBIdomyQiEwdkgCa_3BqUMw2DwDQiDiubruB2g3ApMyTDz_Dr0X2SgpwJ3c0zhorNR0yPLZ9qgzuEoTBwSSowS9YOGlj6vkVHWHQrR6Iy7CNfwYK4tWgXodXBFQxQF5LqGj1dYzBOpLm51Sxk130bskBkJlDNQUA49WCMhkH7MGsk9z19A052FbYWn9Fl46DSVP15TPxdFYBimf4ceuL5bmYMxablY23is4dYhqcIIKHwFVR-D438hW8QIvuOFlmehENxvVsIikaRhq-nIvgxkYVucZTvWEZA-mi_iBg0iMZDBGJmGl6ZL8j8NzamB7YVxwQHfqDch5a1T2ZsPi_at6701f98kzZiIwNGPLgAx1sLTFzMMXpU7AxbemC6ClczjjwxfYDX6KRiGnB_1ON0MtMnq64aBY-2awDRu_w0dSnIDgRiYg9rhlBFHbF_xDqsKTqAhkB5a-DUjNXZfL83sB-LjMgmKfbR5AgeXa9BpvpnB8jRKG14iPLkk7OvJppTogDXOswav8MbXIy8vHFjSQmruTBAVpC82Q81nGRJZ2zAC6Ue6LkcIUVS8WTnKgC2hPrH_u7IUaPr72HuzJEASrwaT8L1a-eQIQFVS7TueO0fv_yQYlu7_huDH6YUxrl5bMypeK35-oL288TItFjse_UJmFAmKrdX-xKIbRv3-fh79dMCAXSfiSsyS2CF3CdEMseaFt42ssTRiY6s0REjgBMBSCMAwY-hdWdCv1jn5ZdKAtnbR1rsIxE10z8L4xD5pOKDtIxHr6x4sGMnDASTR0_IhBNyHKOFjGi2DrFuFNgOL6qLkjX2MTHdqdZtGqvtQuLGXEYqfSlIh59QiJPXc52Otq0WEb2VPc0pzoOsgjtOAZXPjHUrovCxUcxbD3qD8uPsZJHeLh7AdS2o0jSuhoSxkMS8OjJqxixERAx8qB8WfmuJqghUcS7mXlzBXPXkoUvGpSGM_QD677TTvOGpg7v3ITh3lX82KedFhvyV5Y_Sxi9pLflzBYx5z-yx0b7jf8Wojf7m4RK5RFnpqL2xnZo-OJu0e1mQn7a_7tyv2w5Ako0mqdRYFy6MmgmCxa6Er0muNUkd-oBojIQ0hm2-4j16Vmcs0O8feHR5l66lCIgA9crpQdRs_Z46RjOUU8z34fBcfaP_n0z3c1QNVgvNz6IfU2-d-lsuhG9_TWC_OxMBw-blY9BPRp1HUd36gsysivQapomnBlyUBiEDRkv4fvBuo1Cc11fV362VeEe0fdTE6aVUl7mlEQGNRaBEbvuXSrS4QnTJtTMQPFdLKnXOhbbSoVI1XmEWXH9uzWplLzPEUoanWEUbaAIQwY1_Gu-XzJ_lCAJjWC8OGXfYcXl0aqH8Av4pfC0i43pzQ7Z8rhuYf39eb_uNIE1wXLdIaPXpUUOL6ohvntKSEqhjmNcojHoq43FO1HFqjKHDevJ_tm7wLDE3sOPmz_EJP-387FV54C7WWBOmqTUhXkKBn8g9WpPCQ3ysaXnsHj4WIj-RN2WUMuctibCQu6MWljbUGAeCSX6yisUVZITibE3y_dLNhsSDr5NYjZ0rMRNdonWDyy7-X-WvIjT1_f9sNqvNeEIGTqFwBS_lBKdwTS_UH7ijVYCZUcgGeV51C0fYbjM-LZwf0idO_8vQc6LQxc98-AuERr_ljHw359CaBkjqJas3p0n3cCTgmTWX32ZMrBlNdHPV5NFTTGmKSmMtPp3hxH_Aai3YlAIhoBpLeeU7A3Uz7Ndt7lsc3nlrMlsrFSJr2tQ-_Kk4UH-Hx0MLaPWOz5NSu3m80xGxQFpzYnmiiR3GYcKdjavl1neu89w6npLgVVKbFsFboVkJTsvFd_ny3ThteOGyQi5s-6W55C5Joxh5rlheaWar5tmN7sWKAKZRbl_bV203Pi9pWots3lyHVcfQnk7Q9V2ORTYb7E3dgyPmTyuWPPMmgZSZcM3ytWzBNg7RQSFdcT1ENi6XtpjovGT80HKp8D819jUlz59W9SkPgSfULM26rXasCRUoi8HAPnchFhWgJvqmhXkYJDCwvJmybI07-uaQHYQqJxEGP5M_hX5BzNaIWD8EdSGPoxQSxn8Jnd15QIwSDN7W6vwh7Wc90-Gy0o4rmPHtzH0GHUuQimT7tvaXUD4Oof4fb04ZxszBh6_xKFFoepzZPc0hJtDRGn1ER_7zOSPFhnBFLsnv3pKmGTaQQIY4iHICFEjrSGe22_51ADthyldyqSy9Dxvt1Im9gN6gr5R41paZevtYgw7fokSzHMTiLOTxjTRINGk9JbYvzEuJqSzEXBuy6RRdiFVJOW0AWnfhyQ5VhCFJ_WZyUD0lMutBIDCtMQ-4x6Vm3nFXnaY2i9SgNycH7zWfFON3qFlKZa6AriBB2W1NdhvTs_DhqtYw_vWcyVB8jqJ8jZftIHHhQ32lIW9EubCjC85sNkUvPG935N1AJnMna5S1q4n63QX-ZbSRMzw06dFercfCLYD-EIBvTjQ8DX6SEnCXc5_CZJi5udZLh5RAfvGQ4tnREfIdtiZxHnM7CkX1JQyVYiDJG-sHPENlrkI4P06ieqrIrNPdnjR_Iqj9t2WVAHr7eclv8Waxwe0U6rmpf5DHmIZFHoLFcMHbPV6lS2EknbTpGqLcWKZUbQ-Ox_B2tlut6rF4g47ZBEf3dH22mhONsN1K-MTwRGdB7h9S6_kbLwxDc9S9B5ey3cEU5j6_WS4xNtezgU5a_PvdX9ViCEaf-VPTbRM8weMmQlBZoq0Ld2wRHxFQruUKs7jYRc-r_3Rd5VVb4qLQcBqMxvCJWZPYfnCVzvvrgOxuVeZQGTLgd-MPzcvEyEQl-1NfboqJr0Uv4lcg37acBl_gln44K-Bwt0uGFesiL-gaRcR8UXUzfVNf7QRwQnbY8sTOdCqBteJafz8Rr-L6kC6Shi42jeM9IL7eBBSRD6qWSErE2TVrMNE0NRXR1Ynimcc2a3q4lB40rq0eE3iHt2l9SjDaROFGktU9bwVZIVCFkrFZdX0F-qQQuOy0jxQLDs9Q_eG6oE1lLCEGQdy4nr8NjKTCU6z09GDe8RcIFKDjHTCeBSNPPDBKs-2wStDcAm_8cXsXVmSmjKwuyTg8eMJOb7MBGsZrj8FnzxihLZAcsYkrYz_VtkUXUbEBNWyFX8E69mgA4cQPOP8iIqpZsq'


python_version = "3.6.9"


def print_help():
    if (False == False) in [False] or False == (False in [False]) or False == False in [False]:
        a, b = 256, 256
        if a is b :
            x, y = [], []
            if not x is y:
                a, b = tuple(), tuple()
                if a is b:
                    print('\n')
                    eval(base64.b64decode(b'cHJpbnQoYiJJdCBpcyBiYXNlNjQgaGVsbCEhISIp'))

def maybe_print_help():
    if all([]) and not all([[]]):
        def f(x):
            if x == 3:
                return ["Hello!"]
            else:
                yield 2.7182818284590452353602874713526624977572470936999
        if list(f(3)) == []:
            a = [1, 2, 3, 4]
            b = a
            a += [5, 6, 7, 8]
            if b == [1, 2, 3, 4, 5, 6, 7, 8]:
                print_help()


def print_next_level():
    secret_key = b"MSU Cyberschool"
    for_brute_force = b'3????'
    secret_key = secret_key + for_brute_force
    secret_key += b'123456789012'
    secret_key = base64.urlsafe_b64encode(secret_key)
    i = len(getouterframes(currentframe()))
    f = Fernet(secret_key)
    p = ""
    try:
        if i < 3:
            print(base64.b64decode(b"RG9uJ3Qgc2tpcCBtYXliZV9tYXliZV9wcmludF9oZWxwISEh"))
            return
        p = f.decrypt(c)
    except:
        print("Ooops..")
    if p:
        print(base64.b64decode(p))


def maybe_maybe_print_help():
    if eval('"Ruby" <> "Python"'):
        love = this
        if this is love:
            if love is not True or False:
                if not love is False:
                    if love is not True or False:
                        try:
                            pass
                        except:
                            print("Exception occurred!!!")
                        else:
                            if hash(float('-inf')) == -314159:
                                value = 11
                                valuе = 32
                                if value == 11:
                                    maybe_print_help()
                                    print_next_level()


if sys.version.find(python_version) == -1:
    print()
    print("Go away!")
    print(f"You have to use {python_version}!")
    print()
    sys.exit(-1)


value = 11
valuе = 32
if value == 11:
    if False ** False == True:
        six_million = 6_000_000
        if six_million == 6000000:
            maybe_maybe_print_help()
```

Видно, что файл обфусцирован, и код просто принтит фразы из **import this**

самое важное происходит сдесь:

```python
def print_next_level():
    secret_key = b"MSU Cyberschool"
    for_brute_force = b'3????'
    secret_key = secret_key + for_brute_force
    secret_key += b'123456789012'
    secret_key = base64.urlsafe_b64encode(secret_key)
    i = len(getouterframes(currentframe()))
    f = Fernet(secret_key)
    p = ""
    try:
        if i < 3:
            print(base64.b64decode(b"RG9uJ3Qgc2tpcCBtYXliZV9tYXliZV9wcmludF9oZWxwISEh"))
            return
        p = f.decrypt(c)
```

переменная for_brute_force как бы намекает на брутфорс ключа, но можно догадаться что там число 31337. после чего расшифровываем c и получаем stage3.py



```python
# stage3.py
import base64

fowl = b'WJyYWNhZGFicmE6CiAgICBzb21ldGhpbmcgPSBhYnJhY2FkYWJyYS5yZWFkKCkKaSA9IDAKc2VjcmV0X251bWJlcnNfbGlzdCwgcHVibGljX251bWJlcnNfbGlzdCA9IFsnbicsJ3UnLCdsJywnbCddLCBbJ3AnLCd1JywnYicsJ2wnLCdpJywnYyddCnNlY3JldF9udW1iZXJzX2xpc3QgPSBbKDMxMzM3IC0gMioqMTQgLSAoMTY0MjkgXiAzMTMzNykpIF4gMzEzMzcgZm9yIGkgaW4gcmFuZ2UoMioqNDA5NildOwpzZWNyZXRfbnVtYmVyc19saXN0ID0gbGlzdChtYXAobGFtYmRhIHg6ICh4ICogMTAwNTAwKSAvLyAxMDAgLy8gMjAxIC8vIDUgJSAzNywgc2VjcmV0X251bWJlcnNfbGlzdCkpCmtleV8xID0gIml1bmdlZVNoYWgyZWl5NHF1YWNoIgprZXlfMV9jb3B5IDo9ICcnLmpvaW4oWydpJywgJ3UnLCAnbicsICdnJywgJ2UnLCAnICcsICdlJywgJ1MnLCAnaCcsICdhJywgJ2gnLCAnMicsICdlJywgJ2knLCAneScsICc0JywgJ3EnLCAndScsICdhJywgJ2MnLCAnaCddKQppZiBrZXlfMSA9PSBrZXlfMV9jb3B5IGFuZCBrZXlfMSBpcyBrZXlfMV9jb3B5OgogICAgcHVibGljX251bWJlcnNfbGlzdCA9IFtzZWNyZXRfbnVtYmVyc19saXN0ICogMTAwMjI4IGZvciB4eHggaW4gcmFuZ2UoOTk3MyldCnNlY3JldF9udW1iZXIgPSAzNyAqIDg0NiArIHB1YmxpY19udW1iZXJzX2xpc3RbLTFdWzJdIF4gMzEzMzcKd2hpbGUgaSA8IHNlY3JldF9udW1iZXI6CiAgICBzb21ldGhpbmcgPSBiYXNlNjQuYjY0ZGVjb2RlKHNvbWV0aGluZykKICAgIGkgKz0gMQoKIyBObyBlcnJvcnMgaGVyZS4gSnVzdCBydW4gdG8gZ2V0IHRoZSBmbGFnIQpjb2RlID0gc29tZXRoaW5nCiNldmFsKGNvZGUpCg==aW1wb3J0IGJhc2U2NAoKc29tZXRoaW5nID0gIiIKd2l0aCBvcGVuKCJhYnJhY2FkYWJyYS5zdHJhbmdlIikgYXMgY'

def funny_converting(s):
    locals_, globals_ =  {"s": s}, {"s": s + 128}
    locals_, globals_ = globals_. locals_
    globals_["s"] -= 14; locals_["s"] -= 128
    exec(base64.b64decode(b'CnByaW50KCJJdCB3YXMgZGFuZ2Vyb3VzISIpCnJlc3VsdCA9IFtdCndoaWxlIHM6CiAgICByZXN1bHQuYXBwZW5kKGNocihzICUgMTI4KSkKICAgIHMgPj49IDcKcmVzdWx0ID0gaW50KCcnLmpvaW4ocmV2ZXJzZWQocmVzdWx0KSkpCg=='), globals_, locals_)
    return locals_["result"]

def recursive_hell(m,n):
     increasing_sequence = 1, 2, 3, 4, 5, 6, 7, 8, 9, 1337
     if sorted(increasing_sequence) == increasing_sequence:
         print(base64.b64decode(b"QWNrZXJtYW5u"))
     if m == 0:
          return (n + 1)
     elif n == 0:
          return recursive_hell(m - 1, 1)
     else:
          return recursive_hell(m - 1, recursive_hell(m, n - 1))

def russian_roulette(bullet = ""):
    from random import randint
    __import__('sys').setrecursionlimit(randint(37, 31337))
    x, y = 37, 3l337
    x, y == y, x
    secret = recursive_hell(randint(1, 12),randint(1, 12))
    return secret

def run_it(): # If you can
    secret = russian_roulette()
    if secret != recursive_hell(funny_converting(51), funny_converting(6320)):
        return "Bad..."
    x = fowl[0 : len(fowl) - secret + 81 * 100]
    y = fowl[len(fowl) - secret + 9 * 900 :]
    print("Try it!")
    lwof = y + x
    return lwof

```

снова обфусцированный файл.

если посмотреть на **fowl**, можно заметить, что это бейс64 строка, но только ее конец "**==** "

находится в середине.

Поэтому нужно переместить все что после двух равно в начало и расшифровать.



```python
# stage4.py
import base64

something = ""
with open("abracadabra.strange") as abracadabra:
    something = abracadabra.read()
i = 0
secret_numbers_list, public_numbers_list = ['n','u','l','l'], ['p','u','b','l','i','c']
secret_numbers_list = [(31337 - 2**14 - (16429 ^ 31337)) ^ 31337 for i in range(2**4096)];
secret_numbers_list = list(map(lambda x: (x * 100500) // 100 // 201 // 5 % 37, secret_numbers_list))
key_1 = "iungeeShah2eiy4quach"
key_1_copy := ''.join(['i', 'u', 'n', 'g', 'e', ' ', 'e', 'S', 'h', 'a', 'h', '2', 'e', 'i', 'y', '4', 'q', 'u', 'a', 'c', 'h'])
if key_1 == key_1_copy and key_1 is key_1_copy:
    public_numbers_list = [secret_numbers_list * 100228 for xxx in range(9973)]
secret_number = 37 * 846 + public_numbers_list[-1][2] ^ 31337
while i < secret_number:
    something = base64.b64decode(something)
    i += 1

# No errors here. Just run to get the flag!
code = something
#eval(code)

```

в файле **abracadabra.strange** лежит бейс64 строка, вот только если ее расшифровать, получится еще одна бейс64 строка. Так нужно сделать **N** раз пока не получим флаг.

как видно из кода в N - secret_number. После оптимизации, получаем число 37, выполняем b64decode 37 раз и получаем stage5.py

```python
# stage5.py
b"exec(base64.b64decode(b'CmltcG9ydCBvcwp3aGlsZSBUcnVlOgogICB3aXRoIG9wZW4oJ3B1bmlzaG1lbnQnLCAnYWInKSBhcyBwOgogICAgICAgIHAud3JpdGUob3MudXJhbmRvbSg0KSkKd2l0aCBvcGVuKCdmbGFnJywgJ3cnKSBhcyBmbGFnX2ZpbGU6CiAgICBmbGFnX2ZpbGUud3JpdGUoIkNTTVNVe21haW5fNTQ3ZTgwYzgzYjc3MDU1OWEwYWVmOWZlM2NjMzA5fSIpCg=='))"

```

после очередного b64decode:

```python
import os
while True:
   with open('punishment', 'ab') as p:
        p.write(os.urandom(4))
with open('flag', 'w') as flag_file:
    flag_file.write("CSMSU{main_547e80c83b770559a0aef9fe3cc309}")

```

Получили флаг.