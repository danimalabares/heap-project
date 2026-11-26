## What is this

Sources of the Heap Project (www.heap-project.org), the notebook of Daniel González Casanova Azuela. The website is built with Gerby, the software of the Stacks Project. Compile a chapter with `make NAME.pdf`.

## How to use

Make a clone of repo in your computer so that you have all the files.
Then you can edit and compile.

## How to compile

To compile use ``make`` as in

``make complex-geometry.pdf``

Also you can try

``latexmk -pdf complex-geometry.tex``

or

``latexmk -pdf -pvc complex-geometry.tex``

for continuous compilation.

You can also use

``make clean``

to delete all the byproducts of compilation (inclding pdf).
