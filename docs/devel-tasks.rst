Description
===========
JT, short for json templates, is primarily written to scratch an itch of one of
the primary developers. He needed a command line filter that would substitute
values from a json file into a LaTeX template to produce invoices. While a
specific program probably exists, or something much simpler could be made with
an afternoon with Jinja2 and a bit of jiggery-pokery, he also needed a decent
project to learn intermediate python skills. There was also some consideration
of doing this in haskell, and such a version might exist if time allows.

The end goal is that this should be called like

.. code: shell
   jt -t invoice.jtt -o 'invoice{date}.tex' -c 'latex' < invoices.json
   
This would load the invoice template, then if invoices is a json list, for each
   element it would substitute the template, and as long as each json element
   had a "date" field, that would determine the name of the output file.

TODO:
====
- Internal format for substitution lists
- Merge substitution list with chained-dict type environments
- Json to CDTE
- Maybe Yaml to CDTE?
- Subs-list <=> Json
- Subs-list <=> splice-type format, with curly-braces
- Subs-list <=> shell/perl-type format, with sigils
- Output option templatable

