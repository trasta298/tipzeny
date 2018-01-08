# Usages for Rinhime(りん姫), the BitZeny tipping bot on Twitter

This is the help page for Rinhime *(pronounced: `Re-in-he-may`)* , the BitZeny tipping bot on Twitter.    
Please refer below for commands.    
You can use any command by both tweeting or messaging except for `giveme`, `rainlist`, and `rainfollowerlist` command.    
For any issues about the bot (stopped, or bugs), please contact the dev's [Twitter](https://twitter.com/tra_sta).    

Translated by [nao20010128nao](https://github.com/nao20010128nao).     

**Notices:**
- Follow back won't be done for everyone.
- You need at least 5 ZNY for receiving RAIN.

## balance
### @rintips balance (any comment, optional)
Replies you the balance you have.   
**Example:** `@rintips balance`    
<img src="https://i.imgur.com/kjoqPPN.png" alt="" width="50%" height="50%">

## deposit
### @rintips deposit (any comment, optional)
Replies you deposit address.    
**Example:** `@rintips deposit`     
<img src="https://i.imgur.com/r6cxfFc.png" alt="" width="50%" height="50%">

## withdraw
### @rintips withdraw (ZNY address, required) (amount to withdraw, required)
Withdraws specified amount of BitZeny to the specified address.    
**Example:** `@rintips withdraw ZuGdQvycbE9HTfke3EPcSUQEH2joaYqXjj 10`    
<img src="https://i.imgur.com/NNqJiEu.png" alt="" width="50%" height="50%">

## withdrawall
### @rintips withdrawall (ZNY address, required)
Withdraws *all* BitZeny to the specified address.        
**Example:** `@rintips withdrawall ZuGdQvycbE9HTfke3EPcSUQEH2joaYqXjj`    
**CAUTION:** This command will withdraw **ALL** BitZeny including the last 5ZNY.

## send
### @￰rintips send (Twitter account ID starting with @, required) (amount to send, required) (any comment, optional)
Sends specified amount of BitZeny to the specified account.

## tip
### @￰rintips tip (Twitter account ID starting with @, required) (amount to tip, required) (any comment, optional)
Sends specified amount of BitZeny to the specified account.    
The receiver needs to use `balance` command within 3 days to receive.    
If the receiver didn't received your tip, it'll be sent back to your balance.    
**Example:** `@rintips tip @tra_sta 3.9 Thanks!`
**Tip:** You can donate the author by: `@￰rintips tip @￰rintips (amount to tip, required)`

## rain
### @￰rintips rain (amount to rain, required)
Delivers equally ZNYs to the users who fulfilled the following condition:
- Have deposited at least 5 ZNY.

## rainlist
Only available in the Direct Messages.    
Replies the list of users who fulfilled the condition to get rained.

## rainfollower
### @￰rintips rainfollower (amount to rain, required)
Delivers equally ZNYs to the users who fulfilled the following conditions:
- Have deposited at least 5 ZNY.
- Your follower.
**Note:** Don't abuse this, since it is a one of heavier operations.

## rainfollowerlist
Only available in the Direct Messages.    
Replies the list of users who fulfilled the condition to get rained in your follower.

## giveme
### @rintips giveme (any comment, optional)
If your account fulfills the following conditions, you can get a little ZNYs.    
- Using official client.
- Tweeted more than 100 tweets.
- 2 weeks elapsed from creation of your account.
- Your balance is 10 ZNY or less.
- 7 days elapsed from the last withdrawal.
- 24 hours elapsed from the last `giveme` command.

**Caution:** Not available in the Direct Messages, be careful.

## A hidden command only available for the New Year Day
**Caution:** The following command contains Japanese Kanjis, you may need Copy and Paste.
### @￰rintips お年玉 (Twitter account ID starting with @, required) (amount to tip, required) (any comment, optional)
You can send a New Year present.  

### @￰rintips お賽銭 (amount to tip, required) (any comment, optional)
You can make a money offering. More you make, I will be happier.  
