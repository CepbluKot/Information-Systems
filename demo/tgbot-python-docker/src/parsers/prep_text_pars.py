import requests
from bs4 import BeautifulSoup


def get_prepods_text_list_page(url):

    prepod_list = []

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for select_div in soup.find_all("div", {"class": "mb-4"}):
        for select_lesson in select_div.find_all("p", {"class": "mb-2 fw-semi-bold text-dark"}):
            lesson_part_one = " ".join(select_lesson.find(
                text=True, recursive=False).split())

            for select_lesson_next in select_lesson.find_all("span", {"class": "text-nowrap"}):
                lesson_part_two = " ".join(select_lesson_next.find(
                    text=True, recursive=False).split())
                full_lesson = lesson_part_one + " " + lesson_part_two

                for lesson_type in select_lesson_next.find_all("span", {"class": "badge bg-soft-secondary text-secondary ms-2 fw-medium text-smaller"}):
                    type = " ".join(lesson_type.find(
                        text=True, recursive=False).split())

        for select_prepod in select_div.find_all("a", {"class": "text-body"}):
            if {"prepod": select_prepod.text, "lesson": full_lesson} not in prepod_list:
                
                prepod_list.append(
                    {"prepod": select_prepod.text, "lesson": full_lesson, "role": type})

    return(prepod_list)


def get_prepod_page(url):
    lessons_list = []
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    prepod_name = " ".join(
        (soup.find("h1", {"class": "mb-5"}).find(text=True)).split())
    # print(" ".join((soup.find("h3", {"class": "me-5 mb-2 fw-medium"}).find(text=True)).split()))
    for select_div in soup.find_all("div", {"class": "mb-4"}):
        
        for select_group_area in select_div.find_all("ul", {"class": "list-inline list-separator text-body small"}):
            
            for select_group in select_group_area.find_all("a", {"class": "text-body"}):
                
                group = " ".join(select_group.find(
                    text=True, recursive=False).split())

                for select_lesson_area in select_div.find_all("div", {"class": "d-flex align-items-center justify-content-between"}):
                    
                    for select_lesson_area_first_part in select_lesson_area.find_all("p", {"class": "mb-2 fw-semi-bold text-dark"}):

                        lesson_part_one = " ".join(select_lesson_area_first_part.find(
                            text=True, recursive=False).split())

                        for select_lesson_area_second_part in select_lesson_area_first_part.find_all("span", {"class": "text-nowrap"}):

                            lesson_part_two = " ".join(select_lesson_area_second_part.find(
                                text=True, recursive=False).split())

                            for select_lesson_type in select_lesson_area_second_part.find_all("span", {"class": "badge bg-soft-secondary text-secondary ms-2 fw-medium text-smaller"}):

                                lesson_type = " ".join(select_lesson_type.find(
                                    text=True, recursive=False).split())

                                if not {"prepod": prepod_name, "lesson": lesson_part_one + lesson_part_two, "group": group} in lessons_list:
                                    lessons_list.append(
                                        {"prepod": prepod_name, "lesson": lesson_part_one + " " + lesson_part_two, "group": group})
                                    print(lessons_list)
    return lessons_list


# print(get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d72d63e7-1d99-11e0-9baf-1c6f65450efa&week=1#'))
