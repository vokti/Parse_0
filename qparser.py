from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from model import Question
from time import sleep


class ProgHub(object):

    def __init__(self, driver, lang):
        self.driver = driver
        self.lang = lang

    def parse(self):
        self.go_to_tests_page()
        self.parse_question_page()

    def parse_question_page(self):
        question = Question()
        self.fill_question_text(question)
        self.fill_question_code(question)
        self.fill_answer(question)
        self.choose_answer()
        self.right_answer(question)
        self.next_question()
        p = question
        return p

    def go_to_tests_page(self):
        self.driver.get("https://proghub.ru/tests")
        slide_elms = self.driver.find_elements_by_class_name('carousel__card')

        for elem in slide_elms:
            lang_link = elem.get_attribute('href')
            if self.lang in lang_link:
                language = lang_link.split('/')[-1]
                self.driver.get('https://proghub.ru/t/' + language)
                link = self.driver.find_element_by_class_name("btn-cyan").get_attribute('href')
                self.driver.get(link)
                break

    def fill_question_text(self, question):
        try:
            sleep(0.5)
            question_text_elm = self.driver.find_element_by_tag_name('h3')
            question.text = question_text_elm.text
        except NoSuchElementException:
            print('Question text missing')

    def fill_question_code(self, question):
        try:
            question_code_elm = self.driver.find_element_by_tag_name('pre')
            question.code = question_code_elm.text
        except NoSuchElementException:
            pass

    def fill_answer(self, question):
        try:
            question_answers = self.driver.find_element_by_class_name('question__answer_list')
            for x in question_answers.text.split('\n'):
                question.answers.append(str(x))
        except NoSuchElementException:
            pass

    def choose_answer(self):
        sleep(0.5)
        try:
            self.driver.find_element_by_class_name('question__answer_item').click()
            sleep(0.5)
            self.driver.find_element_by_class_name('btn-primary').click()
        except NoSuchElementException:
            pass

    def right_answer(self, question):
        sleep(0.5)
        quests = self.driver.find_elements_by_class_name('question__answer_item')
        for right_question in quests:
            if (right_question.get_attribute('class') == 'question__answer_item correct' or
                    right_question.get_attribute('class') == 'question__answer_item selected correct'):
                text = right_question.text
                for x, _ in enumerate(question.answers):
                    if question.answers[x] == text:
                        question.answers[x] += ' right'

    def next_question(self):
        self.driver.find_element_by_class_name('btn-cyan').click()


def main():
    driver = webdriver.Chrome()
    parser = ProgHub(driver, 'python')
    parser.parse()


if __name__ == "__main__":
    main()
