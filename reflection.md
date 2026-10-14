# Reflection

1. Which issues were the easiest to fix, and which were the hardest? Why?

The easy ones were the ones the tools pointed at directly: missing docstrings, renaming setExpiry, the blank lines, opening files with `with`, and the default `[]` argument. Each of those had one obvious fix.

The hard one was the expired permit, because none of the tools flagged it. The only sign was in the output: KA01AB1234 was missing from the flagged list even though its expiry was set to 2020. The cause was that the date was saved as 01/01/2020 while the code reads 2020-01-01, and the bare except swallowed the error and returned False. I also got confused when "Permits on file" printed 3 and then 4. That turned out to be the old permits.json from the first run being loaded again, so it was a real bug (bad permits were being saved) and not a mistake in how I ran it. Taking out the global permits variable was also some work, since every function and every call had to change.

2. Did the static analysis tools report any false positives? If so, describe one example.

I don't think there were any real false positives. The closest was Bandit's warning about random.randint. It is only low severity and for a small demo it hardly matters, but permit numbers shouldn't be guessable, so the fixed version uses secrets. Pylint and Flake8 also disagreed about line length (100 vs 79), but that is just different default settings, not a mistake in either tool.

3. How would you integrate static analysis tools into your actual software development workflow?

While coding I'd run flake8 and pylint in the editor, and add a pre-commit hook so style problems get caught before a commit. In CI I'd run pylint, flake8 and bandit on every pull request and fail the build if the pylint score drops below a set number. Our CI/CD calculator lab already worked like this, and some of its early runs failed just because of lint problems like trailing whitespace. Static analysis can't see logic bugs like the expiry one, so I'd still want unit tests alongside it.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Pylint went from 6.32 to 10.00, and Bandit and Flake8 now report nothing. The behaviour is better too: the expired permit is flagged, bad plates and zones are rejected, pressing Enter at the prompt skips instead of deleting a permit, and old junk no longer builds up in permits.json. Errors aren't hidden by bare excepts any more, and passing permits into each function makes the code easier to read and test.
