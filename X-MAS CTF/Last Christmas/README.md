X-MAS: Lapland Mission

![2_title](images/2_title.png) 

The game is written in Unity Engine. We asked to kill all robots to get the flag, but robots instantly kill us when get in their FOV.

![2_game](images/2_game.png)

![2_death](images/2_death.png)

Solution:

In Unity, every game class is stored in "Data\Managed\Assembly-CSharp.dll". Let's open it in dnSpy.

![2_disas](images/2_disas.png)

Let's open Bot class and change Shoot method for this:

![bot](images/bot.png)

To this:

![2_patched](images/2_patched.png)

Now bots can't kill us and we can easily get the flag:)

![2_bots_cantkill](images/2_bots_cantkill.png)

![2_flag](images/2_flag.png)

