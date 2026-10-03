# Smell baseline

Fowler's code smells from *Refactoring*, chapter 3. They apply when the repo documents nothing. A documented repo rule wins: where the repo endorses a pattern, drop the smell. Skip anything the linter or typecheck already enforces.

Every smell is `[judgement]`. Write the exact name as the Source, so the validator can match it.

- **Mysterious Name.** A name that does not say what the thing does or holds. Rename it.
- **Duplicated Code.** The same logic shape in two hunks or files of the diff. Extract it and call it from both.
- **Feature Envy.** A function that reads another module's data more than its own. Move it to that data.
- **Data Clumps.** The same few fields or params travel together. Bundle them into one type.
- **Primitive Obsession.** A string or number standing in for a domain concept. Give the concept a type.
- **Repeated Switches.** The same switch on the same union in several places. Share one map or one function.
- **Shotgun Surgery.** One logical change forces edits across many files. Gather what changes together.
- **Divergent Change.** One file edited for several unrelated reasons. Split it.
- **Speculative Generality.** Parameters, hooks, or abstraction the spec does not need. Inline it.
- **Message Chains.** Long `a.b().c().d()` navigation. Hide the walk behind one call.
- **Middle Man.** A function that only delegates. Call the target directly.
- **Refused Bequest.** An implementer that ignores most of what it inherits. Use composition.
