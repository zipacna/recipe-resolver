"""
Title: Recipe-Resolver
Author: Jean Mattes
Author-URI: https://risingcode.net/
Description: Resolves Recipes in the form of indented text.  Returns the resolved Recipe-Trees of more complex examples.

Notes (Note on Notes: https://stackoverflow.com/a/16445016)
    https://www.computerhope.com/issues/ch001721.htm
    https://regexone.com/
"""


import re
from time import time
from timeit import timeit

from Recipe import Component, Ingredient


class Resolver:
    # TODO: add types of ingredients (gas, liquid[hydrazine, soil, ...], earth[anything craftable from soil], metal);
    #  but what is scrap?
    # TODO: add crafting stations to components and ingredients
    lines = []
    recipes = {}

    def __init__(self, f='example-basic.txt'):
        self.f = f
        self.read()
        self.assess()
        self.resolve()
        self.info()

    def read(self):
        with open(self.f) as f:
            for line in f:
                self.lines.append(line)

    def info(self):
        # print(self.lines)
        # print()
        # print(f'is_whitespace:', [self.is_whitespace(t) for t in self.lines])
        # print(f'is_component:', [self.is_component(t) for t in self.lines])
        # print(f'is_ingredient:', [self.is_ingredient(t) for t in self.lines])
        # print()
        # print(self.recipes)
        print('\n'.join([v.broken_down.__repr__() for k, v in self.recipes.items()]))

    def assess(self):
        for i, l in enumerate(self.lines):
            if self.is_whitespace(l):
                continue
            if self.is_component(l):
                n = 1
                while i+n < len(self.lines):
                    line_np1 = self.lines[i+n]
                    if self.is_whitespace(line_np1) or self.is_component(line_np1):
                        break
                    if self.is_ingredient(line_np1):
                        np1_ingre = Ingredient(self.remove_whitespace(line_np1))
                        np1_comp = Component(name=self.remove_whitespace(l), ingredients=[np1_ingre])
                        recipe = self.recipes.get(np1_comp.name)
                        if recipe is None:
                            self.recipes.update({np1_comp.name: np1_comp})
                        elif isinstance(recipe, Component):
                            recipe.ingredients.append(np1_ingre)
                    n += 1

    def resolve_rec(self, ingredients: list):
        resolved = []
        for ingre in ingredients:
            if ingre.name in self.recipes.keys():
                ingre.convert2comp(self.recipes.get(ingre.name))
                resolved.extend(self.resolve_rec(ingre.comp.ingredients))
            else:
                resolved.append(ingre)
        return resolved

    def resolve(self):
        for k, v in self.recipes.items():
            if isinstance(v, Component):
                v.breakdown(self.resolve_rec(v.ingredients))

    @staticmethod
    def is_whitespace(text: str):
        return text.startswith('#') or text.startswith('\n') or (re.search(re.compile(r'\w'), text) is None)

    @staticmethod
    def is_ingredient(text: str):
        return (text.startswith('    ') or text.startswith('\t')) and (re.search(re.compile(r'\w'), text) is not None)

    @staticmethod
    def is_component(text: str):
        return re.search(re.compile(r'^\w'), text) is not None

    @staticmethod
    def remove_whitespace(text: str):
        return text.replace('\n', '').replace('\t', '').replace('  ', '')


if __name__ == '__main__':
    s = time()
    # print(timeit(stmt=Resolver, number=10))
    Resolver(f='example-medium.txt')
    print(f'ROP: {round(time() - s, 6)} sec.')
