from functools import partial
import pandas as pd


class DictContainer(dict):
    def value(self):
        return self


class DataFrameContainer:
    def __init__(self):
        self.df = pd.DataFrame([])
        self.to_add_entity_ids = []
        self.to_add_components = []
        self.to_remove_entity_ids = []

    def __setitem__(self, entity_id, component):
        self.to_add_entity_ids.append(entity_id)
        self.to_add_components.append(component)

    def __delitem__(self, entity_id):
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

    def __getitem__(self, entity_id):
        self._complete()
        return self.df.loc[entity_id]

    def __contains__(self, entity_id):
        # cannot call self._complete here as we do not want
        # to trigger it during tracking checks
        if entity_id in self.to_remove_entity_ids:
            return False
        return (entity_id in self.df.index or
                entity_id in self.to_add_entity_ids)

    def value(self):
        self._complete()
        return self.df


class Registry:
    def __init__(self):
        self.components = {}
        self.systems = []
        self.component_to_systems = {}
        self.entity_id_counter = 0

    def register_component(self, component_id, container=None):
        if container is None:
            container = DictContainer()
        self.components[component_id] = container
        self.component_to_systems[component_id] = []

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
            if entity_id not in self.components[component_id]:
                return False
        return True

    def get(self, entity_id, component_id):
        return self.components[component_id][entity_id]

    def create_entity_id(self):
        result = self.entity_id_counter
        self.entity_id_counter += 1
        return result

    def add_entity(self, **components):
        entity_id = self.create_entity_id()
        self.add_components(entity_id, **components)
        return entity_id

    def add_components(self, entity_id, **components):
        for component_id, component in components.items():
            self.add_component(entity_id, component_id, component)

    def add_component(self, entity_id, component_id, component):
        self.components[component_id][entity_id] = component
        for system in self.component_to_systems[component_id]:
            if self.has_components(entity_id, system.component_ids):
                system.track(entity_id)

    def remove_component(self, entity_id, component_id):
        del self.components[component_id][entity_id]
        for system in self.component_to_systems[component_id]:
            system.forget(entity_id)

    def component_containers(self, component_ids):
        return [self.components[component_id]
                for component_id in component_ids]

    def execute(self, update):
        for system in self.systems:
            containers = self.component_containers(system.component_ids)
            system.execute(update, containers)


def container_query(component_containers, entity_ids):
    return [container.value() for container in component_containers]


def entity_ids_query(component_containers, entity_ids):
    return [[container[entity_id] for entity_id in entity_ids]
            for container in component_containers]


class System:
    # XXX make query a dict and let it determine per component what to
    # retrieve, so we can mix different component containers
    def __init__(self, func, component_ids, query=entity_ids_query):
        self.func = func
        self.component_ids = component_ids
        self.query = query
        self.entity_ids = set()

    def execute(self, update, component_containers):
        args = ([self.entity_ids] +
                self.query(component_containers, list(self.entity_ids)))
        self.func(update, *args)

    def track(self, entity_id):
        self.entity_ids.add(entity_id)

    def forget(self, entity_id):
        self.entity_ids.remove(entity_id)


def item_func(func, update, *lists):
    for items in zip(*lists):
        func(update, *items)


def item_system(func, component_ids):
    return System(partial(item_func, func), component_ids)
