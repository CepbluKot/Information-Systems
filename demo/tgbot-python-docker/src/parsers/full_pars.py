import prep_text_pars


def parse_group(index):
    full_prepods_list = []
    begin_week = 1
    end_week = 30
    for week in range(begin_week, end_week):
        curr_week = prep_text_pars.get_prepods_text_list_page(
            'https://mai.ru/education/studies/schedule/index.php?group={1}&week={0}#'.format(week, index))
        for prep in curr_week:
            if prep not in full_prepods_list:
                full_prepods_list.append(prep)

    return full_prepods_list


def parse_group_today(index):
    full_prepods_list = []

    curr_week = prep_text_pars.get_prepods_text_list_page(
        'https://mai.ru/education/studies/schedule/index.php?group={0}#'.format(index))
    for prep in curr_week:
        if prep not in full_prepods_list:
            full_prepods_list.append(prep)

    return full_prepods_list


def parse_prepod(url):
    begin_week = 1
    end_week = 18 + 1
    full_lessons_list = []

    for week in range(begin_week, end_week):
        if not 'week=' in url:
            tru_url = url[:-1]

            curr_week = prep_text_pars.get_prepod_page(
                (tru_url + '&week={0}#'.format(week)))

            for lesson in curr_week:
                if lesson not in full_lessons_list:
                    full_lessons_list.append(lesson)
        else:
            curr_week = prep_text_pars.get_prepod_page((url))
            if curr_week not in full_lessons_list:
                full_lessons_list.append(curr_week)
    return full_lessons_list


print(parse_prepod('https://mai.ru/education/studies/schedule/ppc.php?guid=d72d63e7-1d99-11e0-9baf-1c6f65450efa#'))
# print(parse_group('М3О-221Б-20'))
# print(parse_group_today('М3О-221Б-20'))
# for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
#    print(data['group'])
