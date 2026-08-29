# Conference notebook format

Use the established style of
`hodge-birational-atoms-2026.tex` and
`xxii-egd-2026.tex`, subject to the current
rules in `AGENTS.md`.

## Source fidelity

The official conference website is the
source of truth. Its programme, abstract
pages, and linked official PDFs may provide
different parts of an entry. Retain the URL
that supports each item.

Use the official spelling and ordering of:

- the event title;
- presentation titles;
- speaker names;
- affiliations;
- presentation types;
- dates, times, rooms, and venues.

Do not infer an affiliation from an email
domain, personal knowledge, or another
website. Do not infer a missing date or time
from neighbouring schedule entries.

For an unavailable field, write one of these
as appropriate:

```tex
Not listed on the official site as of
MONTH DAY, YEAR.
```

```tex
No abstract is available on the official
site as of MONTH DAY, YEAR.
```

## Verbatim abstracts

Copy every available abstract without
rewriting it. Preserve its words, spelling,
capitalization, punctuation, paragraph
breaks, citations, and mathematical
content. Do not repair apparent errors.

The following are mechanical TeX changes,
not editorial changes:

- escape TeX special characters;
- convert official HTML or MathJax math to
  equivalent TeX;
- encode links with `\href`;
- replace web-only typography with its TeX
  equivalent;
- insert line breaks to meet the repository
  width limit.

After conversion, compare the rendered text
with the official abstract word for word.
Keep the source's paragraph boundaries.

## Chapter opening

Use this shape, adapting only fields that
are actually available:

```tex
\input{preamble}
\begin{document}

\title{Official conference title}
\maketitle
\phantomsection
\label{section-phantom}
\tableofcontents

\medskip\noindent
{\bf Conference information.}

\href{OFFICIAL-URL}{%
Official conference title}

Official date range.

Official venue,
city, region, country.

Information accessed MONTH DAY, YEAR.

\medskip\noindent
{\bf Organizers.}

Official organizer list.
```

Omit the organizer block only when the
official sources do not identify organizers;
then state that it was not listed in the
conference information block.

## Presentation sections

Create one `\section` for each talk or
lecture and one for each complete
minicourse. Use the exact official title,
with only necessary TeX encoding. Never use
subsections or subsubsections.

Use a unique lowercase label derived from
the title and, when needed, the speaker:

```tex
\section{Exact official presentation title}
\label{section-lowercase-unique-title}

\medskip\noindent
{\bf Official presentation type.}

Speaker name,
official affiliation.

\medskip\noindent
{\bf Schedule.}

Official date, time, room or venue.

\medskip\noindent
{\bf Official listing.}

\href{OFFICIAL-ENTRY-URL}{Programme entry.}

\medskip\noindent
{\bf Abstract.}

Verbatim abstract paragraphs, with only
mechanical TeX conversion.
```

Use the presentation type printed by the
official programme, such as `Talk`,
`Plenary lecture`, `Contributed talk`, or
`Minicourse`. If no type is given, use
`Presentation` rather than guessing.

For a minicourse, list all official sessions
inside its single Schedule block:

```tex
\begin{itemize}
\item Session 1: official date, time, room.
\item Session 2: official date, time, room.
\end{itemize}
```

If the same title is explicitly delivered as
separate talks rather than sessions of one
minicourse, preserve the programme's own
grouping.

End the document with:

```tex
\bibliography{my}
\bibliographystyle{amsalpha}

\end{document}
```

Do not add mathematical exposition, speaker
biographies, inferred research interests,
or placeholder notes. The initial chapter is
a faithful conference scaffold; handwritten
content can be added under each section
later.
