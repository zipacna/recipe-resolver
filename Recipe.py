from collections import Counter


class Component:
    def __init__(self, name='', ingredients=None):
        if ingredients is None:
            ingredients = []
        self.name = name
        self.ingredients = ingredients
        self.broken_down = None

    def __repr__(self):
        return f'Component {self.name}: {self.ingredients}'

    def breakdown(self, resolved: list):
        self.broken_down = Breakdown(item=self.name, ingredients=resolved)


class Ingredient:
    def __init__(self, name=''):
        self.name = name
        self.comp = None

    def convert2comp(self, comp: Component):
        self.comp = comp

    def __repr__(self):
        if isinstance(self.comp, Component):
            return self.comp.__repr__()
        return f'Ingredient {self.name}'


class Breakdown:
    def __init__(self, item: str, ingredients: list):
        self.pretty = None
        self.item = item
        self.raw = self.raw_breakdown(ingredients)
        self.counted = self.occ_breakdown()

    def raw_breakdown(self, ingredients: list):
        broken_down = []
        for ingre in ingredients:
            if isinstance(ingre.comp, Component):
                broken_down.extend(self.raw_breakdown(ingre.comp.ingredients))
            elif isinstance(ingre, Ingredient):
                broken_down.append(ingre.name)
        return broken_down

    def occ_breakdown(self):
        ct = Counter(self.raw)
        self.pretty = []
        for k, v in ct.items():
            self.pretty.append(f'{v}x {k}')
        self.pretty = '\n\t'.join(self.pretty)
        return ct

    def __repr__(self):
        return f'{self.item}\n\t{self.pretty}'
