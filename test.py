import os
import sys
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


def size(name, width, height):
    return {"width": width, "height": height, "name": name}


def capture_feature(driver, feature, size, capture_dir="./"):
    size_name = size["name"]
    feature_name = feature.__name__
    feature(driver)
    driver.set_window_size(size["width"], size["height"])
    os.makedirs(capture_dir, exist_ok=True)
    driver.save_screenshot(f"{capture_dir}{feature_name}-{size_name}.png")


def clean_path(path):
    return path


def noop_feature(driver):
    pass


def page_feature(path, root):
    def _page(driver):
        driver.get(f"{root}{path}")

    _page.__name__ = f"page_{clean_path(path)}_feature"
    return _page


def main(root, pages):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(root)
    sizes = [
        size("tiny", 500, 768),
        size("small", 700, 768),
        size("medium", 950, 768),
        size("large", 1200, 768)
    ]
    features = [
        noop_feature,
        *[page_feature(p, root) for p in pages]
    ]
    for f in features:
        for s in sizes:
            capture_feature(driver, f, s, "capture/")

    driver.close()


main(sys.argv[1], sys.argv[2:])
