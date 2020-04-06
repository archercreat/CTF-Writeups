# Mr. Game and Watch (271 solves)

> My friend is learning some wacky new  interpreted language and different hashing algorithms. He's hidden a  flag inside this program but I cant find it... He told me to connect to `challenges.auctf.com 30001` once I figured it out though. Author: nadrojisk

We are given compiled java class.

Again, we have 3 checks to pass in order to get the flag

### check 1:

```java
private static boolean crack_1(Scanner paramScanner) {
    System.out.println("Let's try some hash cracking!! I'll go easy on you the first time. The first hash we are checking is this");
    System.out.println("\t" + secret_1);
    System.out.print("Think you can crack it? If so give me the value that hashes to that!\n\t");
    String str1 = paramScanner.nextLine();
    String str2 = hash(str1, "MD5");
    return (str2.compareTo(secret_1) == 0);
}
```

googling secret_1 md5 gives first flag `masterchief`

### check 2:

```java
private static int[] decrypt(String paramString, int paramInt) {
    int[] arrayOfInt = new int[paramString.length()];
    for (byte b = 0; b < paramString.length(); b++)
        arrayOfInt[b] = paramString.charAt(b) ^ paramInt; 
    return arrayOfInt;
}

private static boolean crack_2(Scanner paramScanner) {
    System.out.println("Nice work! One down, two to go ...");
    System.out.print("This next one you don't get to see, if you aren't already digging into the class file you may wanna try that out!\n\t");
    String str = paramScanner.nextLine();
    return (hash(str, "SHA1").compareTo(decrypt(secret_2, key_2)) == 0);
}
```

After decrypting secret_2 and looking for sha1 we find second flag `princesspeach`

### check 3:

```java
private static int[] encrypt(String paramString, int paramInt) {
    int[] arrayOfInt = new int[paramString.length()];
    for (byte b = 0; b < paramString.length(); b++)
        arrayOfInt[b] = paramString.charAt(b) ^ paramInt; 
    return arrayOfInt;
}

private static boolean crack_3(Scanner paramScanner) {
    System.out.print("Nice work! Here's the last one...\n\t");
    String str1 = paramScanner.nextLine();
    String str2 = hash(str1, "SHA-256");
    int[] arrayOfInt = encrypt(str2, key_3);
    return Arrays.equals(arrayOfInt, secret_3);
}
```

`solidsnake`



```bash
$ nc  challenges.auctf.com 30001
Welcome to the Land of Interpreted Languages!
If you are used to doing compiled languages this might be a shock... but if you hate assembly this is the place to be!

Unfortunately, if you hate Java, this may suck...
Good luck!

Let's try some hash cracking!! I'll go easy on you the first time. The first hash we are checking is this
        d5c67e2fc5f5f155dff8da4bdc914f41
Think you can crack it? If so give me the value that hashes to that!
        masterchief
Nice work! One down, two to go ...
This next one you don't get to see, if you aren't already digging into the class file you may wanna try that out!
        princesspeach
Nice work! Here's the last one...
        solidsnake
That's correct!
auctf{If_u_h8_JAVA_and_@SM_try_c_sharp_2922}
^C
```



