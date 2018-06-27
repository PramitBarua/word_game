# word_game
word game for fun

This is a word game software. In this present state of the code, there are 304 words in the list. 
Most of these words are for GRE test takers.

This software allows the player to add a new word, edit or delete existing words.

Every word in the list has a unique score ranging from -5 to 5. -5 means so hard to remember and
5 means easy to remember. However, this scoring was done based on my personal feeling. :P

It allows the player to play various games such as write the word from the meaning, multiple 
choice question and guessing words. The program will set the game randomly. However, the code 
is written in such a way that the writing game will pop up more frequently than other games.
-In writing game, the software will provide the meaning of the word and will ask the player to
write the corresponding word
-Multiple choice game can be two types. In the 1st type the player will be asked to pick the 
meaning of the given word and in the 2nd case, the player will be asked to pick the word for the 
given meaning. In multiple type questions, the player will get four choices to pick the answer. 
-In guessing game, the software will show a word and player will try to guess the meaning of the 
word. When the player will guess the word and press enter the program will show the actual meaning 
of the word and ask for player feedback on his/her guessing.

Based on the player performance, the program will automatically update the score of each word. If 
the score of a particular word is -5 or 5 then the score will not further decrease or increase. When
player failed to provide the correct answer, the program will deduct 1 from the correct score. 
However, to improve the score of a particular word player have to give the correct answer of that 
word twice. 

Moreover, if the word list contains 5 or more words of the score -1 then it will perform the games 
on those short-listed words. At first, the software will give a message to the player about the 
above-mentioned situation. After that, it will display those words and their corresponding meaning 
one by one. When there is no word that has a score below -1, the software will ask the player to 
start the game. If the player agrees to play then it will start showing questions about those words. 
Otherwise, it will display the words and their meaning one by one as previous.


If you have any further suggestions on how to improve the software or any bug then feel free 
to send me a message
@ pramit.barua@gmail.com 
