from functools import partial


class Registry:
    def __init__(self):
        self.components = {}
        self.systems = []
        self.component_to_systems = {}

    def register_component(self, component_id):
        self.components[component_id] = {}

    def register_system(self, system):
        # XXX add topological sort options so you can design system
        # execution order where this matters
        self.systems.append(system)
        self.update_component_to_systems(system, system.component_ids)

    def update_component_to_systems(self, system, component_ids):
        for component_id in component_ids:
            self.component_to_systems.setdefault(component_id, []).append(
                system)

    def get(self, entity_id, component_id):
        return self.components[component_id][entity_id]

    def has_components(self, entity_id, component_ids):
        for component_id in component_ids:
            if entity_id not in self.components[component_id]:
                return False
        return True

    # def add_entity(self, **components):
    #     entity_id = self.create_entity_id()
    #     for component_id, component in components.items():
    #         self.add(entity_id, component_id, component)

    def add(self, entity_id, component_id, component):
        self.components[component_id][entity_id] = component
        for system in self.component_to_systems[component_id]:
            system.add(self, entity_id)

    def remove(self, entity_id, component_id):
        del self.components[component_id][entity_id]
        for system in self.component_to_systems[component_id]:
            system.remove(self, entity_id)

    def lists(self, entity_ids, component_ids):
        result = [entity_ids]
        for component_id in component_ids:
            all_components = self.components[component_id]
            result.append([all_components[entity_id]
                           for entity_id in entity_ids])
        return result

    def execute(self, update):
        for system in self.systems:
            system.execute(update, self)


class System:
    def __init__(self, func, component_ids):
        self.func = func
        self.component_ids = component_ids
        self.entity_ids = set()

    def query(self, registry):
        return registry.lists(list(self.entity_ids), self.component_ids)

    def execute(self, update, registry):
        self.func(update, *self.query(registry))

    def add(self, registry, entity_id):
        if not registry.has_components(entity_id, self.component_ids):
            return
        self.entity_ids.add(entity_id)

    def remove(self, registry, entity_id):
        self.entity_ids.remove(entity_id)


def item_func(func, update, *lists):
    for items in zip(*lists):
        func(update, *items)


def item_system(func, component_ids):
    return System(partial(item_func, func), component_ids)
