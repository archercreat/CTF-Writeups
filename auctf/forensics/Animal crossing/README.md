# Animal crossing

In this challenge we are given pcap file with suspicious dns requests. 

Every dns request starts with base64 string + `ad.quickbrownfoxes.org`

Solution:

Lets dump the whole string and decode it:

```python
from scapy.all import *
scapy_cap = rdpcap('animalcrossing.pcapng')
out = []
for packet in scapy_cap:
    if packet.haslayer(DNS):
        rec = packet[DNSQR].qname
        if b'ad.quickbrownfoxes.org' in rec:
            s = rec[:rec.find(b'.')]
            if s not in out:
                out.append(s)

print(''.join([i.decode() for i in out]))
```

In the end we get this:

```
Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… auctf{it_was_star_wars_all_along} He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but 
```

`auctf{it_was_star_wars_all_along}`