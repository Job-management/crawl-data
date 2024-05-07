from venv import logger


def get_company_name_topdev(source):

    return source.find(
        "p", class_="my-1 line-clamp-1 text-base font-bold text-gray-500"
    ).get_text(" ", strip=True)


def get_title_topdev(source):

    return source.find("h1", class_="text-2xl font-bold text-black").get_text(
        " ", strip=True
    )


def get_jobs_topdev(source):

    return source.find("h1", class_="text-2xl font-bold text-black").get_text(
        " ", strip=True
    )


def get_headquater_topdev(source):

    return source.find("div", class_="w-11/12").get_text(" ", strip=True)


def get_num_employee_topdev(source):

    return "None"


def get_exp_topdev(source):

    div = source.find_all("div", class_="item-card-info")

    if len(div) > 0:

        return div[0].find("a", class_="hover:text-primary-300").get_text(strip=True)

    return "None"


def get_level_topdev(source):

    div = source.find_all("div", class_="item-card-info")

    if len(div) > 1:

        return div[1].find("a", class_="hover:text-primary-300").get_text(strip=True)

    return "None"


def get_salary_topdev(source):

    # need login cookie

    # div = source.find('div', class_='flex max-w-[540px] items-center')

    # if(len(div) > 0) :

    #     return div[0].find('p', class_='text-primary').get_text(strip=True)

    return "None"


def get_edu_topdev(source):

    return "None"


def get_requirement_topdev(source):

    div = source.find_all("div", class_="rounded bg-white p-4 md:px-6 md:py-4")

    res = ""

    if div:

        second_div = div[0]

        lis = second_div.find_all("ul")[1].find_all("li")

        for li in lis:

            res += li.get_text(strip=True) + "\n"

        return res

    else:

        return "None"


def get_description_topdev(source):

    div = source.find(
        "div",
        class_="prose mb-4 max-w-full border-b border-gray-200 pb-2 text-sm last:mb-0 last:border-0 last:pb-0 lg:text-base",
    )

    return div.get_text(strip=True)


def get_date_topdev(source):

    return "None"


def get_src_pic_topdev(source):

    div = source.find(
        "div", class_="flex w-[21%] flex-initial items-center justify-center bg-white"
    )

    return div.find("img").get("src")


def get_time_topdev(source):

    return "None"


def get_place_topdev(source):

    return source.find("div", class_="w-11/12").get_text(" ", strip=True)


def get_probation_topdev(source):

    return "None"


def get_sex_topdev(source):

    return "None"


def get_way_topdev(source):

    return "None"


def get_age_topdev(source):

    return "None"


def get_right_topdev(source):

    return "None"
