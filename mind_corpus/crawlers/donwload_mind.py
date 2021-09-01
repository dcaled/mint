import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import mind_corpus.constants as const


def main():
    gdd.download_file_from_google_drive(file_id=const.lusa_subset_google_id,
                                        dest_path=const.fp_lusa_subset,
                                        unzip=True)
    os.remove(const.fp_lusa_subset)
    print("Download status - Lusa subset complete.")


if __name__ == '__main__':
    main()
