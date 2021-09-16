class Component(dict):
    def __init__(self, name, parent=None, children=None, **kwargs):
        assert name != '' and name != ' ' and name != None, 'Name cannot be {0}'.format(name)
        self.__name = name
        self['name'] = self.__name

        if parent is not None:
            assert isinstance(parent, Component), 'Parent must be a Component'
            if self not in parent.get_children():
                parent.add_child(self)
        self.__parent = parent

        if children is not None:
            assert isinstance(children, list), 'Children must be a list of Component instances'
            for child in children:
                assert isinstance(child, Component), 'Child instances must be a Component'
            self.__children = children
        else:
            self.__children = []

        for arg in kwargs:
            self[arg] = kwargs[arg]

    def get_parent(self):
        if self.__parent is None:
            print('No parent')
            return None
        else:
            return self.__parent

    def get_children(self):
        if self.__children is None:
            print('No children')
            return None
        else:
            return self.__children

    def add_child(self, child):
        assert isinstance(child, Component), 'Child must be a Component'
        self.__children.append(child)


if __name__ == '__main__':
    components = []
    antriebswelle = Component('Antriebswelle')
    components.append(antriebswelle)
    components.append(Component('6017', parent=antriebswelle, children=None, sub_name='6017-1', stl_files=[
          "Antriebswelle - 6017-3 _6017_PART1_2-1.STL",
          "Antriebswelle - 6017-3 _6017_PART2_4-1.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-12.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-15.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-16.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-17.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-18.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-19.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-20.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-21.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-22.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-23.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-24.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-25.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-26.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-27.STL",
          "Antriebswelle - 6017-3 _6017_PART3_6-8.STL"]))
    components.append(Component('6017', parent=antriebswelle, sub_name='6017-2', stl_files=[
          "Antriebswelle - 6017-4 _6017_PART1_2-1.STL",
          "Antriebswelle - 6017-4 _6017_PART2_4-1.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-12.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-15.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-16.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-17.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-18.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-19.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-20.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-21.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-22.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-23.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-24.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-25.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-26.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-27.STL",
          "Antriebswelle - 6017-4 _6017_PART3_6-8.STL"]))
    components.append(Component('Welle', parent=antriebswelle, stl_files=['Antriebswelle - Antriebswelle-1.STL']))
    components.append(Component('Parallel Key', parent=antriebswelle)) #TODO: stl_files missing?

    children = antriebswelle.get_children()
    for child in children:
        print(child['name'])


### Tests ###
#TODO: Component init assert
#TODO: Component init add Children, wrong instances
#TODO: Component init ad parent, wrong instance