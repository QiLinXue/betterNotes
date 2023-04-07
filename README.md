# BetterNotes (WIP)

## Introduction to BetterNotes
**BetterNotes** is a project with the intended purpose of making the process of note-taking more *streamlined* for STEM classes, specifically aimed at math, physics, and CS courses.

### Demo
**See an interactive live demo [here!](http://qilin-better-notes.herokuapp.com/)**

**Watch it in action:** *Note:* in the demo below, I used a VSCode extension that automatically updates the HTML file, but you can use any editor you wish! You can even use a markdown app, and the HTML file will still be automatically updated.
![](better-notes-demo.gif)
### High Level Goals
This aims to make note-taking easier by:

* Making notes more modular. A simple markdown file can automatically be converted to:
    * PDF
    * HTML
* Support for $\LaTeX$, tables, diagrams, and more!
* Ability to create extensions to add more features such as graphs
* A quick and readable documentation system!
* Style should be easy to customize

### Inspiration
This project is inspired from spending countless hours taking notes in both $\LaTeX$ and HTML as both a student and a teaching assistant. Why can't I take notes on an easier platform and have it convert it to both HTML and LaTeX?

### Disclaimer
The project is not yet complete! Currently, it only supports markdown to HTML. I hope to eventually add $\LaTeX$ support and custom styles (who knew writing notes could be so simple!)


## Features
Here are some examples of basic features

### Math
We support in-line equation $ax^2+bx+c=0$ as well as full-line equations:
$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$
It live updates! Wow... This is so cool....

We can even do a standard verbatim environment to get stuff like `@this@`!
### Code
It can do in-line code `like this` or do code blocks like this:
```py
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)
```

### Images
We can import a simple image (this is what DALLE gives me for the prompt `note taking app cyberpunk`)
![](test_img.png)

### TikzPicture
This note system supports custom tikzpictures! How cool is that!
```tex
tikz
\draw (0,0) rectangle (1,1);
\draw[->, thick] (0.5,0.5) -- (1.5,1.5) node[anchor=south] {$\vec{F}$};
\draw[->, thick] (0.5,0.5) -- (-1.5,0.5) node[anchor=north] {$F_g$};
\draw[->, thick] (0.5,0.5) -- (0.5,1.5) node[anchor=west] {$F_N$}; 
\draw[->] (2.5,1.5) -- (3,1.5) node[anchor=west] {${x}$};
\draw[->] (2.5,1.5) -- (2.5,2) node[anchor=south] {$_{y}$};
```

### Boxes
We can create definitions

@@DEF
A **stack** is a collection of elemennts with the operations `push` and `pop`
* `push` inserts the elements into the collection
* `pop` removes the most *recently added element* that's not yet removed an returns it.
@@

and theorems

@@THM
Theorem: It is trivial to show that
$$ P \neq NP$$
@@

@@PRF
*Proof:* Prove by contradiction. Suppose $P=NP.$ Then pick $N=2.$ Dividing both sides by $P$ gives
$$1 = N$$
contradicting $N=2.$
@@

## Usage
### Compiling
First, make sure you pip install `pyinstaller`. Then run:
```bash
pyinstaller --onefile betterNotes.py
```

You may need to add it to path. On Linux, you can do this via
```bash
mv dist/betterNotes ~/bin
nano ~/.bashrc
export PATH="$PATH:$HOME/bin"
source ~/.bashrc
```

### Live Update
After it has compiled, you can run
```bash
betterNotes input.md output.html
```
where you can replace `input.md` and `output.html` with the respective input and output files. If `output.html` is not give, the output file will default to `input.html`. If `input.md` or `output.html` do not exist, they will be created. Therefore, to start new notes you can simply run
```bash
betterNotes input.md
```