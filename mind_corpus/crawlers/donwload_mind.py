import json
import os
from tqdm import tqdm
from google_drive_downloader import GoogleDriveDownloader as gdd

import mind_corpus.constants as const
from mind_corpus.crawlers.newspaper3k_crawler import crawl_url


def download_subset_newspaper3k(subset_name, subset_articles):
    print("Downloading {} subsets - Starting...".format(subset_name))
    print()

    crawler_status = {"success": 0, "fail": 0}
    for entry in tqdm(subset_articles):
        if entry["source"] != "lusa":
            current_status = crawl_url(const.fp_mind_corpus, entry)
            if current_status:
                crawler_status["success"] += 1
            else:
                crawler_status["fail"] += 1
    print()
    print("Downloading {} subsets - Complete (Retrieved {}, Failed {} news articles).".format(
        subset_name, crawler_status["success"], crawler_status["fail"]))


def main():
    # Creating logs directory.
    if not os.path.exists(const.fp_logs):
        os.makedirs(const.fp_logs)

    # Download Lusa subset.
    print("Downloading Lusa subset - Starting...")
    gdd.download_file_from_google_drive(file_id=const.lusa_subset_google_id,
                                        dest_path=const.fp_lusa_subset,
                                        unzip=True)
    os.remove(const.fp_lusa_subset)
    print("Downloading Lusa subset - Complete.\n")

    # Download other subsets.
    with open(const.fp_mind_metadata, encoding='utf-8') as json_file:
        mind_metadata = json.load(json_file)

    download_subset_newspaper3k("Fact remaining", mind_metadata[0:6000])
    download_subset_newspaper3k("Opinion", mind_metadata[6000:12000])
    download_subset_newspaper3k("Entertainment", mind_metadata[12000:18000])
    download_subset_newspaper3k("Satire", mind_metadata[18000:19029])
    download_subset_newspaper3k("Conspiracy", mind_metadata[19029:])


if __name__ == '__main__':
    main()
