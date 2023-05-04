import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = f'Create a multiple choice quiz on the topic of {topic} consisting ' \
        + f'of {num_questions} questions. Each question should have {num_possible_answers} ' \
        + f'options. Make sure all of the correct answers are not the same letter. ' \
        + f'Also include the correct answer for each question using the ' \
        + f'starting string "Correct Answer:" '

    return prompt


def create_student_view(ai_response, num_questions):
    student_view = {1: ''}
    question_number = 1
    for line in ai_response.split('\n'):
        if not line.startswith('Correct Answer:'):
            student_view[question_number] += line + '\n'
        else:
            if question_number < num_questions:
                question_number += 1
                student_view[question_number] = ''
    return student_view


def get_answer_key(ai_choices, num_questions):
    answers = {1: ''}
    question_number = 1
    for line in ai_choices.split('\n'):
        if line.startswith('Correct Answer:'):
            answers[question_number] += line + '\n'
            if question_number < num_questions:
                question_number += 1
                answers[question_number] = ''
    return answers


def take(student_view):
    student_answers = {}
    for question, question_text in student_view.items():
        print(question_text)
        answer = input('Enter your answer: ')
        student_answers[question] = answer
    return student_answers


# def grade(student_answers, answer_key):
#     correct_answers = 0
#     for question, answer in student_answers.items():
#         if answer.upper() == answer_key[question][16]:
#             correct_answers += 1
#     score = 100 * correct_answers / len(answer_key)
#     return score


response = openai.Completion.create(engine='text-davinci-003',
                                    prompt=create_test_prompt('Mexican History', 4, 4),
                                    max_tokens=256,
                                    temperature=0.7)
raw_test_body = response['choices'][0]['text']
answer_key = get_answer_key(raw_test_body, 4)
student_test_view = create_student_view(raw_test_body, 4)

# for key in student_test_view:
#     print(student_test_view[key])

students_test_answers = take(student_test_view)

print(raw_test_body)
print(answer_key)
print(student_test_view)
print(students_test_answers)
# student_score = grade(students_test_answers, answer_key)
# print(f'Your score is {student_score}%')
