from core import constants
from core.epubs import EPUBCheck


def main():
    ec = EPUBCheck(
        constants.EPUBCHECK_DOWNLOAD_URL,
        constants.EPUBCHECK_ROOT_DIR,
        constants.EPUBCHECK_LOCAL_ZIP,
        constants.JAVA_EXECUTABLE
    )
    ec.install()


if __name__ == "__main__":
    main()
