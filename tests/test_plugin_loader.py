from src.plugins.registry import PLUGINS


def test_all_plugins_declare_contract_fields():
    for cls in PLUGINS:
        assert isinstance(cls.NAME, str) and cls.NAME
        assert isinstance(cls.VERSION, str) and cls.VERSION
        assert isinstance(cls.REQUIRES, list)


def test_dependency_names_resolve():
    names = {cls.NAME for cls in PLUGINS}
    for cls in PLUGINS:
        for dep in cls.REQUIRES:
            assert dep in names, f"{cls.NAME} requires unknown plugin {dep}"


def test_plugin_names_unique():
    names = [cls.NAME for cls in PLUGINS]
    assert len(names) == len(set(names))