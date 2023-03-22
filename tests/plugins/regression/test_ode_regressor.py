import pytest

from tempor.plugins import plugin_loader
from tempor.plugins.regression import BaseRegressor
from tempor.plugins.regression.plugin_ode_regressor import ODERegressor as plugin
from tempor.utils.dataloaders.sine import SineDataLoader

train_kwargs = {"random_state": 123, "n_iter": 50}


def from_api() -> BaseRegressor:
    return plugin_loader.get("regression.ode_regressor", **train_kwargs)


def from_module() -> BaseRegressor:
    return plugin(**train_kwargs)


@pytest.mark.parametrize("test_plugin", [from_api(), from_module()])
def test_ode_regressor_plugin_sanity(test_plugin: BaseRegressor) -> None:
    assert test_plugin is not None
    assert test_plugin.name == "ode_regressor"
    assert len(test_plugin.hyperparameter_space()) == 9


@pytest.mark.parametrize("test_plugin", [from_api(), from_module()])
def test_ode_regressor_plugin_fit(test_plugin: BaseRegressor) -> None:
    dataset = SineDataLoader().load()

    test_plugin.fit(dataset)


@pytest.mark.parametrize("test_plugin", [from_api(), from_module()])
def test_ode_regressor_plugin_predict(test_plugin: BaseRegressor) -> None:
    dataset = SineDataLoader().load()

    output = test_plugin.fit(dataset).predict(dataset)
    assert output.numpy().shape == (len(dataset.time_series), 1)


def test_hyperparam_sample():
    for repeat in range(100):  # pylint: disable=unused-variable
        args = plugin._cls.sample_hyperparameters()  # pylint: disable=no-member, protected-access
        plugin(**args)