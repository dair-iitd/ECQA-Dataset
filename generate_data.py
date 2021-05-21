import json
import pandas as pd

DECQA_FILE = './ecqa.jsonl'
CQA_FILES = ['./cqa/train_rand_split.jsonl', './cqa/dev_rand_split.jsonl']

label2idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}


lines = []
for filename in CQA_FILES:
	with open(filename) as f:
		for line in f:
			lines.append(json.loads(line))

data = {}
for line in lines:
	id = line['id']
	answerKey = line['answerKey']
	tmp_ques_obj = line['question']
	question = tmp_ques_obj['stem']
	concept = tmp_ques_obj['question_concept']
	choices_obj = tmp_ques_obj['choices']
	choices = ['' for i in range(5)]
	for choice in choices_obj:
		choices[label2idx[choice['label']]] = choice['text']
	answer = choices[label2idx[answerKey]]
	data[id] = {'question': question, 'answer': answer, 'choices': choices, 'concept': concept}

print(len(data.keys()))

lines = []
with open(DECQA_FILE) as f:
	for line in f:
		lines.append(json.loads(line))

print(len(lines))

twice = 0
not_found = 0

for line in lines:
	id = line['id']
	if ('positives' not in line) or ('negatives' not in line) or ('explanation' not in line):
		print(id, 'not in decqa')
		not_found += 1
	elif ('positives' in data[id]) and ('negatives' in data[id]) and ('freeflow' in data[id]):
		if line['explanation']!=data[id]['freeflow']:
			print(id, 'twice in decqa')
			twice += 1
			# print(line['positives'])
			# print(line['negatives'])
			# print(line['explanation'])
			# print(data[id]['positives'])
			# print(data[id]['negatives'])
			# print(data[id]['freeflow'])
	else:
		positives = line['positives']
		negatives = line['negatives']
		freeflow = line['explanation']
		data[id]['positives'] = positives
		data[id]['negatives'] = negatives
		data[id]['freeflow'] = freeflow

print('# Not Found', not_found)
print('# Twice', twice)

total = 0
q_ids = []
q_concept = []
q_text = []
q_op1 = []
q_op2 = []
q_op3 = []
q_op4 = []
q_op5 = []
q_ans = []
q_ans = []
taskA_pos = []
taskA_neg = []
taskB = []

for id in data.keys():
	if ('positives' in data[id]) and ('negatives' in data[id]) and ('freeflow' in data[id]):
		total += 1
		q_ids.append(id)
		q_concept.append(data[id]['concept'])
		q_text.append(data[id]['question'])
		q_ans.append(data[id]['answer'])
		q_op1.append(data[id]['choices'][0])
		q_op2.append(data[id]['choices'][1])
		q_op3.append(data[id]['choices'][2])
		q_op4.append(data[id]['choices'][3])
		q_op5.append(data[id]['choices'][4])
		taskA_pos.append('\n'.join(data[id]['positives']))
		taskA_neg.append('\n'.join(data[id]['negatives']))
		taskB.append(data[id]['freeflow'])


print(total)
print(len(q_ids), len(q_concept), len(q_text), len(q_op1), len(q_op2), len(q_op3), len(q_op4), len(q_op5), len(q_ans), len(taskA_pos), len(taskA_neg), len(taskB))
tmp_data = {'q_no':  q_ids,
 		'q_concept': q_concept,
		'q_text': q_text,
		'q_op1': q_op1,
		'q_op2': q_op2,
		'q_op3': q_op3,
		'q_op4': q_op4,
		'q_op5': q_op5,
		'q_ans': q_ans,
		'taskA_pos': taskA_pos,
		'taskA_neg': taskA_neg,
		'taskB': taskB,
		 }
df = pd.DataFrame(tmp_data, columns = ['q_no', 'q_concept', 'q_text', 'q_op1', 'q_op2', 'q_op3', 'q_op4', 'q_op5',
									'q_ans', 'taskA_pos', 'taskA_neg', 'taskB'])
# print(df.shape[0])
# df = df[df['taskB'].str.split().str.len().gt(1)]
# df = df[df['taskA_pos'].str.split().str.len().gt(1)]
# df = df[df['taskA_neg'].str.split().str.len().gt(1)]
# print(df.shape[0])

df.to_csv('cqa_data.csv', encoding='utf-8')

split_files = ['./author_split/train_ids.txt', './author_split/val_ids.txt', './author_split/test_ids.txt']
output_files = ['cqa_data_train.csv', 'cqa_data_val.csv', 'cqa_data_test.csv']

for split_idx in range(3):
	ids = []
	with open(split_files[split_idx]) as f:
		for line in f:
			ids.append(line.strip())
	total = 0
	q_ids = []
	q_concept = []
	q_text = []
	q_op1 = []
	q_op2 = []
	q_op3 = []
	q_op4 = []
	q_op5 = []
	q_ans = []
	q_ans = []
	taskA_pos = []
	taskA_neg = []
	taskB = []

	for id in ids:
		if ('positives' in data[id]) and ('negatives' in data[id]) and ('freeflow' in data[id]):
			total += 1
			q_ids.append(id)
			q_concept.append(data[id]['concept'])
			q_text.append(data[id]['question'])
			q_ans.append(data[id]['answer'])
			q_op1.append(data[id]['choices'][0])
			q_op2.append(data[id]['choices'][1])
			q_op3.append(data[id]['choices'][2])
			q_op4.append(data[id]['choices'][3])
			q_op5.append(data[id]['choices'][4])
			taskA_pos.append('\n'.join(data[id]['positives']))
			taskA_neg.append('\n'.join(data[id]['negatives']))
			taskB.append(data[id]['freeflow'])


	print(total)
	print(len(q_ids), len(q_concept), len(q_text), len(q_op1), len(q_op2), len(q_op3), len(q_op4), len(q_op5), len(q_ans), len(taskA_pos), len(taskA_neg), len(taskB))
	tmp_data = {'q_no':  q_ids,
	 		'q_concept': q_concept,
			'q_text': q_text,
			'q_op1': q_op1,
			'q_op2': q_op2,
			'q_op3': q_op3,
			'q_op4': q_op4,
			'q_op5': q_op5,
			'q_ans': q_ans,
			'taskA_pos': taskA_pos,
			'taskA_neg': taskA_neg,
			'taskB': taskB,
			 }
	df = pd.DataFrame(tmp_data, columns = ['q_no', 'q_concept', 'q_text', 'q_op1', 'q_op2', 'q_op3', 'q_op4', 'q_op5',
										'q_ans', 'taskA_pos', 'taskA_neg', 'taskB'])
	df.to_csv(output_files[split_idx], encoding='utf-8')
