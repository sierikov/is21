# IS - 21
![IS 21 poster](./public/poster.png)


## Description
Pack of Python cli tools. The pack contain following algorithms: 
[Levenshtein distance][ld], [Dice coeficient][dice], [Hidden Markov models][hmm] and Logic.

[ld]: https://en.wikipedia.org/wiki/Levenshtein_distance
[hmm]: https://en.wikipedia.org/wiki/Hidden_Markov_model
[dice]: https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient


## Installation

Requirements to run: 
- `python3.8`
- `pip3`
- `virtualenv` - optional, see instructions below

You will need install dependencies with `pip3 install -r requirements.txt` after you clone the repo. 

Usage - `python3 is21.py --help`. For more detailed instructions see section *Usage* below.

```text
Usage: is21.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  arg   Checks if given arguments contains rebuts, attacks or defeats
  dice  Calculates Dice coefficient for given WORDs
  hmm   Creates Markov model for given data
  lev   Calculates Levenshtein distance between first and second WORDs
```

### Instalation with `venv`

Clone the repository and open it with a command line, then follow these steps:

1. Create `venv` in the root folder of the project with following command:
```
python3 -m venv venv
```
2. Activate the `venv`:
```
source venv/bin/activate
```
3. Install the requirements:
```
pip3 install -r requirements.txt
```
Done. To exit `venv` use `deactivate`.

## Usage
By default all commands provide only anwser. To see more details use `-v` or `--verbose` command.

### Levenshtein distance

By default all commands in Levenshtein uses `greedy` option. If you want to calculate optimum use `-o` or `--optimum` flag.

> Note: Calculation of optium is not optimised, so can be slow for very long wods.

#### Basic distance
Calc the disance between two words (`word1`, `word2`):
```
python3 is21.py lev -w word1 -w word2 -v
```
Output:
```
┬   ┌─┐ ┬  ┬
│   ├┤  └┐┌┘
┴─┘ └─┘  └┘ 
    

Multiply sequence alignment

Alignment of word1 with word2
-  -  -  -  -  -  -
      w  o  r  d  2
   0  1  2  3  4  5
w  1  0  1  2  3  4
o  2  1  0  1  2  3
r  3  2  1  0  1  2
d  4  3  2  1  0  1
1  5  4  3  2  1  1
-  -  -  -  -  -  -

Total score: 1 
```

#### Distance between `n` words
Calc the disance between four words (`word1`, `word2`, `w1ord`, `1word`):
```
python3 is21.py lev -w word1 -w word2 -w w1ord -w 1word -v
```
Output:
```
┬   ┌─┐ ┬  ┬
│   ├┤  └┐┌┘
┴─┘ └─┘  └┘ 
    

Multiply sequence alignment

Alignment of word1 with word2
-  -  -  -  -  -  -
      w  o  r  d  2
   0  1  2  3  4  5
w  1  0  1  2  3  4
o  2  1  0  1  2  3
r  3  2  1  0  1  2
d  4  3  2  1  0  1
1  5  4  3  2  1  1
-  -  -  -  -  -  -

Alignment of word1, word2 with w1ord
-  -  --  -  -  -  --  --
          w  1  o  r   d
      0   3  6  9  12  15
w  w  2   0  3  6  9   12
o  o  4   2  2  3  6   9
r  r  6   4  4  4  3   6
d  d  8   6  6  6  5   3
1  2  10  8  7  8  7   5
-  -  --  -  -  -  --  --

Alignment of w-ord1, w-ord2, w1ord- with 1word
-  -  -  --  --  --  --  --  --
              1  w   o   r   d
         0    6  12  18  24  30
w  w  w  3    3  6   12  18  24
-  -  1  6    5  6   9   15  21
o  o  o  9    8  8   6   12  18
r  r  r  12  11  11  9   6   12
d  d  d  15  14  14  12  9   6
1  2  -  18  17  17  15  12  9
-  -  -  --  --  --  --  --  --

Alignment:
w-ord1
w-ord2
w1ord-
1word-

Total score: 15 
```

#### Optimum for `n` words

Calc the disance between four words (`word1`, `word2`, `w1ord`, `1word`) with optimum alignment (`-o` flag):
```
python3 is21.py lev -w word1 -w word2 -w w1ord -w 1word -v -o
```
Output:
```
┬   ┌─┐ ┬  ┬
│   ├┤  └┐┌┘
┴─┘ └─┘  └┘ 
    

Multiply sequence alignment

  Optimal Alignment A*: 
  -  -  -  -  -  -
  -  w  o  r  d  1
  -  w  o  r  d  2
  w  1  o  r  d  -
  1  w  o  r  d  -
  -  -  -  -  -  -

Total score: 15 
```
