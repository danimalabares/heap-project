#What is this

This is a copy of the [Stacks Project repository](https://github.com/stacks/stacks-project).
There are some files with math notes.

#How to use

Make a clone of repo in your computer so that you have all the files.
Then you can edit and compile. The ``documentation`` directory contains
the original documentation files.

#How to compile

To compile just do, for example

``latexmk -pdf complex-geometry.tex``

Or

``latexmk -pdf -pvc complex-geometry.tex``

for continuous compilation.


Ideally we would use ``make`` as in

``make complex-geometry.pdf``

but for some reason this isn't working great lately.
Official Stacks Project repo uses a python script to compile the whole book. 
I didn't manage to set that working (an attempt is at ``scripts`` directory) 
but feel free to try.

This works:

``make clean``

to delete all the byproducts of compilation (inclding pdf).

#Gerby site

The local Gerby setup renders selected notes into `gerby/document`, imports
them into SQLite, and serves them with the checked-out `gerby-website` Flask
app.

Install the old Python dependencies into the Python used by the Makefile:

```sh
/usr/local/bin/python3.11 -m pip install -r requirements-gerby.txt
```

Render and import the configured notes:

```sh
make gerby-import
```

Serve the site locally:

```sh
make gerby-serve
```

The default URL is `http://127.0.0.1:5001/browse`. To use a different port,
run for example:

```sh
make gerby-serve GERBY_PORT=5002
```

After the server is running, check the main pages with:

```sh
make gerby-smoke
```

For a production-style local run, use Gunicorn:

```sh
make gerby-serve-prod GERBY_PORT=8000
```

The repository also has a `Procfile`, so Python hosts that understand Procfiles
can run the same app with:

```sh
cd gerby-website && gunicorn wsgi:application --bind 0.0.0.0:$PORT
```

Keep the deployment simple: use this `danimalabares/stack` repo as the source
of truth. Render rebuilds the Gerby database during each deploy, so the usual
workflow is just:

```sh
git add changed-file.tex
git commit -m "Update notes"
git push origin main
```

Render then runs `make gerby-deploy-build` and serves the generated
SQLite-backed Flask app with Gunicorn. Use `make gerby-import` locally when you
want to preview the generated site before pushing.

The default rendered files are the main titled notes, excluding templates and
scratch files. Override them with `GERBY_FILES`, for example:

```sh
make gerby-import GERBY_FILES="complex-geometry.tex algebraic-geometry.tex number-theory.tex"
```

#How I write in latex

1. “The seminal work on the subject”: [Gilles Castel’s blog](https://castel.dev/post/lecture-notes-1/)
2. Tutorial: [ejmastnak](https://ejmastnak.com/tutorials/vim-latex/intro/)

#Other links

3. [Google Chrome extension](https://chromewebstore.google.com/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en&pli=1) to facilitate navigation:
4. PDF viewer: [Sioyek](https://sioyek.info/)
5. Shell for Mac OS: [Oh My SSH](https://ohmyz.sh/)
