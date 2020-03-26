# Райтап на Корейский локальный стф 2019

Все таски, которые я решал, были под андройд. Поэтому, перед тем как начать, хорошо бы было подготовить окружение для работы с андройдом.

### Тулзы, которые нам понадобятся:

[Android studio](https://developer.android.com/studio)

[Frida](https://frida.re/)

[apktool](https://ibotpeaches.github.io/Apktool/)

[jd-gui](https://java-decompiler.github.io/)

[dex2jar](https://github.com/pxb1988/dex2jar)

ida pro (ну а че)

Обязательно нужно создать эмулятор без гугл апи (чтобы был рут)

## Оглавление
1. [Missing So](##MissingSo)
2. [Sign](##Sign)
3. [LateProblem](##LateProblem)
4. [task_附件](##task_附件)


## MissingSo

Дан MissingSo.apk файл. Для начала установим его на эмулятор и запустим:

```bash
$ adb install task_MissingSo.apk
Success
```

![](https://i.imgur.com/uLEcVE1.png)

Ничего интересного, пора посмотреть что внутри.

---

### Анализ:


Используем `dex2jar`, чтобы конвертировать апк в java файл:
```bash
d2j-dex2jar MissingSo.apk
```
получаем `task_MissingSo-dex2jar.jar`. Теперь этот файл можно открыть в `jd-gui`.

Посмотрим MainActivity:

```java
public class MainActivity extends AppCompatActivity {
  private Button btn;
  
  private EditText input;
  
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(2131361820);
    Button button = (Button)findViewById(2131165250);
    this.btn = button;
    button.setOnClickListener(new View.OnClickListener() {
          public void onClick(View param1View) {
            MainActivity mainActivity = MainActivity.this;
            if (mainActivity.stringFromJNI(mainActivity.input.getText().toString()) == 0) {
              MainActivity.this.btn.setText("K.O");
            } else {
              MainActivity.this.btn.setText("FAIL");
            } 
          }
        });
    try {
      File file1 = getFilesDir();
      File file3 = new File();
      StringBuilder stringBuilder2 = new StringBuilder();
      this();
      stringBuilder2.append(file1.getAbsolutePath());
      stringBuilder2.append(File.separator);
      stringBuilder2.append("libdec.so");
      this(stringBuilder2.toString());
      if (file3.exists())
        file3.delete(); 
      File file4 = new File();
      StringBuilder stringBuilder1 = new StringBuilder();
      this();
      stringBuilder1.append(file1.getAbsolutePath());
      stringBuilder1.append("//..//lib//librcnb.so");
      this(stringBuilder1.toString());
      File file2 = new File();
      StringBuilder stringBuilder3 = new StringBuilder();
      this();
      stringBuilder3.append(file1.getAbsolutePath());
      stringBuilder3.append(File.separator);
      stringBuilder3.append("libdec.so");
      this(stringBuilder3.toString());
      if (!file4.exists()) {
        stherror();
        return;
      } 
      FileInputStream fileInputStream = new FileInputStream();
      this(file4);
      FileOutputStream fileOutputStream = new FileOutputStream();
      this(file2);
      int i = fileInputStream.read();
      while (true) {
        fileOutputStream.write((i ^ 0x39) + 119 & 0xFF);
        int j = fileInputStream.read();
        i = j;
        if (j == -1) {
          fileOutputStream.close();
          StringBuilder stringBuilder = new StringBuilder();
          this();
          stringBuilder.append(file1.getAbsolutePath());
          stringBuilder.append(File.separator);
          stringBuilder.append("libdec.so");
          System.load(stringBuilder.toString());
          file2.delete();
          TextView textView = (TextView)findViewById(2131165312);
          this.input = (EditText)findViewById(2131165268);
          return;
        } 
      } 
    } catch (Exception exception) {
      stherror();
      return;
    } 
  }
  
  public void stherror() {
    ((TextView)findViewById(2131165312)).setText("Something Error.");
  }
  
  public native int stringFromJNI(String paramString);
}
```


Метод `OnCreate` вызывается тогда, когда мы запускаем приложение. Что в нем происходит?

Сначала создается `Listener`для кнопки, который описывает что делать при ее нажатии. В данном случае берется текст из поля и посылается в `stringFromJNI` функцию.
Если глянуть в самый конец `public native int stringFromJNI(String paramString);` - нативная функция.

После чего в `try` `catch` расшифровывается и подгружается нативная библиотека `librcnb.so`.

Давайте посмотрим, что это за библиотека. Используем `apktool`, чтобы разархивировать апк файл на его составляющие:

```bash
apktool d -r task_MissingSo.apk
I: Using Apktool 2.4.0-dirty on task_MissingSo.apk
I: Copying raw resources...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
```

Теперь в папке `task_MissingSo/lib/` можно найти папку `x86/` и `armeabi-v7a/` с одной и той же либой.
Что это значит? 

Это сделано для того, чтобы приложение запустилось на устройствах разных архитектур. Java не зависит от архитектуры, но нативные библиотеки зависят. 

Я взял `x86/librcn.so` т.к. знаком с x86 архитектурой больше.


Расшифруем библиотеку как описано в коде выше:

```python
enc = open('librcnb.so', 'rb').read()
out = open('libdec.so', 'wb')

for i in enc:
    c = (((i ^ 0x39) + 119)  & 0xff).to_bytes(1, byteorder='big')
    out.write(c)
```

Теперь откроем в иде и посмотрим. Нам интересна функция `stringFromJNI`

Из java кода выше известно, что в функцию подается введенный нами текст и возвращается bool.

```c++
bool __cdecl Java_com_zxc_missingso_MainActivity_stringFromJNI(JNIEnv *a1, jobject a2, jstring a3)
{
  char *v3; // eax
  char *str; // esi
  int len; // edi
  int v7; // eax
  char *v8; // eax
  unsigned __int8 v9; // cl
  unsigned int v10; // edx
  int *v11; // ecx
  char v12; // cl
  unsigned int v13; // edx
  char v15; // [esp+0h] [ebp-FBCh]
  unsigned __int8 v16; // [esp+1h] [ebp-FBBh]
  void *v17; // [esp+4h] [ebp-FB8h]
  char out[4020]; // [esp+8h] [ebp-FB4h]

  v17 = &_stack_chk_guard;
  v3 = (*a1)->GetStringUTFChars(a1, a3, 0); // перевод в сишный массив
  str = v3;
  len = -1;
  while ( v3[++len] != 0 )  // подсчет длины строки
    ;
  memset(out, 0, 0xFA0u); 
  v15 = 0;
  rcnb_encode_block(str, len, out, &v15); // зашифровать?
  v8 = &out[4 * v7];
  if ( v15 )
  {
    v9 = v16;
    if ( (v16 & 0x80u) != 0 )
    {
      v12 = v16 & 0x7F;
      v13 = (v16 & 0x7Fu) / 0xA;
      *v8 = dword_1618[v13];
      v11 = &dword_1654[(v12 - 10 * v13)];
    }
    else
    {
      v10 = v16 / 0xFu;
      *v8 = dword_15A0[v10];
      v11 = &dword_15DC[(v9 - 15 * v10)];
    }
    *(v8 + 1) = *v11;
    v8 += 8;
  }
  *v8 = 0;
  return wcscmp(out, &byte_167C); // сравниваем зашифрованные данные
                                  // с каким-то массивом
}
```

Что тут происходит? 

Сначала наша строка из `jstring` конвертируется в сишный `char` массив, после чего вызывается `rcnb_encode_block` и в самом конце просходит сравнение с уже имеющимся массивом.

И тут появляется проблема: функция `rcnb_encode_block` зашифрована. (вообще, начиная с 0x1040 по 0x1790 все зашифровано)

Если глянуть на экспортируемые функции, то почти все они находятся в зашифрованном регионе:

![](https://i.imgur.com/zg7UcZM.png)

Можно предположить, что авторы хотели чтобы мы сдампили код из памяти. 

Для сведения: в функции `.ini_proc` происходит расшифровка этого региона памяти, но для меня было проще сдампить его.

### Отладка:


Для отладки установим и запустим android_x86_server из папки ida pro на эмулятор.

```bash
adb push android_x86_server /data/data/
adb shell "chmod 775 /data/data/android_x86_server"
adb forward tcp:23946 tcp:23946
adb shell "./data/data/android_x86_server &"
IDA Android x86 32-bit remote debug server(ST) v1.25. Hex-Rays (c) 2004-2019
Listening on 0.0.0.0:23946...

```

После этого в Иде выберем `Remote Linux debugger`, В `Debugger -> process options..` выберем 

host: 127.0.0.1

port: 23946

Теперь, нажав `Debugger -> Attach to process..` нам выведется список всех процессов на нашем андройд эмуляторе.

Выберем из списка `com.zxc.missingso` и подключимся к нему.


Найдем из списка модулей нашу библиотеку:

![](https://i.imgur.com/Mh0AXQz.png)

Найдем в памяти нужный регион и сдампим на диск

```python
from idaapi import *
raw = get_many_bytes(0xCE1D8040, 0x750)
open('raw','wb').write(raw)
```

Теперь откроем заново либу в иде и пропатчим:

```python
from idaapi import *
addr = 0x1040
raw  = open('raw','rb').read()
for i, v in enumerate(raw):
  PatchByte(addr + i, v)
```

### Решение:

Нужно загуглить имя функции `rcnb_encode_blockend`. Наткнемся на вот такой [репозиторий](https://github.com/rcnbapp/librcnb). Оказывается, это опенсорсная библиотека для кодировки в rcnb (кэп).

То есть наша введеная строка кодируется в rcnb и сравнивается с уже имеющейся последовательностью. Все, что нужно - раскодировать обратно. 

Для этого дампим флаг в файл, открываем как utf-16, запихиваем в декодер и получаем флаг.

```python
flag = open('flag', 'rb').read()
print(flag.decode('utf-16'))
```

`ȑcÑƄřĊŇÞɍcÑþŗċÑƄȑÇǸþŗȼňƀȑÇƝÞɌĉŇBȓƈǸßɌĆnBȓčǸƃŗċŇßȐcņƁȐcņƁȑÇÑƀřčȠbřČňB`

```c++
#include <rcnb/cdecode.h>
#include <rcnb/cencode.h>

#include <assert.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

/* arbitrary buffer size */
#define SIZE 512

int main()
{
    wchar_t* encoded = L"ȑcÑƄřĊŇÞɍcÑþŗċÑƄȑÇǸþŗȼňƀȑÇƝÞɌĉŇBȓƈǸßɌĆnBȓčǸƃŗċŇßȐcņƁȐcņƁȑÇÑƀřčȠbřČňB";
    char* decoded = malloc(SIZE);

    setlocale(LC_ALL, "");

    /* decode the data */
    ptrdiff_t res = rcnb_decode(encoded, wcslen(encoded), decoded);
    if (res < 0)
        wprintf(L"decode failed\n");
    printf("decoded: %s\n", decoded);

    free(decoded);
    return 0;
}
```

```bash
./decode
decoded: XMAN{y0u_c4n_Dump_soo00OOOOO_RCNB}
```



## Sign

Повторяем все теже действия, что и с предыдущем файлом.


![](https://i.imgur.com/M0YtYPc.png)

### Анализ:

MainActivity:
```Java
package com.example.sign;

import android.content.Context;
import android.content.pm.PackageInfo;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MainActivity extends AppCompatActivity {
  static {
    System.loadLibrary("native-lib");
  }
  
  public static String SHA(byte[] paramArrayOfbyte) {
    try {
      MessageDigest messageDigest = MessageDigest.getInstance("SHA-512");
      messageDigest.update(paramArrayOfbyte);
      paramArrayOfbyte = messageDigest.digest();
      StringBuffer stringBuffer = new StringBuffer();
      this();
      for (byte b = 0; b < paramArrayOfbyte.length; b++) {
        String str = Integer.toHexString(paramArrayOfbyte[b] & 0xFF);
        if (str.length() < 2)
          stringBuffer.append(0); 
        stringBuffer.append(str);
      } 
      return stringBuffer.toString();
    } catch (NoSuchAlgorithmException noSuchAlgorithmException) {
      noSuchAlgorithmException.printStackTrace();
      return "";
    } 
  }
  
  public native boolean en(String paramString);
  
  public String getSign() {
    for (PackageInfo packageInfo : getPackageManager().getInstalledPackages(64)) {
      if (!packageInfo.packageName.equals(getPackageName()))
        continue; 
      return SHA(packageInfo.signatures[0].toByteArray());
    } 
    return "";
  }
  
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(2131361820);
    final EditText et2 = (EditText)findViewById(2131165270);
    getSign();
    Button button = (Button)findViewById(2131165250);
    Toast toast = Toast.makeText((Context)this, null, 0);
    toast.setText("Sign is flag1!");
    toast.show();
    button.setOnClickListener(new View.OnClickListener() {
          public void onClick(View param1View) {
            if (MainActivity.this.en(et2.getText().toString())) {
              Toast toast = Toast.makeText((Context)MainActivity.this, null, 0);
              toast.setText("flag2 is correctis XMAN{flag2 + flag1}");
              toast.show();
            } else {
              Toast toast = Toast.makeText((Context)MainActivity.this, null, 0);
              toast.setText("Try again!");
              toast.show();
            } 
          }
        });
  }
}
```


Опять, мы имеем одну нативную функцию `public native boolean en(String paramString);` + функцию `public String getSign()`, которая возвращает sha512 от сигнатуры данного приложения.

Для решения этого таска, нужно получить 10 первых байт хэша, который возвращает `getSign()` и чтобы функция `en(paramstring)`  вернула True.

Проблема в том, что функция `getSign` не выводится на экран, поэтому получить хэш так просто не получится.

### Первый флаг:

Для начала давайте посмотрим на функцию `en(paramstring)`. Так же, с помощью `apktool`, достаем либу и открываем в иде:

```c++
jdouble __cdecl Java_com_example_sign_MainActivity_en(JNIEnv *env, jobject obj, jstring str)
{
  const char *input; // edi
  jsize inp_len; // ecx
  int i; // eax
  char *val; // edi
  char c; // dl
  char v8; // si
  unsigned __int8 v9; // cl
  char v10; // dl
  const char *v11; // edi
  const char *inp; // [esp+4h] [ebp-28h]
  int v13; // [esp+Ch] [ebp-20h]
  char out[12]; // [esp+17h] [ebp-15h]

  *(_DWORD *)&out[1] = __readgsdword(0x14u);
  input = (*env)->GetStringUTFChars(env, str, 0);
  inp_len = (*env)->GetStringUTFLength(env, str);
  if ( input && inp_len == 11 )
  {
    __android_log_print(4, "src:", "%s", input);
    (*env)->ReleaseStringUTFChars(env, str, input);
    inp = input;
    __android_log_print(4, "src:", "%s", input);
    i = -11;
    val = &vals;
    do
    {
      c = inp[i + 11];
      v8 = c - 32;
      if ( (unsigned __int8)(inp[i + 11] - 97) >= 0x1Au )
        v8 = inp[i + 11];
      v9 = c - 65;
      v10 = c + 32;
      if ( v9 >= 0x1Au )
        v10 = v8;
      out[i] = *val ^ ((v10 ^ 0x28) + 66);
      val += 4;
      ++i;
    }
    while ( i );
    out[0] = 0;
    v11 = (const char *)malloc(0xDu);
    __strncpy_chk2(v11, &v13, 12, 13, 12);
    (*env)->ReleaseStringUTFChars(env, str, inp);
    __android_log_print(4, "src:", "%s", "777");
    if ( !strcmp(v11, cmp) )
      puts("this is flag2");
  }
}
```

Наша строка конвертится в сишный массив, сверяется его длина с 11 и если это так, массив кодируется и сверяется с уже имеющимся.

### Решение:

Достаточно простого брутфорса, чтобы получить первый флаг:

```python
flag = '7@Lpz::tZpc'
vals = [0xa4, 0xc9, 0xd3, 0xc9, 0xf1, 0xa6, 0xb5, 0xcd, 0xd4, 0xf6, 0xda]

if __name__ == "__main__":
    out = ''
    for i in range(len(flag)):
        for j in range(126):
            v8 = (j - 32) & 0xff
            if (j - 97) & 0xff >= 0xa1:
                v8 = j
            v9  = (j - 65) & 0xff
            v10 = j + 32
            if v9 >= 0x1a:
                v10 = v8
            if vals[i] ^ ((v10 ^ 0x28) + 66) & 0xff == ord(flag[i]):
                out += chr(j)
                break
    print(out)
```

получаем `YOU_ARE_DL_`

---

### Второй флаг:

Для получения второго флага, нам понадобится `frida`. Мы установим хук на функции `getSign()` и выпишем то, что она вернет.

Установим фриду как написано в документации:

```bash
$ adb root # might be required
$ adb push frida-server /data/local/tmp/
$ adb shell "chmod 755 /data/local/tmp/frida-server"
$ adb shell "/data/local/tmp/frida-server &"
```

Для проверки работоспособности можно чекнуть работающие процессы командой `frida-ps -U`

### Решение:

Пишем скрипт, который будет хукать нужную нам функцию:

```python
import frida
import sys
import time

package_name = "com.example.sign"
# com.example.sign.MainActivity.getSign()
device = frida.get_usb_device()

pid = device.spawn([package_name])
print(f"{package_name} pid {pid}")

session = device.attach(pid)
time.sleep(1)

script = session.create_script(open('hook.js').read())

script.load()
device.resume(pid)

sys.stdin.read()
```

hook.js:

```javascript
console.log("Script loaded successfully ");
Java.perform(function x(){
    console.log("Inside java perform function");
    var MainActivity = Java.use("com.example.sign.MainActivity");
    console.log("got main class: " + MainActivity);
    MainActivity.getSign.implementation = function() {
        var ret = this.getSign();
        console.log(ret);
        return ret;
    }
});
```

```bash
python3 getSign.py
com.example.sign pid 3863
Script loaded successfully
Inside java perform function
got main class: <class: com.example.sign.MainActivity>
5216ccb62004c4534f35c780ad7c582f4ee528371e27d4151f0553325de9ccbe6b34ec4233f5f640703581053abfea303977272d17958704d89b7711292a4569
```

Полный флаг:
`XMAN{YOU_ARE_DL_5216ccb620}`




## LateProblem
 

![](https://i.imgur.com/zfG2Alm.png)

QR по центру дает вот такую строчку: `wxp://f2f0brA0Dbv82AsUilS0kWWIEYkLgcavi4tq`

Быстрый гугл показал, что это WeChat paymant link. К сожалению, ставить и проверять у меня желания не было.

MainActivity:
```Java
package com.nvshifu.lateproblem;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
  private Button button;
  
  private EditText p4ssw0rd;
  
  static {
    System.loadLibrary("native-lib");
  }
  
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(2131361820);
    this.button = (Button)findViewById(2131165250);
    this.p4ssw0rd = (EditText)findViewById(2131165268);
    this.button.setOnClickListener(new View.OnClickListener() {
          public void onClick(View param1View) {
            String str2 = MainActivity.this.p4ssw0rd.getText().toString();
            String str1 = str2;
            if (str2.isEmpty())
              str1 = " "; 
            str2 = str1.substring(0, 3);
            str2 = MainActivity.this.stringFromJNI(str2);
            if (EasyASR.cmp(str1)) {
              Intent intent = new Intent((Context)MainActivity.this, SecretActivity.class);
              long l = 28218679168L + Long.valueOf(str2).longValue() * 4444L + 24L;
              int i = (int)(l / 1000L);
              intent.putExtra("x", (int)(l % 1000L));
              intent.putExtra("x", i);
              MainActivity.this.startActivity(intent);
            } 
          }
        });
  }
  
  public native String stringFromJNI(String paramString);
}
```

EasyASR модуль:

```Java
package com.nvshifu.lateproblem;

import java.math.BigInteger;

public class EasyASR {
  public BigInteger modulus = new BigInteger("184258096150479708613688154800847599263475725929486952648");
  
  public BigInteger privateKey = this.publicKey.modInverse(this.modulus);
  
  public BigInteger publicKey = new BigInteger("65537");
  
  public static boolean cmp(String paramString) {
    EasyASR easyASR = new EasyASR();
    System.out.println(easyASR);
    return easyASR.encrypt(new BigInteger(str2digit(paramString))).toString()
            .equals("19626040674394963692548286065610770947714774476466545128");
  }
  
  static String str2digit(String paramString) {
    char[] arrayOfChar = paramString.toCharArray();
    int i = arrayOfChar.length;
    String str = "";
    for (byte b = 0; b < i; b++) {
      paramString = String.valueOf(arrayOfChar[b]);
      int j = paramString.length();
      if (j != 1) {
        if (j == 2) {
          StringBuilder stringBuilder1 = new StringBuilder();
          stringBuilder1.append("0");
          stringBuilder1.append(paramString);
          paramString = stringBuilder1.toString();
        } 
      } else {
        StringBuilder stringBuilder1 = new StringBuilder();
        stringBuilder1.append("00");
        stringBuilder1.append(paramString);
        paramString = stringBuilder1.toString();
      } 
      StringBuilder stringBuilder = new StringBuilder();
      stringBuilder.append(str);
      stringBuilder.append(paramString);
      str = stringBuilder.toString();
    } 
    return str;
  }
  
  BigInteger encrypt(BigInteger paramBigInteger) {
    return paramBigInteger.modPow(this.publicKey, this.modulus);
  }
}
```

Если EasyASR.cmp возвращает true, то нам открывается секретное окошко.

В EasyASR происходит рса шифрование (кэп).

Дано:

`e = 65537`

`c = 19626040674394963692548286065610770947714774476466545128`

`n = 184258096150479708613688154800847599263475725929486952648`


К счастью для нас, [factordb](http://www.factordb.com/index.php?query=184258096150479708613688154800847599263475725929486952648) уже имеет разложение `n`:

`2 · 2 · 2 · 7 · 71 · 709 · 7879 · 26263 · 98779 · 56471276761 · 5590885573657 · 10128513203167`

Из него легко находим phi:

```python
seq = [2, 2, 2, 7, 71, 709, 7879, 26263, 98779, 56471276761, 5590885573657, 10128513203167]
phi = 1
for i in seq:
    phi *= (i - 1)
print(phi)
```

`phi = 19433027235364321076184992986153357598109532153677004800`

Теперь найдем приватный ключ:

```python
import sympy
phi = 19433027235364321076184992986153357598109532153677004800
e = 65537
print(sympy.mod_inverse(e, phi))
```

`d = 16782732021520442018874748890295464954077870674061443073`

Можно сделать проверку:

```python
n = 184258096150479708613688154800847599263475725929486952648
e = 65537
c = 19626040674394963692548286065610770947714774476466545128
phi = 19433027235364321076184992986153357598109532153677004800
d = 16782732021520442018874748890295464954077870674061443073

# decrypt
m = pow(c, d, n)

# reencrypt
assert pow(m, e, n) == c
```

Ключ вальдный, вот только расшифрованное сообщение содержит кучу невальдных символов: `b'Z,\xf2\xa3\x0f\x9c\xe9\xfc53%^}\xbcl!D\r\xd8\xf9isK\x00'`

Невалидный ключ не мешает вызвать секретное окошко. С помощью фриды хукаем EasyASR.cmp функцию и возвращаем true.

```javascript
Java.perform(function(x) {
    var EasyASR = Java.use("com.nvshifu.lateproblem.EasyASR");
    EasyASR.cmp.implementation = function(y) {
        return true;
    }
});
```

Нам открывается окно с еще одним QR кодом.

![](https://i.imgur.com/U3jfUQk.png)

В QR коде лежит base64 строчка, которая при расшифровки дает непонятно что.. `b'\\\x18V\x05\x10\x1f+@g\xd4\xa1\xea\x95\x16I\xb7\x92j\xc8\xe5\xb29'`


### Решение:

В java файле присутствует еще один класс `DrawView.class`, но который нигде не вызывается..

В нем, в методе `OnCreate`, рисуется какая-то картинка:

```Java
protected void onDraw(Canvas paramCanvas) {
    super.onDraw(paramCanvas);
    Paint paint = new Paint();
    paint.setAntiAlias(true);
    paint.setStyle(Paint.Style.STROKE);
    paint.setColor(-16777216);
    paint.setStrokeWidth(3.0F);
    Path path = new Path();
    int i = b;
    int j = h;
    int k = a;
    int m = w;
    int n = m * 1 / 2;
    float f1 = (k + 0);
    float f2 = (j + i);
    path.moveTo(f1, f2);
    f1 = (k + m);
    path.lineTo(f1, (i + 0));
    path.moveTo(a, b);
    path.lineTo(f1, f2);
    paramCanvas.drawPath(path, paint);
    change();
    path.moveTo(a, j);
    path.moveTo(a, (b + h));
    path.moveTo((a + w * 1 / 4), (b + h * 1 / 2));
    path.moveTo(y, (b + h));
    path.moveTo((a + w * 1 / 4), (b + h * 1 / 2));
    path.moveTo(a, b);
    path.moveTo(a, b);
    path.moveTo(x, j);
    i = x;
    ...
    ...
```

Сначала я создал пустой проект, скопировал в него этот класс и запустил, но ничего не появилось..

После этого я вспомнил, что в `MainActivity` в секретную активити с qr кодом подается 2 значения:

```Java
Intent intent = new Intent((Context)MainActivity.this, SecretActivity.class);
long l = 28218679168L + Long.valueOf(str2).longValue() * 4444L + 24L;
int i = (int)(l / 1000L);
intent.putExtra("x", (int)(l % 1000L));
intent.putExtra("x", i);
MainActivity.this.startActivity(intent);
```

Где `str2` - строка, которую вернула нативная функция. 

Все, что я сделал - выставил значение `str2 = 0` и вызвал окно, на котором рисуется картинка:

```Java
import com.example.test.DrawView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        long str2 = 0;
        long l = 28218679168L + str2 * 4444L + 24L;
        int i = (int)(l / 1000L);
        DrawView topkek = new DrawView(this);
        topkek.view_init(i, (int)(l % 1000L) );
        setContentView(topkek);
    }
}
```

И получил флаг:


![](https://i.imgur.com/UaXOzB2.png)


Очень непонятный таск ¯\\_(ツ)_/¯



## task_附件

В этом таске нам дано 2 файла: 40Мб приложение и запароленный архив.

Приложение представляет собой frida-server с gui интерфейсом (это объясняет почему такой большой размер файла)

![](https://i.imgur.com/KlwVMX4.png)

Открыв в `jd-gui` можно заметить в `com.wrlus.fridahooker.flag.flag.class`

```Java
package com.wrlus.fridahooker.flag;

import android.content.Context;
import android.content.res.AssetManager;
import android.util.Log;
import java.io.IOException;
import java.io.InputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import org.bouncycastle.util.encoders.Hex;

public class Flag {
  private static final String TAG = "Flag";
  
  private Context context;
  
  public Flag(Context paramContext) {
    this.context = paramContext;
  }
  
  public static String s(InputStream paramInputStream, String paramString) {
    try {
      MessageDigest messageDigest = MessageDigest.getInstance(paramString);
      byte[] arrayOfByte = new byte[4096];
      while (true) {
        int i = paramInputStream.read(arrayOfByte);
        if (-1 != i) {
          messageDigest.update(arrayOfByte, 0, i);
          continue;
        } 
        return Hex.toHexString(messageDigest.digest());
      } 
    } catch (NoSuchAlgorithmException noSuchAlgorithmException) {
    
    } catch (IOException iOException) {}
    iOException.printStackTrace();
    return "";
  }
  
  public boolean c() {
    AssetManager assetManager = this.context.getAssets();
    try {
      InputStream inputStream1 = assetManager.open("1");
      InputStream inputStream2 = assetManager.open("2");
      String str2 = s(inputStream1, "SHA-1").toUpperCase();
      String str3 = s(inputStream2, "SHA-1").toUpperCase();
      inputStream1.close();
      inputStream2.close();
      inputStream1 = assetManager.open("1");
      inputStream2 = assetManager.open("2");
      String str4 = s(inputStream1, "SHA-256").toUpperCase();
      String str1 = s(inputStream2, "SHA-256").toUpperCase();
      inputStream1.close();
      inputStream2.close();
      Log.v("Flag", str2);
      Log.v("Flag", str3);
      Log.v("Flag", str4);
      Log.v("Flag", str1);
      if (str2.equals(str3) && !str4.equals(str1)) {
        StringBuilder stringBuilder = new StringBuilder();
        this();
        stringBuilder.append("Password is ");
        stringBuilder.append(str1);
        Log.v("Flag", stringBuilder.toString());
        return true;
      } 
    } catch (IOException iOException) {
      iOException.printStackTrace();
    } 
    return false;
  }
  
  public String f() {
    return "XMAN{InvalidFlag}";
  }
}
```

Что тут происходит? В функции `public boolean c()` из ассетов достается два файла

```Java
InputStream inputStream1 = assetManager.open("1");
InputStream inputStream2 = assetManager.open("2");
```

Вычисляются их `SHA-1` и `SHA-256` хэши и если SHA-1 хэши совпадают, но SHA-256 хэши не совпадают, то принтится строчка `Password is str1`, где str1 - SHA-256 второго ассета.

Давайте глянем, что это за файлы.

С помощью apktool'а открываем папку с ассетами и видим 2 файла:

1 - pdf архив

2 - текст

![](https://i.imgur.com/5AoNLsx.png)

Контент второго файла: `Please find the suitable file and replace me !`

Очевидно, что нужно найти SHA-1 коллизию 1 файла.

Идем на shattered.it и видим в примерах 2 пдфки: точно такую же пдфку как первая и немного измененную вторую.

Скачиваем вторую и сверяем хэши:

```bash
sha1sum 1 2
38762cf7f55934b34d179ae6a4c80cadccbb7f0a  1
38762cf7f55934b34d179ae6a4c80cadccbb7f0a  2

sha256sum 1 2
2bb787a73e37352f92383abe7e2902936d1059ad9f1ba6daaa9c1e58ee6970d0  1
d4488775d29bdef7993367d541064dbdda50d383f89f0aa13a6ff2e0894ba5ff  2
```

Как я говорил выше, sha256 должен являться паролем от архива.

Пробуем - подходит.

В архиве лежит `frida.pcapng`, можно предположить что это траффик между frida-server'ом и клиентом.

![](https://i.imgur.com/04lwZA7.png)


Не разбирая пакеты, можно сделать `strings` на файл и встретить вот такую строчку:

```
    Java.perform(function() {
        var Flag = Java.use('com.wrlus.fridahooker.flag.Flag')
        Flag.f.implementation = function () {
            sendp('Get real flag')
            return '\x58\x4d\x41\x4e\x7b\x37\x38\x38\x61\x33\x65\x63\x61\x34\x35\x35\x61\x39\x34\x62\x31\x36\x36\x31\x63\x61\x61\x62\x66\x64\x33\x37\x30\x35\x66\x66\x63\x39\x62\x33\x30\x34\x64\x64\x64\x62\x37\x35\x35\x66\x62\x30\x38\x65\x36\x33\x63\x65\x39\x38\x31\x66\x39\x37\x36\x33\x37\x30\x34\x7d'
```

Переведя из байтмассива, получаем флаг:

`XMAN{788a3eca455a94b1661caabfd3705ffc9b304dddb755fb08e63ce981f9763704}`

На этом всё :)