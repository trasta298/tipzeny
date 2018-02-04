# りん姫 How to use

ここはりん姫(BitZeny投げ銭bot)のヘルプページです。以下で使えるコマンドを参照してください。  
また、`giveme`以外のコマンドはDMでも使うことができます。  
botが止まっていた時や質問があるときは[開発者twitter](https://twitter.com/tra_sta)まで。  
※注意  
・フォロバは気まぐれです。必ずしもされるわけではありません。  
・コマンドを使うときの空白はすべて半角にしてください。  
・`rain`を受け取るために残高は5ZNY以上残しておくことをお勧めします。    

## balance/残高
### @zenytips balance (コメント)
残高を確認できます。  
例:`@zenytips balance`  
<img src="https://i.imgur.com/kjoqPPN.png" alt="" width="50%" height="50%">  

## deposit/入金
### @zenytips deposit (コメント)
入金用アドレスを返します。  
例:`@zenytips deposit`  
<img src="https://i.imgur.com/r6cxfFc.png" alt="" width="50%" height="50%">  

## withdraw/出金
### @zenytips withdraw 受取ZNYアドレス 出金額
指定した額を出金することができます。  
例:`@zenytips withdraw EXAMPleAdDreSS 10`  
<img src="https://i.imgur.com/NNqJiEu.png" alt="" width="50%" height="50%">  

## withdrawall/全額出金
### @zenytips withdrawall 受取ZNYアドレス
りん姫にある残高すべてを出金することができます。  
例:`@zenytips withdrawall EXAMPleAdDreSS`    

## send/送金
### @￰zenytips send @￰twitterアカウント 送金額 (コメント)
指定された額のZNYを相手に送ります。    

## tip/投銭
### @￰zenytips tip @￰twitterアカウント 投銭額 (コメント)
指定された額のZNYを相手に送ります。送られた側は3日以内に`balance`をすると受け取れます。  
相手が3日以内に受け取らなかった場合、返金されます。  
例:`@zenytips tip @tra_sta 3.9 ありがとう！`  
### @￰zenytips tip @￰zenytips 投銭額
で開発者に寄付できます。サーバー維持費に使うので是非投げ銭ください。    

## rain
### @￰zenytips rain 撒銭額
条件を満たしている人に均等にZNYを送ります。  
rainを受け取れる条件は、残高5zny以上で`balance`をしていることです。    
<!--
## rainlist
DMでのみ使えます。rainを受け取る条件を満たしている人一覧を返します。    

## rainfollower
### @￰zenytips rainfollower 撒銭額
自分のフォロワーの人に限り`rain`をします。重いので連発しないでね。    

## rainfollowerlist
DMでのみ使えます。`rainfollower`を受け取る条件を満たしている人一覧を返します。    
-->
## giveme
### @zenytips giveme (コメント)
以下の条件を満たしているときにちょっとだけZNYがもらえます。また、DMではこのコマンドは使えません。  
・公式クライアントを使用していること  
・100ツイート以上であること  
・アカウントを作成してから2週間以上経過していること  
・残高10ZNY以下であること  
・最後の出金から7日以上経ってること  
・最後の`giveme`から24時間以後であること    


## 正月限定コマンド
### @￰zenytips お年玉 @￰twitterアカウント 投銭額 (コメント)
`tip`のところをお年玉に変えても使えるよーって話。  
### @￰zenytips お賽銭 投銭額 (コメント)
賽銭を投げることができます。いっぱい投げるとご利益があるかも...？あと私がうれしいので是非  
