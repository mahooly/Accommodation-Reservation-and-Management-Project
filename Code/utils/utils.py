from khayyam import JalaliDate


def convert_string_to_date(date_string):
    persian_numbers = '۱۲۳۴۵۶۷۸۹۰'
    english_numbers = '1234567890'
    trans_num = str.maketrans(persian_numbers, english_numbers)
    split_string = [int(x.translate(trans_num)) for x in date_string.split('/')]
    return JalaliDate(split_string[0], split_string[1], split_string[2]).todate()
