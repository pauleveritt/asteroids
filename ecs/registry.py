from functools import partial
import pandas as pd


class DictContainer:
    def __init__(self):
        self.d = {}

    def add(self, entity_id, component):
        self.d[entity_id] = component

    def remove(self, entity_id):
        del self.d[entity_id]

    def get(self, entity_id):
        return self.d[entity_id]

    def contains(self, entity_id):
        return entity_id in self.d

    def list(self, entity_ids):
        d = self.d
        return [d[entity_id] for entity_id in entity_ids]


class DataFrameContainer:
    def __init__(self):
        self.df = pd.DataFrame([])
        self.to_add_entity_ids = []
        self.to_add_components = []
        self.to_remove_entity_ids = []

    def add(self, entity_id, component):
        self.to_add_entity_ids.append(entity_id)
        self.to_add_components.append(component)

    def remove(self, entity_id):
        self.to_remove.append(entity_id)

    def _complete(self):
        self._complete_remove()
        self._complete_add()

    def _complete_add(self):
        if not self.to_add_entity_ids:
            return
        add_df = self._create(self.to_add_components,
                              self.to_add_entity_ids)
        self.df = pd.concat([self.df, add_df])
        self.to_add_entity_ids = []
        self.to_add_components = []

    def _complete_remove(self):
        if not self.to_remove_entity_ids:
            return
        self.df = self.df.drop(self.to_remove_entity_ids)

    def _create(self, components, entity_ids):
        return pd.DataFrame(components, index=entity_ids)

    def get(self, entity_id):
        self._complete()
        return self.df.loc[entity_id]

    def contains(self, entity_id):
        # cannot call self._complete here as we do not want
        # to trigger it during tracking checks
        if entity_id in self.to_remove_entity_ids:
            return False
        return (entity_id in self.df.index or
                entity_id in self.to_add_entity_ids)

    def list(self, entity_ids):
        self._complete()
        # we ignore entity_ids here, as we need to return
        # the original dfs to the function. This implies a system
        # at an even higher level which just takes the entire dfs
        # of components to update along with the entity_ids that match and
        # handles it there
        return self.df


class Registry:
    def __init__(self):
        self.components = {}
        self.systems = []
        self.component_to_systems = {}

    def register_component(self, component_id, container=None):
        if container is None:
            container = DictContainer()
        self.components[component_id] = container

    def register_system(self, system):
        # XXX add topological sort options so you can design system
        # execution order where this matters
        self.systems.append(system)
        self.update_component_to_systems(system, system.component_ids)

    def update_component_to_systems(self, system, component_ids):
        for component_id in component_ids:
            self.component_to_systems.setdefault(component_id, []).append(
                system)

    def has_components(self, entity_id, component_ids):
        for component_id in component_ids:
            if not self.components[component_id].contains(entity_id):
                return False
        return True

    def get(self, entity_id, component_id):
        return self.components[component_id].get(entity_id)

    # def add_entity(self, **components):
    #     entity_id = self.create_entity_id()
    #     for component_id, component in components.items():
    #         self.add(entity_id, component_id, component)

    def add(self, entity_id, component_id, component):
        self.components[component_id].add(entity_id, component)
        for system in self.component_to_systems[component_id]:
            system.track(self, entity_id)

    def remove(self, entity_id, component_id):
        self.components[component_id].remove(entity_id)
        for system in self.component_to_systems[component_id]:
            system.forget(self, entity_id)

    def component_containers(self, component_ids):
        return [self.components[component_id]
                for component_id in component_ids]

    def lists(self, entity_ids, component_ids):
        return [component_container.list(entity_ids)
                for component_container
                in self.component_containers(component_ids)]

    def execute(self, update):
        for system in self.systems:
            system.execute(update, self)


def container_query(registry, entity_ids, component_ids):
    return registry.component_containers(component_ids)


def entity_ids_query(registry, entity_ids, component_ids):
    return registry.lists(entity_ids, component_ids)


class System:
    def __init__(self, func, component_ids, query=entity_ids_query):
        self.func = func
        self.component_ids = component_ids
        self.query = query
        self.entity_ids = set()

    def execute(self, update, registry):
        args = [self.entity_ids] + self.query(registry, list(self.entity_ids),
                                              self.component_ids)
        self.func(update, *args)

    def track(self, registry, entity_id):
        if not registry.has_components(entity_id, self.component_ids):
            return
        self.entity_ids.add(entity_id)

    def forget(self, registry, entity_id):
        self.entity_ids.remove(entity_id)


def item_func(func, update, *lists):
    for items in zip(*lists):
        func(update, *items)


def item_system(func, component_ids):
    return System(partial(item_func, func), component_ids)
