# Autoclicker
Autoclicker that works on Discord.

The concept was not invented by me in any way. I just wanted a small project for myself. There are a lot of bugs, like the recorder not working, etc.

TODO:

1. Fix the default key not working.
2. Fix the repeat timer so it works and you don't need to use both "Repeat Until Stop" and "Repeat for Fixed Times."
3. Fix the recorder so it actually works and does not crash.
4. Add comments to the code (so others can understand the pain in the ass that is Python).
5. Make a dark/light mode so you can switch.

Now that the boring part is over, let's get into the juicy stuff.

![image](https://github.com/user-attachments/assets/d435b6f5-f3b7-455b-a7f0-7db5533403ee)

The autoclicker works in Discord. I was testing it on a bot for autofarming buttons.

Traditional autoclickers just click, but in my code, you can see that it moves the mouse after every click so Discord sees that the mouse is moved, no matter if it's the same coordinate set by you.  
Again, you can input your coordinates by yourself or use "Pick Location," which will log your coordinates after 3 seconds.

The interval is between 50ms and 5s. It can be changed in the code. (You will find it easier when I add comments.)

# Requirements

`pip install -r requirements.txt`

**This autoclicker is provided for educational purposes only. I do not take responsibility for any illegal activities, misuse, or consequences arising from the use of this tool, including but not limited to account bans, violations of terms of service, or any legal issues that may arise from its use in online games or platforms. Users are solely responsible for their actions and should use this tool at their own risk. It is highly recommended to review and comply with the terms of service and community guidelines of any platform or game you use this with.**
