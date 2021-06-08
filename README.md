# PyAHHH
### An [AHHH](https://github.com/KyleM73/AHHH) interpreter written in Python. Creating it made me scream. 
---

Finely crafted by Kyle Morgenstein, AHHH is an esoteric language written entirely by screaming into the void. The original interpreter code provided by Morgenstein is written in C++. I don't know C++ nor how to compile it on Windows, so I just wrote it in Python instead. 

To execute this script Python 3.6 or above is required. (I like f-strings)

Demo programs are available in the [demo](/demo) folder. 

### Setup and Usage

Currently you can just download [`main.py`](/main.py) above to get going. 

To execute a .ahhh file provide it as the first argument to `main.py` as such:

```
python main.py demo/test.ahhh
```
on linux you'll probably have to specify your python version like `python3.8 ...`

#### Debug Mode

An addition made over the original is a "debug mode". This prints out a lot of extra information such as each instruction code being executed, and the state of memory and the registers after each instruction. etc. 

To enable debug mode simply apply the `-d` flag at the command line:
```
python main.py demo/test.ahhh -d
```
----
### Simple Example Execution

Lets look at [test.ahhh](/demo/test.ahhh):
```
AHHH Start
HhhHHhhHHhhHHhhH Set cell 0 to 4
```
Above, we have started the script as all AHHH scripts must: screaming at full volume. Then, we have executed `HhhH` (increment memory cell by 1) 4 times. The memory pointer defaults to cell 0, so cell 0 is incremented up to 4. 

```
HHHh Square cell 0 -> 16
HHhH double cell 0 -> 32
```
Here we've squared and then doubled the current cell. Turning our 4 into a 32. 

```
HhhH Add 1 to cell 0 -> 33 (ASCII !)
```
Lastly for cell 0 we add 1 again. This leaves us with an integer 33, which is an exclamation mark `!` in ASCII.

```
hhhH Move pointer to cell 1
HhhHHhhHHhhHHhhH Set cell 1 to 4 - loop counter
```
Now we shift the memory pointer over to the right. Newly encountered memory cells are initialised to zero, so cell 1 is zero. Nex, like before, we increment cell 1 to hold a value of 4. This cell will be our loop counter.

```
HHHH Start loop
HhHh Decrement cell 1
hhHh Move to cell 0
Hhhh Print cell 0
hhhH Move to cell 1
hhhh End loop
```
`HHHH` marks the start of a loop. Given the currently selected cell is nonzero, we proceed with the loop block. 

Step one of this loop is to decrement that loop counter by 1, then move the memory pointer back to cell 0. 

Next we print out the ASCII character represented by the integer held in cell 0, a `!`. 

Lastly we move our pointer back to cell 1, then hit the end of the loop, represented by `hhhh`, which sends the program back to `HHHH`. 

Now `HHHH` will again check if the current cell is non-zero, find it to be 3, and so continue with the loop once more. However, after repeating this four times, the value in cell 1 will be zero. Now, `HHHH` sees that the selected cell is zero, and searches back down for the end of the loop, skipping the loop block's content. The next instruction to be executed will be whatever comes after `hhhh`:

```
hhhHhhhH move pointer right by 2. Next is Hello, World:
HhhHHHhHHHHhHHHhHHhHHHhHHhhHHhhHHhhHHhhHHhhHHhhHHhhHHhhHhHhhHhhhhhhHHhhHHHhHHHHhHHHhHHhHhHHhhHhhhHhhHhHhHhHhHhHhHhhhhhhHhHhhHhhHHhhHHhhHHhhHhHhhHhhhhhhHhHhhhHhhHhhhhhhHhHhhhHhhHhhHHhhHHhhHHhhhhhhHHhhHHHhHHHHhHHHhHHhHhHhHHHhhHhhHHHhHHHHhHHHhhHHHhHhHHhHhHhHhHhHhHhHhHhhhhhhHHhhHHHhHHHHhHHHhHHhHHhhhhhhHHhhHHHhHHHHhHHHhHHhHHHhHhHhHHHhhHhhHHHhHHHHhHHHhhHHHHHhhHhhHHHhHHHhHHHhHhHHHhHhHHhHhHhhhhhhHhHhhHhhHHhhHHhhHhHhhHhhhhhhHhHhhhHhhHhhHHhhHHhhHHhhhhhhHhHhhHhHhHhHhHhHhhHhhHhhhhhhHhHhhHhHhHhHhHhHhHhHhHhHhHhHhHhHhHhHhHhhhhhhHHhhHHHhHHHHhHHHhHHhHHhhHHhhhhhh!
```
This is just the compressed `Hello, World!` AHHH demo script provided in the the original repository. An expanded version of this, complete with comments, has been copied into this repository here: [hello_world_expanded.ahhh](demo/hello_world_expanded.ahhh).

The final output of this program will be:
```
!!!!Hello, World!\n
```

---

You can find the original AHHH definition and language details here: [AHHH by Kyle Morgenstein](https://github.com/KyleM73/AHHH)
