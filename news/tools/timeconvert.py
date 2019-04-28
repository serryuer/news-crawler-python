import re
 
class DateFormat(object):
    regex1 = re.compile(r".*([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日 ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})")
    regex2 = re.compile(r".*([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日 ([0-9]{1,2}):([0-9]{1,2})")
    regex3 = re.compile(r".*([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日")
    regex4 = re.compile(r".*([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})")
    regex5 = re.compile(r".*([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2})")
    regex6 = re.compile(r".*([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})")
    dateformatregexs = [regex1, regex2, regex3, regex4, regex5, regex6]
 
    monthMap = {"sep": "9", "oct": "10", "nov": "11", "dec": "12", "jan": "1", "feb": "2",
                "aug": "8", "jul": "7", "jun": "6", "may": "5", "apr": "4", "mar": "3"}
    monthMap2 = {"September": "9", "October": "10", "November": "11", "December": "12",
                 "January": "1", "February": "2", "August": "8", "July": "7",
                 "June": "6", "May": "5", "April": "4", "March": "3"}
    @classmethod
    def convertStandardDateFormat(cls, datestr: str) -> str:
        """
        转换日期格式
        :param datestr:
        :return:
        """
        res = ""
        if datestr is None:
            return res
        format_time = ""
        for i in range(0, len(cls.dateformatregexs)):
            try:
                regex = cls.dateformatregexs[i]
                match = regex.match(datestr)
                if match is not None:
                    if 0 == i or 3 == i:
                        format_time = match.group(1) + "-" + match.group(2) + "-" + match.group(3) + " " + match.group(4) + ":" + match.group(5) + ":" + match.group(6)
                        return format_time
                    if 1 == i or 4 == i:
                        format_time = match.group(1) + "-" + match.group(2) + "-" + match.group(3) + " " + match.group(4) + ":" + match.group(5) + ":00"
                        return format_time
                    if 2 == i or 5 == i:
                        format_time = match.group(1) + "-" + match.group(2) + "-" + match.group(3) + " 00:00:00"
                        return format_time
            except Exception as e:
                return None
        return None

if __name__ == '__main__':
    print(DateFormat.convertStandardDateFormat(" 2019-04-28 20:26:43"))
