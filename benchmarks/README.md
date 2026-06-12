# Benchmarks

This directory is for experiments and evaluation code.

The rule for this project is:

```text
src/traffic_analyzer/ = reusable pipeline code
benchmarks/ = experiments that call the reusable pipeline code
```

## Current benchmark focus

1. Compare detection models on the same video samples.
2. Measure inference time and detection quality.
3. Reuse the same output format as the production pipeline.
4. Keep notebooks for exploration, plots and thesis figures.

## Recommended files

- `detection_models_benchmark.ipynb` - exploratory model comparison.
- `benchmark_detection.py` - repeatable detection benchmark script.
- `benchmark_tracking.py` - repeatable tracking benchmark script.
