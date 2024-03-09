from venv import logger 
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from time import sleep
from DB import get_data_from_DB
from get_24 import get_company_name_24, get_title_24, get_job_24, get_headquater_24, get_NumEmployee_24, get_Exp_24, get_level_24, get_Salary_24,get_Edu_24, get_Requirement_24, get_Description_24, get_Date_24, get_SrcPic_24, get_Time_24, get_Place_24, get_Age_24, get_probation, get_Sex_24, get_Way_24, get_right_24

def get_profile_urls_24(driver, url):
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        class_name = 'relative lg:h-[115px] w-full flex rounded-sm border lg:mb-3 mb-2 lg:hover:shadow-md !hover:bg-white !bg-[#FFF5E7] border-se-blue-10'
        a = page_source.find_all('a', class_=class_name)
        all_profile_urls = []
        for profile in a:
            profile_url = 'https://vieclam24h.vn' + profile.get('href')
            if profile_url not in all_profile_urls:
                all_profile_urls.append(profile_url)
        return all_profile_urls
    except Exception as e:
        logger.error(f"Error occurred while extracting profile URLs from {url}: {e}")
        return []
    
def get_profile_info_24(driver, url):
    try:
        driver.get(url)
        sleep(2)
        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        company_name = get_company_name_24(page_source)
        title = get_title_24(page_source)
        date = get_Date_24(page_source)
        salary = get_Salary_24(page_source)
        exp_year = get_Exp_24(page_source)
        level = get_level_24(page_source)
        num_of_employee = get_NumEmployee_24(page_source)
        edu = get_Edu_24(page_source)
        src_pic = get_SrcPic_24(page_source)
        head_quater = get_headquater_24(page_source)
        description = get_Description_24(page_source)
        requirement = get_Requirement_24(page_source)
        job = get_job_24(page_source)   
        time = get_Time_24(page_source) #new
        place = get_Place_24(page_source)
        age = get_Age_24(page_source)
        sex = get_Sex_24(page_source)
        probation = get_probation(page_source)
        way = get_Way_24(page_source)
        right = get_right_24(page_source)
        return [title, company_name, time, place, age, sex, probation, way, job, head_quater, num_of_employee, exp_year, level, salary, edu, right, description, requirement, date, src_pic]
    except Exception as e:
        logger.error(f"Error occurred while scraping data from {url}: {e}")
        return []
    
def is_duplicated(info, data):
    for i in data:
        if i[1] == info[0] and i[2] == info[1] and i[3] == info[2] and i[4] == info[3] and i[5] == info[4] and i[6] == info[5] and i[7] == info[6] :
            return True
    return False

def get_vieclam24(driver, num_pages):
    try:
        page_start = 1
        data =[]
        while page_start <= num_pages:
            url = f'https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?page={page_start}&sort_q='
            print('>>>URL', url)
            driver.get(url)
            sleep(2)
            profile_urls = get_profile_urls_24(driver, url)
            data_DB = get_data_from_DB()     
            for i in profile_urls:
                info = get_profile_info_24(driver, i)
                print('>> Vieclam24:',info)
                if info == []:
                    pass
                else:
                    if not is_duplicated(info , data_DB):
                        print('>> Have Not Exist In DB')
                        data.append(info)
                    else:
                        print('>> In DB')
            page_start += 1
        return data
    except Exception as e:
        print(f"Error occurred while get data 24h: {e}")
        return []
   
