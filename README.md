# Property Mixin Classes

Provides telescope-specific property mixins to access data in a standardised way.

Further provides GuppiRawHeader classes, both a base class and those for implemented telescopes.

# Conventions

## Expected External Mixin Methods

The expected methods externalised to the adjacent mixins of the final implementation class follow the built-in `dict` class:

- `self.get(key[, default])`
  - the second positional argument is the fallback value in lieu of a value for the key.
- `self.__getitem__(key)`
  - raises KeyError if the key is not populated 
- `self.__setitem__(key, value)`

## Acronym choice

Get as specific as possible as the classes represent a point in the heiarchy

- Array acronym over observatory acronym: `VLA` over `NRAO`
- Project acronym over array acronym: `COSMIC` over `VLA`

## Class names

- Camel-case for the acronym: `Cosmic` as opposed to `COSMIC` 

## Property names

- `_nof_` for `Number of`
