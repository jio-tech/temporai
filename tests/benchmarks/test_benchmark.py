from typing import Callable

from tempor.benchmarks import (
    benchmark_models,
    classifier_supported_metrics,
    regression_supported_metrics,
    time_to_event_supported_metrics,
)
from tempor.plugins import plugin_loader
from tempor.plugins.pipeline import Pipeline
from tempor.utils.dataloaders import (
    GoogleStocksDataLoader,
    PBCDataLoader,
    SineDataLoader,
)


def test_classifier_benchmark() -> None:
    testcases = [
        (
            "pipeline1",
            Pipeline(
                [
                    "preprocessing.imputation.ffill",
                    "classification.nn_classifier",
                ]
            )({"nn_classifier": {"n_iter": 10}}),
        ),
        (
            "plugin1",
            plugin_loader.get("classification.nn_classifier", n_iter=10),
        ),
    ]
    dataset = SineDataLoader().load()

    aggr_score, per_test_score = benchmark_models(
        task_type="classification",
        tests=testcases,
        data=dataset,
        n_splits=2,
        random_state=0,
    )

    for testcase, _ in testcases:
        assert testcase in aggr_score.columns
        assert testcase in per_test_score

    for metric in classifier_supported_metrics:
        assert metric in aggr_score.index

        for testcase, _ in testcases:
            assert metric in per_test_score[testcase].index


def test_regressor_benchmark() -> None:
    testcases = [
        (
            "pipeline1",
            Pipeline(
                [
                    "preprocessing.imputation.ffill",
                    "regression.nn_regressor",
                ]
            )({"nn_regressor": {"n_iter": 10}}),
        ),
        (
            "plugin1",
            plugin_loader.get("regression.nn_regressor", n_iter=10),
        ),
    ]
    dataset = GoogleStocksDataLoader().load()

    aggr_score, per_test_score = benchmark_models(
        task_type="regression",
        tests=testcases,
        data=dataset,
        n_splits=2,
        random_state=0,
    )

    for testcase, _ in testcases:
        assert testcase in aggr_score.columns
        assert testcase in per_test_score

    for metric in regression_supported_metrics:
        assert metric in aggr_score.index

        for testcase, _ in testcases:
            assert metric in per_test_score[testcase].index


def test_time_to_event_benchmark(get_event0_time_percentiles: Callable) -> None:
    testcases = [
        (
            "pipeline1",
            Pipeline(
                [
                    "preprocessing.imputation.ffill",
                    "time_to_event.dynamic_deephit",
                ]
            )({"dynamic_deephit": {"n_iter": 10}}),
        ),
        (
            "plugin1",
            plugin_loader.get("time_to_event.dynamic_deephit", n_iter=10),
        ),
    ]
    dataset = PBCDataLoader().load()

    horizons = get_event0_time_percentiles(dataset, [0.25, 0.5, 0.75])

    aggr_score, per_test_score = benchmark_models(
        task_type="time_to_event",
        tests=testcases,
        data=dataset,
        n_splits=2,
        random_state=0,
        horizons=horizons,
    )

    for testcase, _ in testcases:
        assert testcase in aggr_score.columns
        assert testcase in per_test_score

    for metric in time_to_event_supported_metrics:
        assert metric in aggr_score.index

        for testcase, _ in testcases:
            assert metric in per_test_score[testcase].index
