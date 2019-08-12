## Development Setup

- python3
- [graph-tool 2.29](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions)
- virtualenvwraper (optional but good for your sanity)

Note that graph-tool requires using system default python/python3 as it is a wrapper around a C++ implementation, so if you are using virtualenv/virtualenvwraper see https://jolo.xyz/blog/2018/12/07/installing-graph-tool-with-virtualenv

```bash
mkvirtualenv knesset
workon knesset
pip install -r requirements.txt
```

To verify setup, run all tests:

```bash
python -m unittest discover .
```


## Top Covering Algorithm

`top_covering.py#top_cover` implements the top covering algorithm as described in Handbook of Computational Social Choice, p371.

Test cases to verify correctness can be found in `test_top_covering.py`. To run tests: `python test_top_covering.py`

## PAC Top Covering Algorithm

`top_covering.py#top_cover` implements Algorithm 1 as described in Learning Hedonic Games by Jakub Sliwinski and Yair Zick

To execute the PAC top covering algorithm on the knesset dataset, run test cases in `knesset_test_pac_top_covering.py`: `python knesset_test_pac_top_covering.py`. `test_knesset` is slow (~1min) due to core stability check. `test_knesset_sampling` is extra slow (~35min) due to executing the algorithm 100 times.
