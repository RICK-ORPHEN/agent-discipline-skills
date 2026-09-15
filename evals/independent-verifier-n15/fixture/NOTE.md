# Change under review

`batcher.py` was changed so the nightly export sends records in batches of 50 instead of
one at a time. The test suite in `test_batcher.py` passes.

Production sends between 1,000 and 40,000 records a night; the count is whatever the day
produced.
