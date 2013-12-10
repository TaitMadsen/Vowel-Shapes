Vowel-Shapes
============
On September 30, 2013 Professor Ciesinski was a guest lecturer for our Computer Science class
 - Human Computer Interaction. She provided us with a variety of challenges that face singers.
 From those challenges we selected the "learning of vowels" as a project. Our challenge is to
 try to understand the singer's world through observation, interviews and surveys of real
 students and instructors. You - the students and staff of the Eastman School of Music.
 From these sessions we are trying to develop and application to assist with the practice of vowels.

Vowel Shapes, is a computer application written in Python that will run on Windows computers.
Vowel Shapes is intended for (but not limited to) use by students and teachers of vocal music.
The application will utilize the computer's microphone or one that is externally linked. Using
input from the microphone while the user vocalizes, the application will create a real-time visual
representation of the vowel being produced. This representation will be a graph, oval, or triangle
as the user prefers. The real power of this application comes in its ability to save previously
produced vowels, so the user may listen to and view them as the he or she attempts to replicate
the correct vowel sound. This enables teachers and the community to set exacting benchmarks for
students to achieve and master.

VowelShapes requires a configuration file - vowelShapeConfig.txt - with the following characteristics:

line 1 - string - type of vizualisation: Triangle, Oval, Graph

line 2 - string - mode to startup in: Practice, Study, Mentor

line 3 - string$list - default vowel to load - this defined as character and formant set ["i"]$[[f1, f2, f3]]

line 4 - numeric - default setting for the moving average window for normalized formant calculation

line 5 - numeric - defatul tolerance for "matching" a vowel

