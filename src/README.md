## Development Setup

- python3
- [graph-tool](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions)

Note that graph-tool requires using system default python/python3 as it is a wrapper around a C++ implementation, so if you are using virtualenv/virtualenvwraper remember to run `deactivate`.

## Top Covering Algorithm

`top_covering.py#top_cover` implements the top covering algorithm as described in Handbook of Computational Social Choice, p371.

Test cases to verify correctness can be found in `test_top_covering.py`. To run tests: `python test_top_covering.py`
