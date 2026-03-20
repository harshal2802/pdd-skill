# PDD Reference: Data / ML / AI Projects

> **Last reviewed**: 2026-03

Use this file to enrich Workflows 2, 3, and 5 for data engineering, machine learning, and AI pipeline projects.

---

## Additional Context Questions (Workflow 2)

Ask these after the base questions in `project.md`:

- Is this data engineering, ML modeling, AI pipeline, or a combination?
- What's the primary language and environment? (Python, Jupyter, SQL, Spark, etc.)
- What data sources are involved? (databases, APIs, files, streams)
- How is data stored and accessed? (S3, GCS, data warehouse, feature store)
- Is there a pipeline orchestrator? (Airflow, Prefect, Luigi, dbt, Dagster)
- For ML: what framework? (PyTorch, TensorFlow, scikit-learn, HuggingFace, XGBoost)
- How are experiments tracked? (MLflow, Weights & Biases, Neptune, local)
- How is the model or pipeline deployed? (batch, real-time API, embedded)
- What are the evaluation metrics? (accuracy, F1, RMSE, custom business metric)

### Extended `context/project.md` sections for data/ML

```markdown
## Data
- Sources:
- Storage:
- Volume / frequency: (e.g. 10M rows daily batch, or real-time stream)
- Data quality issues known:

## Pipeline
- Orchestrator:
- Schedule / trigger:
- Idempotency requirement: yes / no

## Modeling (if applicable)
- Framework:
- Model type / architecture:
- Training data location:
- Evaluation metrics:
- Experiment tracker:

## Deployment
- Serving pattern: batch / real-time API / embedded
- Latency requirements:
- Monitoring approach:
```

---

## Conventions Starter (Workflow 2)

```markdown
# Data / ML Conventions

## Project structure
- notebooks/ — exploration only, never production code
- src/ — production pipeline and model code
- data/ — raw/, processed/, features/ (never commit raw data)
- models/ — serialized model artifacts
- configs/ — hyperparameters and pipeline config (YAML or JSON)
- tests/ — unit and integration tests for pipeline steps

## Code standards
- All production code in .py files — not notebooks
- Notebooks are for exploration and documentation only
- Every pipeline step is a pure function where possible
- Functions accept explicit inputs and return explicit outputs — no global state

## Reproducibility
- All randomness seeded explicitly
- All dependencies pinned in requirements.txt or pyproject.toml
- Data transformations versioned alongside code
- Config-driven: hyperparameters and paths in config files, not hardcoded

## Pipelines
- Each step idempotent — running twice produces the same result
- Intermediate outputs saved to allow reruns from any step
- Failed steps fail loudly — no silent data corruption
- Data validation at pipeline entry and exit points

## Experiments
- Every run logged to [MLflow / W&B / local tracker]
- Log: params, metrics, artifacts, and the git commit hash
- Never overwrite a previous experiment run

## Data handling
- Never modify raw data in place — always write to a new output path
- PII fields documented and masked before any logging or sharing
- Schema validated on ingest using [Great Expectations / Pydantic / pandera]
```

---

## Common Feature Prompt Patterns (Workflow 3)

### New pipeline step

```markdown
# Prompt: <StepName> Pipeline Step

## Task
Create a pipeline step `<step_name>` that <transforms / filters / aggregates> <data>.

## Input
- Source: <file path pattern / table / stream>
- Schema: <field names and types>
- Volume: <approximate row count or size>

## Transformation logic
- <describe what happens to the data step by step>
- <edge cases: nulls, duplicates, out-of-range values>

## Output
- Destination: <output path / table>
- Output schema: <field names and types>
- Partitioning: <by date / by key / none>

## Constraints
- Step must be idempotent
- Log row counts at input and output
- Raise an exception (don't silently continue) if input schema doesn't match expected
- Use [pandas / Spark / dbt / Polars — match existing stack]
```

### Model training script

```markdown
# Prompt: <ModelName> Training Script

## Task
Write a training script for a <model type> that predicts <target>.

## Data
- Training data path: <path>
- Features: <list of feature columns>
- Target: <target column>
- Train/val/test split: <ratios>

## Model
- Framework: <PyTorch / sklearn / XGBoost>
- Architecture / algorithm: <describe or leave open>
- Hyperparameters: <list with defaults — these will come from config>

## Evaluation
- Primary metric: <metric>
- Additional metrics: <list>
- Log all metrics and params to <tracker>

## Outputs
- Save model artifact to: models/<model-name>-<run-id>/
- Save evaluation report to: reports/<model-name>-<run-id>.json

## Constraints
- Seed all randomness for reproducibility
- Config-driven — no hardcoded hyperparameters
- Script must be runnable from CLI: `python train.py --config configs/train.yaml`
```

---

## Review Checklist (Workflow 5)

Apply in addition to the universal review dimensions:

**Correctness**
- [ ] Data transformations produce expected output on a sample?
- [ ] Edge cases handled: nulls, empty input, schema drift?
- [ ] No silent data loss (rows dropped without logging)?

**Reproducibility**
- [ ] Random seeds set explicitly?
- [ ] No hardcoded paths — all via config or parameters?
- [ ] Dependencies pinned?

**Pipeline integrity**
- [ ] Each step idempotent?
- [ ] Input schema validated before processing?
- [ ] Output schema validated after processing?
- [ ] Intermediate outputs persisted for reruns?

**Data hygiene**
- [ ] Raw data never modified in place?
- [ ] PII handled and masked appropriately?
- [ ] No sensitive data in logs or experiment tracker?

**ML-specific**
- [ ] Train/val/test split correct — no leakage?
- [ ] Evaluation metrics appropriate for the problem type?
- [ ] Experiment logged with params, metrics, and git hash?
- [ ] Model artifact saved with version information?

**Performance**
- [ ] Vectorized operations used instead of row-level loops?
- [ ] Memory usage reasonable for expected data volume?
- [ ] Long-running steps parallelized where possible?
