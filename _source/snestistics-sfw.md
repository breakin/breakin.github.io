---
layout: post
date: 2017-12-24
title: Snestistics - Super Famicon Wars English translation
tags: snes, programming, asm, snestistics
theme: snestistics
landing: index, snestistics
---
We've released a game translation using snestistics. We translated an obscure game that only existed in Japanese into English. The patch and more information can be found [here](http://www.romhacking.net/translations/3354/). I am super proud to have been part of this project and I hope that others want to use snestistics o do other projects. While I might not be as involved in those I would be happy to help out fixing bugs specific to that game.

My involvement
==============
(This text can also be found in the patch readme.txt).

"What are you working on now", David asked. I usually answer this question by describing my latest personal project that I am working on, projects that seldom amounts to anything. Like that time 5 years ago when I wrote a toolto reverse engineer 'A Link to the Past' for the Super Nintendo only to find out that someone had a already done just that. That time I just pushed my tool to github and never touched it again. This time I didn't have a personal project so I said that maybe it would be fun to do something with someone for once. I asked David to tell me everything relevant on his bucket list and he answered "secret project X and an English translation of Super Famicom Wars".

David had told me about the SFW project before - mostly around 5 years ago when he gave it up - and we even speculated if my tools could be used. I told David that I'm not touching "secret project X" with a ten-foot pole but let's do Super Famicom Wars! And so we did. At this time I had never played any games in the Wars series and I had never heard of this game before!

It turned out that my tool from 5 years ago already in its current state was almost enough to unblock David. By being able to get a really nice assembler source code of the game lessened the cognitive load of reverse engineering. When things became hard again I and David came up with new ways to simplify. Later a mode where you could list all 'functions' being called and a way to custom print function parameters unlocked was added. It was really fun using it on a game that hadn't been reverse engineered before; it felt like we were unlocking the secrets of the game, things nobody but the original developers had seen. That is the benefit of attacking an obscure game!

Then one day David simply understood the game. Reverse engineering was over. I had one major feature almost done that would have been awesome but it was never needed. In the end my tool was only there to push David over the threshold. After this I mostly cheered on, very happy that David persevered and that he managed to get other capable people involved with the actual translation.

I am continuing work on my tool at [https://github.com/breakin/snestistics](https://github.com/breakin/snestistics). It is not ready for general consumption just yet but hopefully it can help push more reverse engineers over the threshold so that they don't need the tool anymore since they now understand the game itself. I am very proud that I was part of this project that in the end actually was finished!

Snestistics
===========
I am currently cleaning up the code we used. We had a feature for which David needed to use make files to compile in things that really should live in data or as some form of plugin. To enable users who don't love building C++ projects I added support for a scripting language (squirrel). I am also working on new features. The coolest feature is the ability to get an answer to the question "why is register or memory this or that at this point". The answer is given as a .dot-file that can be rendered using graphviz into a beautiful graph. The feature is kinda half-baked but it sure is fun to come up with new ways to reduce the complexity of breaking things apart!

Snestistics can be found at [github](https://github.com/breakin/snestistics).
