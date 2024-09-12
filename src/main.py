from pathlib import Path

from parser import LuntryParser
from report_builder import ReportBuilder
import sys
import getopt

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["reports-dir=", "db-path=", "output-dir="])
    except getopt.GetoptError as err:
        print(err)  # выведет что-то вроде "option-a not recognized"
        # показать справку и выйти
        # `usage()` здесь не определена
        # usage()
        sys.exit(2)

    for o, a in opts:
        if o == '--reports-dir':
            reports_dir = Path(a)

        if o == '--db-path':
            db_path = Path(a)

        if o == '--output-dir':
            output_dir = Path(a)

    parsed_reports = LuntryParser.parse_from_directory(reports_dir)
    grouped_by_image = LuntryParser.group_by_image_name(parsed_reports)
    reports_with_cve = LuntryParser.create_image_cves(grouped_by_image)
    ReportBuilder.update_db(db_path, grouped_by_image, reports_with_cve)
