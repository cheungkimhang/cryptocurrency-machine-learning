import argparse

def main(
    # skip_scrape: bool = False, skip_strategy: bool = False, skip_slack: bool = False
) -> None:
    print("hello world")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=__name__,
    )
    args = parser.parse_args()
    main()
