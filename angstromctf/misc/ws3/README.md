# ws3 (211 solves)

> What the... record.pcapng
>
> Author: JoshDaBosh

We can clearly see that some github transmission is going on. Looking at the packets we can notice packets starting with **PACK** magic bytes. This is a github commit archive.



Solution:

In wireshark -> File -> Export objects -> save all.

```bash
binwalk -e *
```



Next, we use binwalk to extract every archive. The largest extracted file is png image.

![678](images/678.jpg)



