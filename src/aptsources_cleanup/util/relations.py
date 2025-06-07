# -*- coding: utf-8
__all__ = ('EquivalenceRelation',)

import itertools
from operator import methodcaller
from .functools import comp, partial as fpartial
from .collections import ExtSet


class FrozensetAltRepr(frozenset):

	__slots__ = ()


	def __str__(self):
		return self._str_impl(self)


	@staticmethod
	def _str_impl(items):
		return ', '.join(tuple(map(repr, items))).join(('{', '}'))


class OrderedFrozenset(FrozensetAltRepr):

	__slots__ = ('order',)


	def __new__(cls, items=()):
		items = dict(zip(items, itertools.count()))
		self = super().__new__(cls, items.keys())
		self.order = items
		return self


	def index(self, item):
		return self.order[item]


	def __str__(self):
		assert self == self.order.keys()
		return self._str_impl(self.order)


class EquivalenceRelation(frozenset):

	__slots__ = ()


	def __new__(cls, *classes, settype=FrozensetAltRepr):
		if len(classes) == 1:
			classes, = classes

		if settype is None:
			settype = FrozensetAltRepr
		elif settype == "ordered":
			settype = OrderedFrozenset

		self = super().__new__(cls, map(settype, classes))
		if not self:
			try:
				return cls.EMPTY
			except AttributeError:
				pass

		if __debug__:
			overlapping = [
				"{:s} & {:s} = {:s}".format(
					*map(FrozensetAltRepr._str_impl, (a, b, a & b)))
				for a, b in itertools.combinations(self, 2) if not a.isdisjoint(b)
			]
			assert not overlapping, \
				'Overlapping equivalence classes: ' + ', '.join(overlapping)

		return self


	def get_class(self, element):
		containing_classes = filter(methodcaller('__contains__', element), self)
		clazz = next(containing_classes, None)
		if __debug__:
			if clazz is not None:
				try:
					next(containing_classes)
				except StopIteration:
					pass
				else:
					raise AssertionError(
						repr(element) + " appears in at least two classes")
		return clazz


	@classmethod
	def parse(cls, s, item_delimiter=',', class_delimiter=';', **kwargs):
		if class_delimiter in item_delimiter:
			raise ValueError(
				"Item delimiters must not contain class delimiters; but got {!r} in {!r}"
					.format(class_delimiter, item_delimiter))
		return cls(
			map(methodcaller('split', item_delimiter), s.split(class_delimiter)),
			**kwargs)


	def __str__(self):
		return format(self)


	def __format__(self, sfmt):
		classes = self

		if sfmt:
			fmt = sfmt[1:].split(sfmt[0], 6)
			if len(fmt) < 2:
				raise ValueError("Illegal format: " + repr(sfmt))

			if len(fmt) % 2:
				classes, item_transform = (
					self._format_parse_options(fmt.pop(), classes))
			else:
				item_transform = None

			item_delimiter = fmt[0]
			class_delimiter = fmt[1]
			class_prefix_suffix = fmt[2:4]
			prefix_suffix = fmt[4:6]

		else:
			item_transform = repr
			item_delimiter = ', '
			class_delimiter = '; '
			prefix_suffix = class_prefix_suffix = ('{', '}')

		if item_transform:
			classes = map(comp(fpartial(map, item_transform), tuple), classes)
		classes = map(item_delimiter.join, classes)
		if any(class_prefix_suffix):
			classes = map(methodcaller('join', class_prefix_suffix), classes)
		classes = class_delimiter.join(tuple(classes))
		if any(prefix_suffix):
			classes = classes.join(prefix_suffix)
		return classes


	@classmethod
	def _format_parse_options(cls, s, classes):
		opts = ExtSet(s)

		sort_mode = opts.discard_first_of(('a', 'd'))
		if sort_mode is not None:
			sort_mode = fpartial(sorted, reverse=sort_mode == 'd')
			classes = sort_mode(map(sort_mode, classes))

		if not opts:
			item_transform = ''
		elif len(opts) == 1:
			item_transform, = opts
		else:
			item_transform = None

		item_transform = cls._item_transformers.get(item_transform, False)
		if item_transform is False:
			raise ValueError('Invalid format option string: ' + repr(s))

		return (classes, item_transform)


	_item_transformers = { '': None, 's': str, 'r': repr }


EquivalenceRelation.EMPTY = EquivalenceRelation()


class IndexedEquivalenceRelation(EquivalenceRelation):

	__slots__ = ('_index',)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._index = dict(itertools.chain.from_iterable(
			zip(clazz, itertools.repeat(clazz)) for clazz in self))


	def get_class(self, element):
		return self._index.get(element)
