# Changelog
<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) starting with version 1.0.

## [Unreleased] - [2.6.1]

### April 21, 2020

#### Added

- Added previous day commit changes in [changelog.md].

### April 20, 2020

#### Added

- Added examples in `fuzzy_search()`'s docstring to explain it's use in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0).
- Added argument for considering threading in `toast()` in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0). This is used in MLE Vzen service.
- Added a plain black image for testing.
- Added support for new & improved functions like `toast()`, `detect_faces()` in [follow.py](https://github.com/xames3/mle/commit/cd75ac5e29d9d3ac7e7a53b6c1f9bd970e3b68db).

#### Changed

- Changed `find_string()` to `fuzzy_search()`, since the name makes the function more obvious and optimized `log()` in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0).
- Changed OSError with more explicit `socket.error` for socket based exceptions in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0).
- `seconds_to_datetime()` now explicitly converts seconds to int in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0).
- Changed default video source back to internal webcam instead of video file in [follow.py](https://github.com/xames3/mle/commit/cd75ac5e29d9d3ac7e7a53b6c1f9bd970e3b68db).
- Elapsed time is now displayed as soon as the MLE VZen service is started unlike previously which used to display after calculating the FPS in [follow.py](https://github.com/xames3/mle/commit/cd75ac5e29d9d3ac7e7a53b6c1f9bd970e3b68db).
- Changed docstrings for all the functions to fit newer use cases in [detector.py](https://github.com/xames3/mle/commit/f6647a4808c9dd0d5ab636a36c8f18ba09f81b93).
- Changed x0, y0, x1 & y1 to left, top, right & bottom respectively.

#### Deprecated

- Plain import for defaults module is deprecated, now it is used with an alias `dx` unless imported with something.
- Obvious inline comments are deprecated.
- `face` prefixes are deprecated for real.

#### Fixed

- Fixed imports to use newer functions in [detector.py](https://github.com/xames3/mle/commit/f6647a4808c9dd0d5ab636a36c8f18ba09f81b93).

#### Removed

- Removed `pick_random_color()` since it is not used anywhere in [common.py](https://github.com/xames3/mle/commit/5645a82a3b66c834304f705b27e958f4f6ee14b0).
- Removed support for YOLOv3 object detection and switched back to CaffeModel in [follow.py](https://github.com/xames3/mle/commit/cd75ac5e29d9d3ac7e7a53b6c1f9bd970e3b68db).
- Now [detector.py](https://github.com/xames3/mle/commit/f6647a4808c9dd0d5ab636a36c8f18ba09f81b93) doesn't display X, Y & Z orientation angles while detecting faces.
- Removed `detect_faces_using_yolo()` and moved it to archive from [detector.py](https://github.com/xames3/mle/commit/f6647a4808c9dd0d5ab636a36c8f18ba09f81b93).

[Back to top](#changelog)

### April 19, 2020

#### Added

- Added legacy commit changes from Apr 17 - Apr 15.

[Back to top](#changelog)

### April 18, 2020

#### Added

- Added alias for `defaults.py`.
- Added latest updates to changelog.

#### Changed

- Changed function orders in [write.py](https://github.com/xames3/mle/commit/9b372dab59731d5095a17ab951cc0a63a0d99cc0).
- Replace all instances of validation with test in [components.py](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee). Argument session_name is now **session** & train_sample argument is now **train_samples** in [components.py](https://github.com/xames3/mle/commit/1aba4d8dcca3131b46ff3e49ccc8988d689bcaee).
- Change Tuple to Sequence in [opencv.py](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
- `rescale()` is now `resize()`, `draw_description_box()` is `display_text()`, `draw_bounding_box()` is `display_detection()` and `draw_statistics_box()` is now `display_statistics()` in [opencv.py](https://github.com/xames3/mle/commit/ea43b6f568846b0af55753d05a5984eac7001039).
- Change docstring to fit needs of new functions.

#### Deprecated

- Periods from inline comments are now deprecated.

#### Removed

- Removed explicit directories under ./mle/data/ & models from model directory & replace with extensions in [.gitignore](https://github.com/xames3/mle/commit/f78430c239078e70009be2122e0d563c6f397cc5).

[Back to top](#changelog)

### April 17, 2020

#### Changed

- Changed symlink references of caffemodel, prototext and 5-pt & 68-pt face landmarks.

#### Deprecated

- Model symlinks will no longer have `FACE` prefix.

[Back to top](#changelog)

### April 16, 2020

#### Changed

- Changed symlink reference to use Tiny YOLOv3 config & weights instead of YOLOv3 in [models.py](https://github.com/xames3/mle/commit/2c9cf6ccb623ca38fe083c793a7546a7386bcfd2).

[Back to top](#changelog)

### April 15, 2020

#### Added

- Added [changelog.md](https://github.com/xames3/mle/commit/ef2ed3ed213ce2ac193dc661f3f757de2ac1df22) to the repository.
- Added support for face detection using YOLOv3 in [follow.py](https://github.com/xames3/mle/commit/7a137b283e3a0109b320026315a3633ca8fccf2b).
- Added new [detector.py](https://github.com/xames3/mle/commit/cef628a7d021baee85cb72f983ed79efc30261bf) module which provides support for face detection using YOLOv3 and caffemodel.

#### Changed

- Changed explicit type hints of the coordinate tuples in [opencv.py](https://github.com/xames3/mle/commit/9a5bd68ceefed97122c6001ae901744e02c02656).
- Changed symlinks to make them more generalised and variable names less obvious in [models.py](https://github.com/xames3/mle/commit/2617e3c310f04be4129e75a80dfb113b85ddb3c7)

#### Removed

- [face_detector.py](https://github.com/xames3/mle/commit/672f77a141e778a690c2f5ca01359342d4f1cbef) in favor of `detector.py`.

[Back to top](#changelog)
