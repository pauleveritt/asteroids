from functools import partial


class Registry:
    def __init__(self):
        self.components = {}
        self.systems = []

    def register_component(self, component_id):
        self.components[component_id] = {}

    def register_system(self, func, component_ids):
        # XXX add topological sort options so you can design system
        # execution order where this matters
        self.systems.append(System(func, component_ids))

    def register_system_item(self, func, component_ids):
        self.systems.append(SystemItem(func, component_ids))

    def get(self, entity_id, component_id):
        return self.components[component_id][entity_id]

    def add(self, entity_id, component_id, component):
        self.components[component_id][entity_id] = component

    def remove(self, entity_id, component_id):
        del self.components[component_id][entity_id]

    def entity_ids(self, component_ids):
        result = None
        for component_id in component_ids:
            components = self.components[component_id]
            s = set(components.keys())
            if result is None:
                result = s
            else:
                result = result.intersection(s)
            if not result:
                return set()
        if result is None:
            return set()
        return result

    def query(self, component_ids):
        entity_ids = self.entity_ids(component_ids)
        lists = []
        for component_id in component_ids:
            all_components = self.components[component_id]
            lists.append([all_components[entity_id]
                          for entity_id in entity_ids])
        return lists

    def execute(self):
        for system in self.systems:
            system.execute(self)


class System:
    def __init__(self, func, component_ids):
        self.func = func
        self.component_ids = component_ids

    def query(self, registry):
        return registry.query(self.component_ids)

    def execute(self, registry):
        self.func(*self.query(registry))


def item_func(func, *lists):
    for items in zip(*lists):
        func(*items)


class SystemItem:
    def __init__(self, func, component_ids):
        self.system = System(partial(item_func, func), component_ids)

    def execute(self, registry):
        self.system.execute(registry)
