from squad.demo_prepro import prepro
from basic.demo_cli import Demo
import sys

demo = Demo()


def answer_para_question(paragraph, question):
	pq_prepro = prepro(paragraph, question)
	answer = demo.run(pq_prepro)
	if len(answer) == 0:
		return "Oops, no answer found!"
	return answer


if __name__ == "__main__":
	p = open(sys.argv[1], 'r')
	paragraph = []
	for line in p:
		paragraph.append(line.rstrip())
	paragraph = " ".join(paragraph)
	question = " ".join(sys.argv[2:])
	print(answer_para_question(paragraph, question))

