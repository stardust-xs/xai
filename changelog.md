# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) starting with version 1.0.

## [Unreleased] - [2.6.1]

### Added

- Saturday, April 18 2020
  - `defaults.py` is now used with an alias.
  - Update changelog with latest updates.

### Changed

- Saturday, April 18 2020
  - Change function orders in [`write.py`](https://github.com/xames3/mle/commit/9b372dab59731d5095a17ab951cc0a63a0d99cc0).
  - Replace all instances of validation with test in [`components.py`](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee). Argument session_name is now **session** & train_sample argument is now **train_samples** in [`components.py`](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee).
  - Change Tuple to Sequence in [`opencv.py`](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
  - rescale() is now resize(), draw_description_box() is display_text(), draw_bounding_box() is display_detection() and draw_statistics_box() is now display_statistics() in [`opencv.py`](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
  - Change docstring to fit needs of new functions.

### Deprecated

- Saturday, April 18 2020
  - Remove periods from inline comments.

### Removed

- Saturday, April 18 2020
  - Remove explicit directories under ./mle/data/ & models from model directory & replace with extensions in [`gitignore`](https://github.com/xames3/mle/commit/f78430c239078e70009be2122e0d563c6f397cc5).
