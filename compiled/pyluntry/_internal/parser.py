import json
import os
import re
from collections import defaultdict
from pathlib import Path


class LuntryParser:

    @staticmethod
    def parse_from_directory(reports_dir: str) -> list[dict[str, str]]:
        """
        Парсит json отчеты Luntry из директории

        :param reports_dir: абсолютный путь до директории с отчетами
        :return: список объектов с отчетами
        """
        current_dir, other_dirs, reports = next(os.walk(reports_dir))

        result = []
        for report in reports:
            file_name = Path(current_dir) / report
            with open(file_name, 'r') as file:
                data = json.load(file)
                for current_report in data:
                    result.append(current_report)
        return result

    @staticmethod
    def group_by_image_name(reports: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
        """
        Группирует отчеты по наименованию образа

        :param reports: список объектов с отчетами
        :return: словарь, где в качестве ключа выступает имя образа, а значение список отчетов
        """

        pattern = r'/(.*?)(?=@)'

        # Поиск с использованием регулярного выражения
        result = defaultdict(list)
        for report in reports:
            image_string = report["ImageID"]
            match = re.search(pattern, image_string)
            image_name = match.group(1)

            result[image_name].append(report)

        # Убираем дубликаты
        for image in result:
            result[image] = list({v['ID']: v for v in result[image]}.values())

        return result

    @staticmethod
    def create_image_cves(reports: dict[str, list[dict[str, str]]]) -> dict[str, set]:
        """
        Возвращает словарь вида {"имя_образа": {cve_id}}

        :param reports: сгруппированные отчеты по имени образа
        """
        result = defaultdict(set)

        for image in reports:
            for report in reports[image]:
                result[image].add(report["ID"])
        return result
