# Babycrypt

We are given with elf64 binary and notes.dat file.

The binary asks for key and text and gives out encrypted text.

The notes contains output from program with different inputs:

```
key: %key%
text: test_test_test_test_test
Encoded: 7685737a9f7895737a9f84857b769f7a657b769f78898378
         
key: %key%
text: qwertyuiopasdfgh
Encoded: 717785747885858d6f7e917364686776

key: %key%
text: skIllaoInasJjklqo19akq9k13k45k69alq1
Encoded: 7393a992708d8fad708d83aa7273707d6f3939856b7d398bb53b8b34b573b6c5618e7135
         

key: %key%
text: %flag%
Encoded: 8185748f7b3b3a3565454584b8babbb8b441323ebc8b3a86b5899283b9c2c56d64388889b781


*Note: in all three cases used one key*
```



After some reversing we can see that key is being shuffled and applied to input text. After that it prints encrypted text.

```c
void make_text(char *data)
{
  unsigned __int64 v1;
  int v2; 
  int v3; 
  int v4; 
  int i; 

  for ( i = 0; ; ++i )
  {
    v1 = i;
    if ( v1 >= text_len(data + 88) )
      break;
    v2 = *(char *)get_text(data + 88, i);
    v3 = *(_DWORD *)get_key(data, i % 16) ^ v2; // xor
    v4 = v3 + *(_DWORD *)get_key(data, i % 16); // add
    sub_55E323148EC6((__int64)(data + 112), (__int64)&v4);
  }
}
```

### Solution:

The solution is simple. since we know 3 inputs and 3 outputs, we can find all possible keys for given pairs.

After that we can find possible plaintexts for given encrypted flag.

```python
import binascii
from z3 import *
import string

outputs = {
    'test_test_test_test_test' : binascii.unhexlify('7685737a9f7895737a9f84857b769f7a657b769f78898378'),
    'qwertyuiopasdfgh' : binascii.unhexlify('717785747885858d6f7e917364686776'),
    'skIllaoInasJjklqo19akq9k13k45k69alq1' : binascii.unhexlify('7393a992708d8fad708d83aa7273707d6f3939856b7d398bb53b8b34b573b6c5618e7135')
}

mapping = {
    0:0,
    1:4,
    2:8,
    3:12,
    4:13,
    5:14,
    6:15,
    7:11,
    8:7,
    9:3,
    10:2,
    11:1,
    12:5,
    13:9,
    14:10,
    15:6
}

# apply key shuffle
def map_key(key):
    new_key = [0 for i in range(len(key))]
    for i, v in enumerate(key):
        new_key[mapping[i]] = v
    return ''.join(new_key)

# apply key shuffle reverse
def map_key_rev(key):
    new_key = [0 for i in range(len(key))]
    new_mapping = {}
    for k, v in mapping.items():
        new_mapping[v] = k
    for i, v in enumerate(key):
        new_key[new_mapping[i]] = v
    return ''.join(new_key)

# encryption
def encode_byte(inp_text, inp_key):
    return ((inp_text ^ inp_key) + inp_key) & 0xff

# helper function
def to_byte(x):
    return bytes([x])

# find all possible keys
# input  - dict{plaintext : encypted_text}
# output - all possible keys
def get_keys(outputs):
    s = Solver()
    key_len = 16
    possible_keys = []
    # make key 16 bytes long 
    # key has to be in hexdigits range
    for i in range(0, key_len):
        globals()['b%i' % i] = BitVec('b%i' % i, 8)
        s.add(Or(And(globals()['b%i' % i] >= 48, globals()['b%i' % i] <= 57), And(globals()['b%i' % i] >= 97, globals()['b%i' % i] <= 104)))
    

    for text, output in outputs.items():
        for i in range(len(text)):
            s.add(encode_byte(ord(text[i]), globals()['b%i' % (i % 16)]) == output[i])
 
    #print(s)
	# find all possible keys
    while s.check() == sat:
        model = s.model()
        block = []
        out = ''
        for i in range(key_len):
            c = globals()['b%i' % i]
            out += chr(model[c].as_long())
            block.append(c != model[c])
        s.add(Or(block))
        possible_keys.append(map_key_rev(out))
    return possible_keys


# input - keys
# output - all possible plaintext
def solve(keys):
    encoded_flag = binascii.unhexlify('8185748f7b3b3a3565454584b8babbb8b441323ebc8b3a86b5899283b9c2c56d64388889b781')
    flag_len = len(encoded_flag)
    for key in keys:
        k = map_key(key)
        s = Solver()
        # gen flag
        for i in range(0, flag_len):
            globals()['b%i' % i] = BitVec('b%i' % i, 8)
            s.add(And(globals()['b%i' % i] >= 32, globals()['b%i' % i] <= 127))

        for i in range(flag_len):
            s.add(encode_byte(globals()['b%i' % i], ord(k[i % len(k)])) == encoded_flag[i])
        if s.check() == sat:
            out = ''
            model = s.model()
            for i in range(flag_len):
                c = globals()['b%i' % i]
                out += chr(model[c].as_long())
            print(out)

if __name__ == "__main__":
    #assert 'aaaabbbbccccdddd' == map_key_rev('acccaddcaddbabbb')
    #sys.exit(main())
    keys = get_keys(outputs)
    solve(keys)
```

And we get all plaintexts

```
Aero{381a95d003629088c8f1ebc189ab6fe7}
Aero{3:1a95d003629088c:f1ebc189ab6fe7}
```

