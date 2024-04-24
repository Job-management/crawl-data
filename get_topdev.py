from venv import logger
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from time import sleep
from DB import get_data_from_DB
from get_info_topdev import get_company_name_topdev,get_title_topdev,get_jobs_topdev,get_headquater_topdev, get_num_employee_topdev,get_exp_topdev, get_level_topdev, get_salary_topdev, get_edu_topdev, get_requirement_topdev,get_description_topdev, get_date_topdev , get_src_pic_topdev,get_time_topdev,  get_place_topdev, get_probation_topdev,get_sex_topdev, get_way_topdev,  get_age_topdev, get_right_topdev 

def get_profile_urls_topdev(driver, url):
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    # with open('page_source.txt', 'w') as f:
    #     # Ghi dữ liệu vào tệp
    #     f.write(str(page_source))
    try:
        class_name = 'block h-[7.5rem] w-[10rem]'
        a = page_source.find_all('a', class_=class_name)
        all_profile_urls = []
        for profile in a:
            profile_url = 'https://topdev.vn' + profile.get('href')
            if profile_url not in all_profile_urls:
                all_profile_urls.append(profile_url)
        return all_profile_urls
    except Exception as e:
        logger.error(f"Error occurred while extracting profile URLs from {url}: {e}")
        return []
    
def get_profile_info_topdev(driver, url):
    try:
        driver.get(url)
        sleep(2)
        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        company_name = get_company_name_topdev(page_source)
        title = get_title_topdev(page_source)
        date = get_date_topdev(page_source)
        salary = get_salary_topdev(page_source)
        exp_year = get_exp_topdev(page_source)
        level = get_level_topdev(page_source)
        num_of_employee = get_num_employee_topdev(page_source)
        edu = get_edu_topdev(page_source)
        src_pic = get_src_pic_topdev(page_source)
        head_quater = get_headquater_topdev(page_source)
        description = get_description_topdev(page_source)
        requirement = get_requirement_topdev(page_source)
        job = get_jobs_topdev(page_source)
        time = get_time_topdev(page_source) #new
        place = get_place_topdev(page_source)
        age = get_age_topdev(page_source)
        sex = get_sex_topdev(page_source)
        probation = get_probation_topdev(page_source)
        way = get_way_topdev(page_source)
        right = get_right_topdev(page_source)
        return [title, company_name, time, place, age, sex, probation, way, job, head_quater, num_of_employee, exp_year, level, salary, edu, right, description, requirement, date, src_pic]
    except Exception as e:
        logger.error(f"Error occurred while scraping data from {url}: {e}")
        return []
    

def is_duplicated(info, data):
    for i in data:
        if i[1] == info[0] and i[2] == info[1] and i[3] == info[2] and i[4] == info[3] and i[5] == info[4] and i[6] == info[5] and i[7] == info[6] :
            return True
    return False

def get_job_topdev(driver):
    try:
        data =[]
        url = f'https://topdev.vn/viec-lam-it'
        print('>>>URL', url)
        driver.get(url)
        sleep(2)
        profile_urls = get_profile_urls_topdev(driver, url)
        data_DB = get_data_from_DB("root", "TvaT2201$")
        for _url in profile_urls:
            info = get_profile_info_topdev(driver, _url)
            print('>> Vieclam24:', info)
            if info == []:
                pass
            else:
                if not is_duplicated(info, data_DB):
                    print('>> Have Not Exist In DB')
                    data.append(info)
                else:
                    print('>> In DB')
        return data
    except Exception as e:
        print(f"Error occurred while get data 24h: {e}")
        return []