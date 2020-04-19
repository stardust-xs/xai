# Changelog
<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) starting with version 1.0.

## [Unreleased] - [2.6.1]

### April 19, 2020

#### Added

- Add legacy commit changes from Apr 17 - Apr 15.

### April 18, 2020

#### Added

- `defaults.py` is now used with an alias.
- Update changelog with latest updates.

#### Changed

- Change function orders in [`write.py`](https://github.com/xames3/mle/commit/9b372dab59731d5095a17ab951cc0a63a0d99cc0).
- Replace all instances of validation with test in [`components.py`](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee). Argument session_name is now **session** & train_sample argument is now **train_samples** in [`components.py`](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee).
- Change Tuple to Sequence in [`opencv.py`](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
- rescale() is now resize(), draw_description_box() is display_text(), draw_bounding_box() is display_detection() and draw_statistics_box() is now display_statistics() in [`opencv.py`](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
- Change docstring to fit needs of new functions.

#### Deprecated

- Remove periods from inline comments.

#### Removed

- Remove explicit directories under ./mle/data/ & models from model directory & replace with extensions in [`.gitignore`](https://github.com/xames3/mle/commit/f78430c239078e70009be2122e0d563c6f397cc5).

### April 17, 2020

#### Changed

- Symlink references of caffemodel, prototext and 5-pt & 68-pt face landmarks.

#### Deprecated

- Model symlinks will no longer have `FACE` prefix.

### April 16, 2020

#### Changed

- Symlink reference to use Tiny YOLOv3 config & weights instead of YOLOv3 in [`models.py`](https://github.com/xames3/mle/commit/2c9cf6ccb623ca38fe083c793a7546a7386bcfd2).

### April 15, 2020

#### Added

- Add [`changelog.md`](https://github.com/xames3/mle/commit/ef2ed3ed213ce2ac193dc661f3f757de2ac1df22) to the repository.
- Add support for face detection using YOLOv3 in [`follow.py`](https://github.com/xames3/mle/commit/7a137b283e3a0109b320026315a3633ca8fccf2b).
- New [`detector.py`](https://github.com/xames3/mle/commit/cef628a7d021baee85cb72f983ed79efc30261bf) module which provides support for face detection using YOLOv3 and caffemodel.

#### Changed

- Explicit type hints of the coordinate tuples in [`opencv.py`](https://github.com/xames3/mle/commit/9a5bd68ceefed97122c6001ae901744e02c02656).
- Made symlinks more generalised and variable names less obvious in [`models.py`](https://github.com/xames3/mle/commit/2617e3c310f04be4129e75a80dfb113b85ddb3c7)

#### Removed

- [`face_detector.py`](https://github.com/xames3/mle/commit/672f77a141e778a690c2f5ca01359342d4f1cbef) in favor of `detector.py`.
