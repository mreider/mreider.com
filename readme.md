This is my personal website.

I built it using a little tool I built called [Krems](https://github.com/mreider/krems)

To do this yourself clone this directory and:

```
git submodule add https://github.com/mreider/krems krems
git submodule update --init
```

Then from there on

```
ruby krems/krems.rb
```

If something changes in the krems project

```
git submodule update --remote
```